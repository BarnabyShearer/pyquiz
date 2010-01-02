#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 bWare. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Simple quiz buzzer handler.'''

__author__ = 'bWare@iWare.co.uk'
__version__ = '0.0.1b'
__metadata__ = dict(
	name="PyQuiz",
	version=__version__,
	description=__doc__,
	author=__author__[:__author__.find('@')],
	author_email=__author__,
	url="http://bware.iware.co.uk/pyquiz.py",
	classifiers=[
		__version__[-1]=='b'
				and
			'Development Status :: 4 - Beta'
				or
			'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		"Environment :: Handhelds/PDA's",
		'Intended Audience :: End Users/Desktop',
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Education :: Testing',
		'Topic :: Games/Entertainment :: Puzzle Games',
	]	
)

def setup():
	from distutils.core import setup
	setup(**__metadata__)

def main():
	from optparse import OptionParser

	parser = OptionParser()
	parser = OptionParser(version="%%prog %s" % __version__)
	parser = OptionParser(description=__metadata__['description'])
	parser.add_option(
		"-m","--mask",
		dest="mask",
		default='00001000010000100001',
		help=u"a bitwise mask of buttons to activate [default: %default (Buzz\u2122 top buzzers)]"
	)
	parser.add_option(
		"-w","--wait",
		dest="wait",
		default=5,
		type="int",
		help=u"timeout after a buzz [default: %default]"
	)
	parser.add_option(
		"-c","--config",
		dest="config",
		default="pyquiz.ini",
		help="file to load/save team/buzzer associations [default: %default]"
	)
	(opts,args) = parser.parse_args()

	import pygame
	import time
	import os

	pygame.init()

	#HACK: PyGame assumes it has a window, and without one can't quit.
	pygame.display.set_mode((200, 200))
	pygame.display.set_caption("%s %s" % (__metadata__['name'],__version__))

	teams = []

	for j in range(0, pygame.joystick.get_count()):
		joy = pygame.joystick.Joystick(j)
		joy.init()
		print 'Initialized Joystick %d: %s with %d buttons.' % (j,joy.get_name(),joy.get_numbuttons())
		if not os.path.exists(opts.config):
			#Create default teams
			group = {}
			coff = 0
			for char in opts.mask[::-1]:
				if char=='1':
					group[coff]=[
						'Team %02d%02d' % (joy.get_id(),coff),
						'%02d%02d.ogg' % (joy.get_id(),coff)
					]
				coff += 1
			teams.append(group)

	opts.mask = int(opts.mask,2)

	if os.path.exists(opts.config):
		import ConfigParser
		
		config = ConfigParser.ConfigParser()
		config.read(opts.config)
		teams = eval(config.get("PyQuiz","Teams"))
		
		print """=== Starting Quiz ===
"""
		for group in teams:
			for team in group:
				print "       Team: %s " % group[team][0]
				group[team][1] = pygame.mixer.Sound(group[team][1])
		print """"""
	
		try:
			while True:
				e = pygame.event.wait()
				if e.type == pygame.QUIT:
					raise SystemExit
				elif e.type == pygame.JOYBUTTONDOWN:
					b = 2**e.button & opts.mask
					if b>0:
						print teams[e.joy][e.button][0]
						teams[e.joy][e.button][1].play()
						time.sleep(opts.wait)
						pygame.event.clear()
		except SystemExit:
			pass
		except KeyboardInterrupt:
			pass
	else:
		print """=== Setup Teams ===
"""
		import ConfigParser

		try:
			while True:
				e = pygame.event.wait()
				if e.type == pygame.QUIT:
					raise SystemExit
				elif e.type == pygame.JOYBUTTONDOWN:
					b = 2**e.button & opts.mask
					if b>0:
						pygame.mixer.Sound(teams[e.joy][e.button][1]).play()
						t = raw_input("Enter Team Name: %s" % teams[e.joy][e.button][0])
						if t=='':
							pass
						elif t=='done':
							break
						else:
							teams[e.joy][e.button][0] = t
						pygame.event.clear()
		except SystemExit:
			pass
		except KeyboardInterrupt:
			pass

		config = ConfigParser.ConfigParser()
		config.add_section('PyQuiz')
		config.set('PyQuiz','Teams',teams)
		configfile = open(opts.config, 'wb')
		config.write(configfile)

	pygame.quit()		


if __name__ == "__main__":
	import sys
	if(sys.argv[0][-8:]=='setup.py'):
		setup()
	else:
		main()
