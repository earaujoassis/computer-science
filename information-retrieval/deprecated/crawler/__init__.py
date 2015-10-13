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

from threading import Thread, Lock
from crawler.http import HttpResponse
from crawler.utils.limited import List
from crawler.utils.parser import ParseHtmlAnchors
from crawler.connection import FetchingContext, FullOfWork, NotSupported, Unreachable
from crawler.providers import NoContentError
from crawler.utils.statistics import StatsStatusCode

class Crawler(object):
    def __init__(self, url_provider, storage_server=None):
        self.url_provider = url_provider
        self.storage_server = storage_server
        self.urls_pool = List(100)
        self.fetching_context = FetchingContext()

        self.stats = StatsStatusCode()

    def push(self, url):
        self.urls_pool.append(url)

    def start(self):
        self.fetching = True
        while self.fetching:
            if not self.urls_pool:
                # TODO Load urls from an stored filesystem
                try:
                    # Call for urls in the url server
                    anchors = self.url_provider.choose()
                except NoContentError:
                    anchors = list()
                for uri in anchors:
                    self.urls_pool.append(uri)
                del anchors
                # If it still haven't got any url, there's nothing to crawl/fetch
                if not self.urls_pool:
                    break
            if len(self.urls_pool) > 0:
                try:
                    anchor = self.urls_pool.pop(0)
                    self.fetching_context.fetch_page(anchor)
                except FullOfWork:
                    self.url_provider.create(anchor)
                except Unreachable:
                    pass
                except NotSupported:
                    pass
                del anchor
            received_data = self.fetching_context.received_data()
            for data in received_data:
                response = self.url_provider.fetched(data[0])
                # If the URL was alredy fetched, don't process the page data
                if response.status_code == 304:
                    continue
                # Send data to be "processed" by the HttpResponse
                response = HttpResponse(data[1])
                import sys
                sys.stdout.write("{0}: {1}\n".format(data[0], response.status_code))
                self.stats.compute(response.status_code)
                # TODO Process response header (eg.: Location field, status code)
                parser = ParseHtmlAnchors(response.content, data[0])
                anchors = parser.anchors
                for anchor in anchors:
                    self.url_provider.create(anchor)
                # TODO Then, after all the data has been cleaned, send it to the data analysis
                del response, parser, anchors
            # TODO Send data analysed to storage server
            del received_data
        return self.stop()

    def stop(self):
        self.fetching = False

class CrawlerThread(Thread, Crawler):
    def __init__(self, url_provider, storage_server=None):
        Crawler.__init__(self, url_provider, storage_server)
        super(CrawlerThread, self).__init__() # It calls Thread.__init__(self)

    def start(self):
        Thread.start(self)
        Crawler.start(self)

    def run(self):
        Crawler.start(self)

