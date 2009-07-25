# -*- coding: utf-8 -*-

"""
TEST_BSXPath.py: Test Script for BSXPath

"""

import sys,os,glob,re,datetime,optparse
import urllib2
import pdb

from BSXPath import BSXPathEvaluator,XPathResult
from BSXPath import ExtDict,typeof,toString

(document,options,url_data)=(None,None,u'http://svn.coderepos.org/share/lang/javascript/javascript-xpath/trunk/test/functional/data/')
DEFAULT_TESTDIR='testdata'

uai={'gecko':True,'opera95':True} # User Agent(dummy)

def escapeStr(str):
  return re.sub(r'\r?\n',r'\\n',re.sub(r'\\',r'\\\\',re.sub(r'"',r'\\"',str)))

def parseTestData(datafile,web=False):
  try:
    f=urllib2.urlopen(datafile) if web else open(datafile)
    data=f.read()
    f.close()
    (comment,html,contextExpr,testData)=data.split('\n--------\n')
    testDataSplited=testData.split('\n')
    
    tests=[]
    for testline in testDataSplited:
      if re.search(r'^\s*#',testline): continue
      #mrslt=re.search(r'^\s*(.*?)\s*=>\s*(.*?)?\s*$',testline)
      mrslt=re.search(r'^\s*(.*?)\s*=>\s*(.*?)\s*$',testline)
      if mrslt:
        tests.append(ExtDict({'expr':mrslt.group(1),'data':mrslt.group(2)}))
    return ExtDict({'comment':comment,'html':html,'contextExpr':contextExpr,'tests':tests})
  except:
    return None

#{ // NodeTest
class NodeTest(object):
  def __init__(self,data):
    self.nodes=[]
    if not data: data=''
    
    if re.search(r'^\s*\(none\)\s*$',data): return
    
    def chktoken(mrslt):
      token=mrslt.group()
      uas = nodeData = nodeType = nodeName = nodeValue = None
      m=re.search(r'([\w-]+)\(((([\w-]+)=)?("[^"]*"|\'[^\']*\'|-?\d+|NaN|-?Infinity|true|false)?)\)((:\w+)*)',token)
      if m:
        nodeType=self.typeMap[m.group(1)]
        if nodeType==0:
          nodeName = '#value'
          nodeValue = m.group(2)
        elif nodeType==2 or nodeType==7:
          nodeName = m.group(4)
          nodeValue = m.group(5)
        elif nodeType==3:
          nodeName = '#text'
          nodeValue = m.group(2)
        elif nodeType==4:
          nodeName = '#cdata-section'
          nodeValue = m.group(2)
        elif nodeType==8:
          nodeName = '#comment'
          nodeValue = m.group(2)
        elif nodeType==9:
          nodeName = '#document'
          nodeValue = None
        else:
          nodeValue = m.group(2)
          
        if nodeValue and nodeType != 0:
          first = nodeValue[0]
          last = nodeValue[-1]
          if last==first and (first == '"' or first == "'"):
            nodeValue = eval(nodeValue)
        uas = m.group(6).split(':')
      else:
        m = re.search(r'((\w+)((\.[\w-]+|#[\w-]+|\[[\w-]+=("[^"]*"|\'[^\']*\')\])*))((:\w+)*)',token)
        nodeType = 1
        nodeName = m.group(2)
        nodeDatas = m.group(3)
        nodeDatas = re.findall(r'\.[\w-]+|#[\w-]+|\[[\w-]+=(?:"[^"]*"|\'[^\']*\')\]',nodeDatas)
        
        class nd_class(object):
          def __init__(self,name):
            self.type='class'
            self.name=name
          def match(self,node):
            classes=re.split(r'\s+',node.get('class',''))
            for _class in classes:
              if _class==self.name:
                return True
            return False
        
        class nd_id(object):
          def __init__(self,name):
            self.type='attr'
            self.name=name
          def match(self,node):
            return node.get('id')==self.name
        
        class nd_attr(object):
          def __init__(self,name,value):
            self.type='attr'
            self.name=name
            self.value=value
          def match(self,node):
            return node.get(self.name)==self.value
        
        nodeData = []
        for data in nodeDatas:
          ch=data[0]
          if ch=='.':
            nodeData.append(nd_class(data[1:]))
          elif ch=='#':
            nodeData.append(nd_id(data[1:]))
          elif ch=='[':
            data = data[1:-1].split('=')
            #nodeData.append(nd_attr(data[0],data[1]))
            nodeData.append(nd_attr(data[0],eval(data[1])))
          else:
            pass
        
        uas = m.group(6).split(':')
        
      if uas: uas=filter(lambda x:x,uas)
      
      def createNodeInfo(nodeType, nodeName, nodeValue, nodeData):
        def _match(snode,node):
          if node.nodeType != snode.nodeType: return False
          if node.nodeName != snode.nodeName: return False
          if node.nodeValue != snode.nodeValue: return False
          if snode.nodeData:
            for nodeData in snode.nodeData:
              if not nodeData.match(node): return False
          return True
        
        return ExtDict({
          'nodeType' : nodeType
        , 'nodeName' : nodeName
        , 'nodeValue': nodeValue
        , 'nodeData' : nodeData
        , 'match'    : _match
        })
      
      #self.nodes.append(createNodeInfo(nodeType, nodeName, nodeValue, nodeData))
      if uas:
        for ua in uas:
          if uai.get(ua):
            self.nodes.append(createNodeInfo(nodeType, nodeName, nodeValue, nodeData))
      else:
        self.nodes.append(createNodeInfo(nodeType, nodeName, nodeValue, nodeData))

      return token
    
    tokens=re.sub(r'([\w-]+\(.*?\)|\w+(\.[\w-]+|#[\w-]+|\[[\w-]+=("[^"]*"|\'[^\']*\')\])*)(:\w+)*',chktoken,data)
    
    if len(self.nodes)==1 and self.nodes[0].nodeType==0:
      self.primitive = True
      #self.value = self.nodes[0].nodeValue
      nodeValue=self.nodes[0].nodeValue
      try:
        self.value = eval(nodeValue)
      except:
        if nodeValue=='true':
          self.value = True
        elif nodeValue=='false':
          self.value = False
  
  typeMap = {
    'value'                 : 0
  , 'element'               : 1
  , 'attribute'             : 2
  , 'text'                  : 3
  , 'cdata-section'         : 4
  , 'entity-reference'      : 5
  , 'entity'                : 6
  , 'processing-instruction': 7
  , 'comment'               : 8
  , 'document'              : 9
  , 'document-type'         : 10
  , 'document-fragment'     : 11
  , 'notation'              : 12
  }
  
  def test(self,nodes):
    if len(nodes)!=len(self.nodes):
        print u' (*) node number error: %d vs %d' % (len(nodes),len(self.nodes))
        return False
    for i in range(0,len(nodes)):
      snode=self.nodes[i]
      if not snode.match(snode,nodes[i]):
        print u'%s' % (snode)
        print u'%s' % (nodes[i])
        try:
          print u' (*) node error: %s' % (nodes[i])
        except:
          print u' (*) node error:'
          print nodes[i]
        return False;
    return True

#} // NodeTest


def testNodes(nodes,data):
  tester=NodeTest(data)
  if getattr(tester,'primitive',False):
    if tester.value == nodes:
      return ExtDict({'status':'OK','detail':'-'})
    else:
      if typeof(tester.value)!='string':
        return ExtDict({'status':'NG','detail':'value(' + toString(nodes) + ')'})
      else:
        return ExtDict({'status':'NG','detail':'value("' + escapeStr(toString(nodes)) + '")'})
  
  if tester.test(nodes):
    return ExtDict({'status':'OK','detail':'-'})
  
  detail = []
  for node in nodes:
      t = ''
      nodeType=node.nodeType
      if nodeType==1:
        t += node.nodeName
        if node.id:
          t += '#' + node.id
        if node.className:
          classes = re.split(r'\s+',node.className)
          t += '.' + '.'.join(classes)
      elif nodeType==3:
        t += 'text("' + escapeStr(toString(node.nodeValue)) + '")'
      elif nodeType==7:
        t += 'processing-instruction(' + node.nodeName+'="' + escapeStr(toString(node.nodeValue)) + '")'
      elif nodeType==8:
        t += 'comment("' + escapeStr(node.nodeValue) + '")'
      elif nodeType==9:
        t += 'document()'
      else:
        t += 'unknown'
      detail.append(t)
  
  return ExtDict({'status':'NG','detail':' '.join(detail)})

def test():
  global document,options,DEFAULT_TESTDIR,url_data
  
  def nodesStr(nodes):
    def tagstr(node):
      try:
        strs=['<'+node.name]
        i=node.get('id')
        c=node.get('class')
        if i:
          strs.append('id='+i)
        if c:
          strs.append('class='+c)
        return escapeStr(' '.join(strs)+'>')
      except:
        return escapeStr(unicode(node))
    
    if isinstance(nodes,list):
      return ' '.join([tagstr(node) for node in nodes])
    elif getattr(nodes,'nodeType',None) or isinstance(nodes,basestring):
      return escapeStr(unicode(nodes))
    else:
      return nodes
  
  if options.web:
    fp=urllib2.urlopen(url_data)
    dirdoc=BSXPathEvaluator(fp.read())
    files=map(lambda node:node.get('href'),dirdoc.getItemList('//li/a[@href!="../"]'))
  else:
    if options.path:
      testdir=options.path
    else:
      testdir=DEFAULT_TESTDIR
    files=os.listdir(testdir)
  
  tnames=','.join(options.names).split(',') if options.names else None
  tnumbers=','.join(options.numbers).split(',') if options.numbers else None
  for name in files:
    if tnames:
      fname=re.sub(r'\..*$','',name)
      if not fname in tnames: continue
    target=url_data+'/'+name if options.web else os.path.join(testdir,name)
    data=parseTestData(target,options.web)
    print '[%s]\n%s\n' % (name,data.comment)
    document=BSXPathEvaluator(data.html)
    context=document.evaluate(data.contextExpr,document,None,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,None).snapshotItem(0)
    tests=data.tests
    cnt=0
    for test in tests:
      cnt=cnt+1
      if tnumbers:
        if not str(cnt) in tnumbers: continue
      print u'No.%d' % cnt
      expr=test.expr
      print u'expr  : %s' % (expr)
      
      (nodes,time,resultType)=document.applyXPath(context,expr)
      
      print u'time  : %d.%06d sec' % (time.seconds,time.microseconds)
      print u'result: %s' % nodesStr(nodes)
      print u'expect: %s' % (test.data)
      
      judge=testNodes(nodes,test.data)
      
      print u'judge : %s (%s)' % (judge.status,judge.detail)
      print u''
    
    print u''
  
def getoptions():
  #parser=optparse.OptionParser(usage=u'%prog')
  parser=optparse.OptionParser()
  parser.add_option(
    '-t','--test'
  , action='append'
  , metavar='<name>'
  , help=u'name: test name'
  , dest='names'
  )
  parser.add_option(
    '-n','--number'
  , action='append'
  , metavar='<number>'
  , help=u'number: test number'
  , dest='numbers'
  )
  parser.add_option(
    '-p','--path'
  , action='store'
  , metavar='<path>'
  , help=u'path: path of test file directory'
  , dest='path'
  )
  parser.add_option(
    '-w','--webdata'
  , action='store_true'
  , help=u'use data on web (%s)' % (url_data)
  , dest='web'
  )
  parser.add_option(
    '-d','--debug'
  , action='store_true'
  , help=u'use pdb'
  , dest='debug'
  )
  return parser.parse_args()

if __name__ == '__main__':
  
  (options,args)=getoptions()
  
  if options.debug:
    pdb.run('test()')
  else:
    test()


#■ End of TEST_BSXPath.py 
