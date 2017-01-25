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

module Processors
    class HttpResponseConstructor < Http::HttpResponse
        attr_accessor :status_line, :header, :content
        def initialize
            super()
            @header = @header.dup
            @header.store('HTTP-Version', 'HTTP/1.1')
        end

        def status_code= value
            @status_code = value
            @header.store('Status-Code', value)
            @header.store('Reason-Phrase', Http::ReasonPhrase[value])
        end

        def content= value
            @content = value
        end
    end

    class HttpResponseCodedConstructor < HttpResponseConstructor
        def initialize status_code
            super()
            @header = @header.dup
            @header.store('HTTP-Version', 'HTTP/1.1')
            @status_code = status_code
            @header.store('Status-Code', @status_code)
            @header.store('Reason-Phrase', Http::ReasonPhrase[@status_code])
        end
    end

    class ReponseProcessor
        def initialize request
            @request, @response = request, nil
        end

        def response
            return @response unless @response.nil?
            begin
                uri = @request.header['Request-URI']
                uri = uri.slice(0,uri.index('?')) if uri.include? '?'
                controller = Routes::Routing.controller_for uri
                instance = Kernel.const_get(controller[:class]).new
                method = instance.method(controller[:method])
                result = method.call @request
                @response = Processors::HttpResponseConstructor.new
                (result.key? :status) ? @response.status_code = result[:status] : @response.status_code = 200
                unless result.key? :template
                    file = case (@response.status_code/100)
                        when 4 then "#{ServerPath}/rest/template/error.xml"
                        when 5 then "#{ServerPath}/rest/template/error.xml"
                        else "#{ServerPath}/rest/template/response.xml"
                    end
                else
                    file = "#{ServerPath}/rest/template/#{result[:template]}.xml"
                end
                template = Template::ProcessContext.new file
                processed_content = template.process result
                @response.header.store('Content-Type', ['text/xml', 'charset=utf-8'])
                @response.header.store('Content-Length', template.size)
                @response.content = processed_content
            rescue Routes::Exceptions::RouteNotFound => error
                return process_response_error error, 404
            rescue Http::Exceptions::BadHeaderError => error
                return process_response_error error, 400
            rescue Http::Exceptions::MethodNotAllowed => error
                return process_response_error error, 405
            rescue => error
                puts "#{error.class}: #{error.message}"
                puts error.backtrace.join("\n")
                return process_response_error error, 500
            end
            return @response
        end

        private
        def process_response_error exception, status_code
            response = Processors::HttpResponseCodedConstructor.new status_code
            response.header.store('Content-Type', ['text/html', 'charset=utf-8'])
            template = Template::ProcessContext.new "#{ServerPath}/rest/template/#{status_code}.html"
            response.content = template.process nil
            response.header.store('Content-Length', template.size)
            return response
        end
    end
end

