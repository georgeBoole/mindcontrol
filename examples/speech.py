#!/usr/bin/env python
# encoding: utf-8
"""
speech.py

Created by Michael Sobczak on 2012-07-18.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

import pyttsx
import code


def _build_say():
	engine = pyttsx.init()
	def say_func(message):
		engine.say(message)
		engine.runAndWait()
	return say_func
	
say = _build_say()





def speak_trace(func):
	def inner_func(args):
		arg_str = str(args)
		try:
			arg_str =  ','.join([str(x) for x in args])
		except:
			pass
		say('Entering function named %s. arguments are %s' % (func.__name__,arg_str))
		res = func(args)
		say('Finished executing %s. Result is %s' % (func.__name__, res))
		return res
	return inner_func

#
#engine = pyttsx.init()
#voices = engine.getProperty('voices')
#for voice in voices:
#   if voice.name == 'Vicki':
#       engine.setProperty('voice', voice.id)
#       print voice
#       engine.say('The quick brown fox jumped over the lazy dog.')
#       break
#engine.runAndWait()
#code.interact(local=locals())