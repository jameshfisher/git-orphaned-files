#!/usr/bin/env python

import os
import subprocess
import sys

commit = sys.argv[1]

devnull = open(os.devnull, 'wb')

note = subprocess.Popen(["git", "notes", "--ref=orphans", "show", commit], stdout=subprocess.PIPE, stderr=devnull)
out, err = note.communicate()

if note.returncode != 0:
    note_add = subprocess.Popen(["git", "notes", "--ref=orphans", "add", "-F", "-", commit], stdin=subprocess.PIPE)
    orphans = subprocess.check_output(["git-orphans", commit])
    note_add.communicate("orphans:\n" + orphans)
    print orphans
else:
    print out[9:]
