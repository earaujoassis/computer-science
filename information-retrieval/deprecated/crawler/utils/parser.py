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

import re
from crawler.connection import normalize_url

anchor_pattern = "href=[\"\']?(?P<path>[A-Za-z0-9.#?=&\///:+_]*)[\"\']?"

class ParseHtmlAnchors(object):
    def __init__(self, document, context=''):
        self.context = context
        self.document = document
        self.__process()

    def __process(self):
        pattern = re.compile(anchor_pattern, re.IGNORECASE)
        self.raw_anchors = pattern.findall(self.document)
        del self.document

    def __get_anchors(self):
        if not hasattr(self, '__anchors'):
            if not self.context:
                self.__anchors = self.raw_anchors
            else:
                self.__anchors = list()
                for anchor in self.raw_anchors:
                    if anchor.startswith('http://') or anchor.startswith('https://'):
                        self.__anchors.append(anchor)
                        continue
                    if '../' in anchor:
                        # TODO Process relative anchor and continue
                        continue
                    if anchor.startswith('/'):
                        uri_scheme, authority, port, path = normalize_url(self.context)
                        anchor = "{0}{1}{2}".format(uri_scheme, authority, anchor)
                        self.__anchors.append(anchor)
                        continue
                    if not anchor.startswith('/'):
                        uri_scheme, authority, port, path = normalize_url(self.context)
                        pieces = path[1:].split('/'); pieces.pop()
                        if len(pieces) > 0: path = '/'.join(pieces)
                        if len(pieces) > 1: path += '/'
                        else: path = ''
                        anchor = "{0}{1}/{2}{3}".format(uri_scheme, authority, path, anchor)
                        self.__anchors.append(anchor)
                        continue
        return self.__anchors
    anchors = property(__get_anchors)

