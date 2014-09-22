#!/usr/bin/env python

import string
import subprocess
import sys

def orphans_of_commit(commit):
  return set([s.strip() for s in subprocess.Popen(["git-orphans-cache", commit], stdout=subprocess.PIPE).stdout])

def parents_of_commit(commit):
  return list(subprocess.Popen(["git", "rev-list", "--parents", "--max-count=1", commit], stdout=subprocess.PIPE).stdout)[0].strip().split(" ")[1:]

commit = sys.argv[1]

orphans = orphans_of_commit(commit)

for parent in parents_of_commit(commit):
  orphans -= orphans_of_commit(parent)

for orphan in orphans:
  print orphan
