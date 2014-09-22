#!/usr/bin/env python

import subprocess
import sys
import time

start_time_unix = int(subprocess.check_output(['date', '+%s']).strip())

time.sleep(1)  # atime has a one-second resolution

subprocess.call(sys.argv[1:])

find = subprocess.Popen(["find", "."], stdout = subprocess.PIPE)

while line = find.stdout.readline():
  line = find.stdout.readline()
  if line == '':
    break
  else:
    filepath = line.strip()
    atime_unix = int(subprocess.check_output(["stat", "-f", "%a", filepath]).strip())
    if atime_unix <= start_time_unix:
        print filepath
