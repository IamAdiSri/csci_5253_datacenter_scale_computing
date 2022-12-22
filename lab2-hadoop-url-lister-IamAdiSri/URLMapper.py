#!/usr/bin/env python
"""mapper.py"""

import sys
import re

def get_urls(string):
	regex = 'href=".*?"'
	urls = re.findall(regex,string)
	urls = [url.split('"')[-2] for url in urls]
	return urls

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    # extract urls from line
    urls = get_urls(line)
    
    # increase counters
    for url in urls:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print('%s\t%s' % (url, 1))
