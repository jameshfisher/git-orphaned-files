# git orphaned-files

How many old files in your repository could be removed without breaking
anything? A significant number, if your repository is non-trivial. **Humans
are terrible at garbage collection**, because orphaning doesn’t break test
suites and doesn’t show up in code review. But how about if your CI process
was able to tell you:

> This commit might have orphaned these files:
> 
> * `/src/server/baz.py`
> * `/src/client/baz.js`

This kind of warning guards against two kinds of failure:

* **Accidental orphaning.** You did not intend to remove the ‘baz’ feature.
  (This error should also be picked up by your test suite.)
* Deliberate orphaning, but **accidental failure to remove the orphan.** You
  retired the ‘baz’ feature, but forgot to remove its implementation. (This
  error is more insidious.)

How might we implement this? Here’s a simple heuristic: **if a file is never
accessed during your build process or during your tests, then it’s probably
orphaned.**

There will be false positives, like `README` files. There will also be false
negatives, like compilers following `import foo.*` instructions. **There will
be errors, but errors are in the nature of the heuristic.** A similar
heuristic we use is ‘code coverage’. We also use ‘linting’ tools which are
useful but sometimes wrong.

In any case, the absolute list of orphaned files is not too important. The
real usefulness is the **difference in the orphan list between commits.** In
each warning, we list each orphan in the current commit which was not an
orphan in the parent commits.

One nice thing about this check is that **the developer does not have to do
anything.** The heuristic just exploits the build process and test suites that
the developer already writes. All the developer does is **tick the check-box:
☑ report orphaned files**.

Another nice thing is that **this check is language-agnostic.** Yes, your
static analyser can give you more accurate dead code warnings. But we leave in
a complex polyglot world where such tools either don’t exist or are too
expensive or too much pain to set up.

## Implementation

So, after running our build and test suite, the unaccessed files should be
marked as dead. **But how can we detect file accesses?** On UNIX, each file
has an **‘atime’ attribute,** which records the latest time the file was
accessed. Lots of operating systems disable the atime feature by default, but
we can simply turn it on by using the strictatime mount option.

As a first pass, I want a standalone command-line tool. I pass it arguments
that run the build and tests. It takes note of the time, runs the build and
tests, then prints out a list of all files with an atime less than the start
time. Thus:

    > orphans make
    README
    BUGS
    src/baz.py
    src/baz.js

A bash program for this is actually very short:

    #!/bin/bash
    start_time=`date +%s`;
    "$@" &> /dev/null;
    for filepath in `find .`; do
      atime=`stat -f %a $filepath`;
      if [ "$atime" -lt "$start_time" ]
      then
        echo "$filepath";
      fi
    done

Now I want a program which knows about git and build/test, and can give me the
orphan list for a given commit. Let’s say the repository has a `./build.sh`
script checked in which builds the project and runs its tests.
