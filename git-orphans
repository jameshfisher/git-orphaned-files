#!/usr/bin/env python

import os
import subprocess
import shutil
import sys
import tempfile

commit = sys.argv[1]

devnull = open(os.devnull, 'wb')

temp_directory_path = tempfile.mkdtemp(suffix='git-orphans');
subprocess.check_call(["git", "clone", "--recurse-submodules", ".", temp_directory_path], stdout=devnull, stderr=devnull)
# subprocess.check_call(["git", "fetch", "origin", commit], cwd=temp_directory_path, stdout=devnull, stderr=devnull)
subprocess.check_call(["git", "checkout", commit], cwd=temp_directory_path, stdout=devnull, stderr=devnull)

orphans = set(subprocess.Popen(["orphans", "./build.sh"], stdout=subprocess.PIPE, cwd=temp_directory_path).stdout)
git_files = set(subprocess.Popen(["git", "ls-files", "--with-tree=" + commit], stdout=subprocess.PIPE, cwd=temp_directory_path).stdout)

shutil.rmtree(temp_directory_path)

for f in (orphans & git_files):
  print f.strip()
