#!/usr/bin/env python
"""\
HG changeset patch to git patch converter.

USAGE: hg-export-to-git-patch.py < hg.patch > git.patch
"""

from email.utils import parsedate_tz, mktime_tz
import re
from datetime import date, datetime, tzinfo, timedelta

def hg_patch_to_git(fin, fout):

    subject_re = re.compile(r'^(RE:)?\s*(\[[^]]*\])?\s*', re.I)

    # headers
    for line in fin:
        if line.startswith('# User '):
            fout.write('From: %s' % line[7:])
        elif line.startswith('# Date '):

            # I have no idea what I'm doing with timezones here...
            (unixtimestamp_string, timezone_string) = line[7:].split()
            class zone(tzinfo):
                def __init__(self, offset):
                    self.offset = timedelta(seconds=offset)
                def utcoffset(self, d):
                    return self.offset
                def dst(self, d):
                    return timedelta(0)
            t = datetime.fromtimestamp(int(unixtimestamp_string), zone(-int(timezone_string)))
            fout.write('Date: %s\n' % (t.strftime("%a, %d %b %Y %H:%M:%S %z")))
        elif line.startswith('#'):
            pass
        else:
            fout.write('Subject: %s' % (line))
            break
        #elif line.startswith('Subject: '):
        #    subject = subject_re.sub('', line[9:])
        #    fout.write(subject + '\n')
        #elif line == '\n' or line == '\r\n':
        #    break

    # commit message
    for line in fin:
        if line == '---\n':
            break
        fout.write(line)

    # skip over the diffstat
    for line in fin:
        if line.startswith('diff --git'):
            fout.write('\n' + line)
            break

    # diff
    # NOTE: there will still be an index line after each diff --git, but it
    # will be ignored
    for line in fin:
        fout.write(line)

    # NOTE: the --/version will still be at the end, but it will be ignored

if __name__ == "__main__":
    import sys
    hg_patch_to_git(sys.stdin, sys.stdout)


__author__ = "Mark Lodato <lodatom@gmail.com>"

__license__ = """
This is the MIT license: http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2009 Mark Lodato

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
