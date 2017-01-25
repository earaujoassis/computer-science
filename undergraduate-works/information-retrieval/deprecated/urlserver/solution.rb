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

require 'policy'

class UrlResource < Resource::Base
    def create request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.post?
        request.params.key? :url ? url = request.params[:url] : url = nil
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        return :response => "URI missing", :status => 406 if url.nil?
        return :response => "URI missing", :status => 406 if url.empty?
        return :response => "URI alredy fetched", :status => 304 if Policy::Maker.fetched? url
        return :response => "URI alredy pooled", :status => 304 if Policy::Maker.isknown? url
        return :response => "URI not allowed", :status => 304 if Policy::Maker.allowed? url
        Policy::Maker.insert(url)
        return :response => "URI successfully pooled", :status => 200
    end

    def list request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.get?
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        return :list => Policy::Maker.resources, :template => 'list', :status => 200
    end

    def unreached request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.get?
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        return :list => Policy::Maker.awaiting, :template => 'list', :status => 200
    end

    def choose request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.get?
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        url = Policy::Maker.pick
        return :list => [url], :template => 'list', :status => 200
    end

    def isknown request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.get?
        request.params.key? :url ? url = request.params[:url] : url = nil
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        return :response => "URI missing", :status => 406 if url.nil?
        return :response => "URI alredy known", :status => 200 if Policy::Maker.isknown? url
        return :response => "URI not known", :status => 404
    end

    def fetched request
        raise Http::Exceptions::MethodNotAllowed, "Method Not Allowed" unless request.put?
        request.params.key? :url ? url = request.params[:url] : url = nil
        request.params.key? :consumer_key ? consumer_key = request.params[:consumer_key] : consumer_key = nil
        # TODO Check if it's a valid consumer key
        request.params.key? :token ? token = request.params[:token]: token = nil
        # TODO Check if it's a valid token key
        return :response => "URI alredy fetched", :status => 304 if Policy::Maker.fetched? url
        return :response => "URI not known", :status => 404 if not Policy::Maker.isknown? url
        Policy::Maker.purge url
        return :response => "URI successfully fetched", :status => 200
    end
end

