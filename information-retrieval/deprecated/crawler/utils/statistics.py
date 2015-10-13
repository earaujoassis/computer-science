# -*- coding: utf-8 -*-

# Copyright 2011 Éwerton Assis
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

import sys

class StatsStatusCode(object):
    def __init__(self, status_code=(200, 301, 302, 404, 500), save=False):
        self.status_code = status_code
        for number in status_code:
            setattr(self, str(number), 0)
        if save:
            self.file = open("stats", "w")

    def compute(self, status_code):
        if status_code in self.status_code:
            new_value = (getattr(self, str(status_code))) + 1
            setattr(self, str(status_code), new_value)

    def __del__(self):
        msg = str(" ").join(["{0}: {1}".format(number, getattr(self, str(number))) for number in self.status_code])
        if hasattr(self, "file"):
            self.file.write("{0}\n".format(msg))
            self.file.close()
        else:
            sys.stdout.write("{0}\n".format(msg))

