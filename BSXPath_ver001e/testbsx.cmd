@echo off

SET TESTDIR="testbsxresult"

dir %TESTDIR% > nul 2>&1 || mkdir %TESTDIR%

echo "--- START"
for %%F in (0000 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012) do TEST_BSXPath.py -w -t %%F > %TESTDIR%\r%%F.txt
echo "--- END"

:END
