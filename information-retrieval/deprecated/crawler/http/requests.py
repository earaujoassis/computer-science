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

from crawler.http import HttpRequest

class HttpRequestGet(HttpRequest):
    def __init__(self, host='', path='', content=''):
        super(HttpRequestGet, self).__init__(content=content)
        self._method = 'GET'
        self.__setitem__('Method', self.method)
        self.__setitem__('Request-URI', path)
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Host', host)
        self._mock_query = dict()
        self._path = str()

    def set(self, key, value):
        return self.__setitem__(key, value)

    def query(self, key, value):
        self._mock_query[key] = value
        self._reset_path()

    def _reset_path(self):
        path = str()
        for key, value in self._mock_query.items():
            query = "{0}={1}".format(key, value)
            if len(path) > 0: query = "&{0}".format(query)
            path = path + query
        self._path = '?{0}'.format(path)

    def writable(self):
        uri_original = self._header['Request-URI']
        self._header['Request-URI'] = uri_original + self._path
        result = super(HttpRequestGet, self).writable()
        self._header['Request-URI'] = uri_original
        return result

class HttpRequestGetHtml(HttpRequestGet):
    def __init__(self, user_agent, host='', path='', content=''):
        super(HttpRequestGetHtml, self).__init__(host, path, content)
        self.set("User-Agent", user_agent)
        self.set("Accept", "text/html,application/xhtml+xml,application/xml")
        self.set("Accept-Charset", "ISO-8859-1,utf-8")

class HttpRequestPost(HttpRequest):
    def __init__(self, host='', path='', content=''):
        super(HttpRequestPost, self).__init__(content=content)
        self._method = 'POST'
        self.__setitem__('Method', self.method)
        self.__setitem__('Request-URI', path)
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Host', host)
        self._mock_content = dict()

    def set(self, key, value):
        return self.__setitem__(key, value)

    def store(self, key, value):
        self._mock_content[key] = value
        self._reset_content()

    def _reset_content(self):
        content = str()
        for key, value in self._mock_content.items():
            query = "{0}={1}".format(key, value)
            if len(content) > 0: query = "&{0}".format(query)
            content = content + query
        self._content = content

class HttpRequestPut(HttpRequestPost):
    def __init__(self, host='', path='', content=''):
        super(HttpRequestPut, self).__init__(host=host, path=path, content=content)
        self._method = 'PUT'
        self.__setitem__('Method', self.method)

