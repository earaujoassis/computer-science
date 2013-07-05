#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright 2013 Ewerton Assis.
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

import os
import sys
import threading
import subprocess
import signal
import argparse
import time

class TColors(object):
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

  def disable (self):
    self.HEADER, self.OKBLUE, self.OKGREEN, \
      self.WARNING, self.FAIL, self.ENDC = ''

class Test(object):
  PASS, FAIL = 0, 1

class ProcessThread(threading.Thread):
  def __init__(self, run, daemon=False):
    super(ProcessThread, self).__init__()
    self.stdout = None
    self.stderr = None
    self.target = run
    self.daemon = daemon
    self.subprocess = None

  def run(self):
    self.subprocess = subprocess.Popen(self.target, shell=False, \
      stdout=sys.stdout, stderr=sys.stderr)
    self.stdout, self.stderr = self.subprocess.communicate()

def main (args):
  if args.solution == "java-rmi":
    print ("{}{}{}{}\t{}".format("[", TColors.OKGREEN, "Now testing the Java RMI solution", TColors.ENDC, "]"))
    server = ProcessThread(run='java -cp ./cls UpperServer'.split(), daemon=True)
    client = ProcessThread(run='java -cp ./cls UpperApp'.split())
    server.start()
    time.sleep(2)
    client.start()
    client.join()
    server.subprocess.terminate()
    server.subprocess.kill()
  if args.solution == "py-crbc":
    print ("{}{}{}{}\t{}".format("[", TColors.OKGREEN, "Now testing the Python CRBC solution", TColors.ENDC, "]"))
    sys.path.append('./src/python')
    registry = ProcessThread(run='python src/python/stub-registry.py'.split(), daemon=True)
    server = ProcessThread(run='python src/python/stub-server.py'.split(), daemon=True)
    client = ProcessThread(run='python src/python/stub-client.py'.split())
    registry.start()
    time.sleep(3)
    server.start()
    time.sleep(3)
    client.start()
    client.join()
    server.subprocess.terminate()
    server.subprocess.kill()
    registry.subprocess.terminate()
    registry.subprocess.kill()
  os._exit(0)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Test distributed-servers builds')
  parser.add_argument('solution', choices=['java-rmi', 'py-crbc'], help='run either the Java RMI or the Python CRBC solution')
  args = parser.parse_args()
  try:
    main(args)
  except:
    print("Did you execute 'make build' first?")
#    import traceback
#    traceback.print_exc()
