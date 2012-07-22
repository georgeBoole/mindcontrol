#!/usr/bin/env python
# encoding: utf-8
"""
test_speec.py

Created by Michael Sobczak on 2012-07-18.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

import sys
import os
from speech import speak_trace


@speak_trace
def add(stuff_to_add):
	return sum(stuff_to_add)

@speak_trace
def fibonacci(n):
	if n <= 1:
		return 1
	else:
		return fibonacci(n-1) + fibonacci(n-2)

def main():
	add([5,4,2,6,7])


if __name__ == '__main__':
	main()

	

