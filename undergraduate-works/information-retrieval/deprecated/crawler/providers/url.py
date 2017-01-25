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

import xml.dom.minidom
from crawler.connection import USER_AGENT
from crawler.connection.support import send_request
from crawler.providers.base import Provider, NoContentError
from crawler.http.requests import HttpRequestGet, HttpRequestPost, HttpRequestPut
from crawler.http import HttpResponse

class UrlProviderClient(Provider):
    def __init__(self, host='localhost', port=8080):
        super(UrlProviderClient, self).__init__(host, port)

    def __process(self, response):
        if response == None or getattr(response, 'status_code', 404) != 200:
            # TODO Certificate that client classes are handling this exception
            raise NoContentError("There's no content to show")
        uris = list()
        try:
            dom = xml.dom.minidom.parseString(response.content)
            for uri in dom.getElementsByTagName('uri'):
                uris.append(uri.firstChild.data)
            return tuple(uris)
        except:
            return tuple()

    def list(self, limit=10):
        request = HttpRequestGet(host=self.host, path='/url/list')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.query("consumer_key", "none")
        request.query("limit", limit)
        response = send_request(request.writable(), self.ip, self.port)
        return self.__process(response)

    def unreached(self, limit=10):
        request = HttpRequestGet(host=self.host, path='/url/unreached')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.query("consumer_key", "none")
        request.query("limit", limit)
        response = send_request(request.writable(), self.ip, self.port)
        return self.__process(response)

    def choose(self, limit=10):
        request = HttpRequestGet(host=self.host, path='/url/choose')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.query("consumer_key", "none")
        response = send_request(request.writable(), self.ip, self.port)
        return self.__process(response)

    def create(self, url):
        request = HttpRequestPost(host=self.host, path='/url/create')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.store("url", url)
        request.store("consumer_key", "none")
        return send_request(request.writable(), self.ip, self.port)

    def fetched(self, url):
        request = HttpRequestPut(host=self.host, path='/url/fetched')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.store("url", url)
        request.store("consumer_key", "none")
        request.store("token", "none")
        return send_request(request.writable(), self.ip, self.port)

    def isknown(self, url):
        request = HttpRequestGet(host=self.host, path='/url/isknown')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "application/xml;text/xml")
        request.set("Accept-Charset", "utf-8")
        request.query("url", url)
        request.query("consumer_key", "none")
        return send_request(request.writable(), self.ip, self.port)

    def close(self):
        return True

