import sys
import subprocess

proc = subprocess.Popen(['python', 'script2.py',  'arg1 arg2 arg3 arg4'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print proc.communicate()[0]
