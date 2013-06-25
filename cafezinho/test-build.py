#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright 2013 Ewerton Assis.
#
# Use intended for the course of Compilers under the Computer Science
# undergraduate program at the Universidade Federal de Goias, Brazil.
# UFG Enrollment: 060194.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys, subprocess, json

class TColors(object):
  HEADER = '\033[95m'; OKBLUE = '\033[94m'; OKGREEN = '\033[92m'; WARNING = '\033[93m'; FAIL = '\033[91m'; ENDC = '\033[0m'

  def disable (self):
    self.HEADER, self.OKBLUE, self.OKGREEN, self.WARNING, self.FAIL, self.ENDC = ''

class Test(object):
  PASS, FAIL = 0, 1

def main (argv):
  if not os.path.isfile ('./cafezinho'):
    print ("{0}{1}{2}".format (TColors.FAIL, "Error: you must build the cafezinho compiler (make build)", TColors.ENDC))
    exit (1)
  if not os.path.isfile ('tests/descriptor.json'):
    print ("{0}{1}{2}".format (TColors.FAIL, "Error: tests/descriptor.json file is missing", TColors.ENDC))
    exit (1)
  descriptor = open ("tests/descriptor.json")
  tests = json.load (descriptor)
  descriptor.close ()
  arguments = [ './cafezinho', None ]
  FNULL = open (os.devnull, 'w')
  for test in tests:
    arguments[1] = test['file']
    return_code = subprocess.call (arguments, stdout=FNULL, stderr=subprocess.STDOUT, shell=False)
    if (return_code == test['status']):
      print ("{0}{1}{2}{3}\t{4}{5}{6}".format ("[", TColors.OKGREEN, "OK", TColors.ENDC, "]", " for ", test['file']))
    else:  
      print ("{0}{1}{2}{3}\t{4}{5}{6}{7}{8}".format ("[", TColors.FAIL, "ERROR", TColors.ENDC, "]", " for ", test['file'], ": ", test['unexpected']))
  FNULL.close ()


if __name__ == '__main__':
  main (sys.argv)
