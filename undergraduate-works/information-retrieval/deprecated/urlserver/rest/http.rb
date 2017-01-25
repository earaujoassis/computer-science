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

module Http
    module Exceptions
        class BadHeaderError < RuntimeError
        end

        class MethodNotAllowed < RuntimeError
        end
    end

    Methods = [:OPTIONS,:GET,:HEAD,:POST,:PUT,:DELETE,:TRACE,:CONNECT]
    Methods.freeze
    ReasonPhrase = {
        200 => 'OK',
        201 => 'Created',
        202 => 'Accepted',
        203 => 'Non-Authoritative Information',
        204 => 'No Content',
        205 => 'Reset Content',
        206 => 'Partial Content',
        300 => 'Multiple Choices',
        301 => 'Moved Permanently',
        302 => 'Found',
        303 => 'See Other',
        304 => 'Not Modified',
        305 => 'Use Proxy',
        306 => 'Switch Proxy',
        307 => 'Temporary Redirect',
        400 => 'Bad Request',
        401 => 'Unauthorized',
        403 => 'Forbidden',
        404 => 'Not Found',
        405 => 'Method Not Allowed',
        406 => 'Not Acceptable',
        407 => 'Proxy Authentication Required',
        408 => 'Request Timeout',
        409 => 'Conflict',
        410 => 'Gone',
        411 => 'Length Required',
        412 => 'Precondition Failed',
        413 => 'Request Entity Too Large',
        414 => 'Request-URI Too Long',
        415 => 'Unsupported Media Type',
        500 => 'Internal Server Error',
        501 => 'Not Implemented',
        502 => 'Bad Gateway',
        503 => 'Service Unavailable'
    }
    ReasonPhrase.freeze

    class HttpRequest
        attr_reader :header, :content, :method
        def initialize complete='', header={}, content=''
            @complete, @header, @content = complete, header, content
            @method = String.new
            @params = nil
            return process
        end

        def writable
            if not @complete.nil? or not @complete.empty? and @header.empty? and @content.empty?
                return @complete
            end
            fields = Array.new
            header = @header.dup
            request_line = "#{header.delete('Method')} #{header.delete('Request-URI')} #{header.delete('HTTP-Version')}"
            header.each_pair do |key, value|
                begin
                    if value.length > 1 and value.instance_of? Array
                        value = value.join('; ')
                    end
                rescue NoMethodError
                end
                field = "#{key}: #{value}"
                fields << field
            end
            if fields.length < 0
                return "#{request_line}\r\n\r\n#{@content}"
            end
            header = fields.join("\r\n")
            return "#{request_line}\r\n#{header}\r\n\r\n#{@content}"
        end

        def params
            if @params.nil?
                @params = Hash.new
                uri = @header['Request-URI']
                if uri.include? "?"
                    index_up = uri.index('?')
                    index_down = uri.index('#')
                    uri = uri[index_up+1..index_down] unless index_down.nil?
                    uri = uri[index_up+1..-1] if index_down.nil?
                    uri = uri.split('&') unless uri.nil?
                    uri = uri.split(';') unless uri.kind_of? Array
                    if uri.kind_of? Array
                        uri.each do |query|
                            key, value = query.split('=')
                            @params.store(key.intern, value)
                        end
                    end
                end
                if (self.post? or self.put?) and not @content.empty?
                    content = @content.dup
                    content = content.split('&')
                    content = content.split(';') unless content.kind_of? Array
                    if content.kind_of? Array
                        content.each do |query|
                            key, value = query.split('=')
                            @params.store(key.intern, value)
                        end
                    end
                end
            end
            @params
        end

        private
        def process
            if @complete.nil? or @complete.empty?
                return self
            end
            header, @content = @complete.split(/\r\n\r\n/, 2)
            header = header.split(/\r\n/)
            header_dict = Hash.new
            header_dict['Method'], header_dict['Request-URI'], header_dict['HTTP-Version'] = header.delete_at(0).split(/ /)
            @method = header_dict['Method']
            method_questions
            header.each do |field|
                index = field.index(':')
                key = field[0..index-1]
                field[0..index+1] = ''
                if field.include? ';'
                    fields = field.split('; ')
                    value = fields
                else
                    value = field
                end
                header_dict[key] = value
            end
            @header = header_dict
            @header.freeze
            return self
        end

        def method_questions
            return if @method.empty?
            standard = @method.downcase
            Http::Methods.each do |method|
                method = method.to_s.downcase
                value = method == standard
                block = lambda { value }
                self.class.send(:define_method, "#{method}?", block)
            end
        end
    end

    class HttpResponse
        attr_reader :header, :content, :status_code
        def initialize complete='', header={}, content=''
            @complete, @header, @content = complete, header, content
            @status_code = 0
            return process
        end

        def writable
            if not @complete.nil? or not @complete.empty? and @header.empty? and @content.empty?
                return @complete
            end
            fields = Array.new
            header = @header.dup
            status_line = "#{header.delete('HTTP-Version')} #{header.delete('Status-Code')} #{header.delete('Reason-Phrase')}"
            header.each_pair do |key, value|
                begin
                    if value.length > 1 and value.instance_of? Array
                        value = value.join('; ')
                    end
                rescue NoMethodError
                end
                field = "#{key}: #{value}"
                fields << field
            end
            if fields.length < 0
                return "#{status_line}\r\n\r\n#{@content}"
            end
            header = fields.join("\r\n")
            return "#{status_line}\r\n#{header}\r\n\r\n#{@content}"
        end

        private
        def process
            if @complete.nil? or @complete.empty?
                return self
            end
            header, @content = @complete.split(/\r\n\r\n/, 2)
            header = header.split(/\r\n/)
            header_dict = Hash.new
            status_line = header.delete_at(0).split(' ')
            if status_line.length > 3
                status_line[2] = status_line[2..-1].join(' ')
                status_line[3..-1] = nil
            end
            header_dict['HTTP-Version'], header_dict['Status-Code'], header_dict['Reason-Phrase'] = status_line
            @status_code = header_dict['Status-Code'].to_i
            header.each do |field|
                index = field.index(':')
                key = field[0..index-1]
                field[0..index+1] = ''
                if field.include? ';'
                    fields = field.split('; ')
                    value = fields
                else
                    value = field
                end
                header_dict[key] = value
            end
            @header = header_dict
            @header.freeze
            return self
        end
    end

    class HttpResponseOK < HttpResponse
        def initialize complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 200
            unless @header.nil?
                @header = @header.dup
                @header.store('Reason-Phrase', 'OK')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.freeze
            end
            self
        end
    end

    class HttpResponsePermanentRedirect < HttpResponse
        def initialize redirect_to, complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 301
            unless @header.nil?
                @header = @header.dup
                # TODO Process redirect_to to make it an uri
                @header.store('Reason-Phrase', 'Bad Request')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.store('Location', redirect_to)
                @header.freeze
            end
            self
        end
    end

    class HttpResponseRedirect < HttpResponse
        def initialize redirect_to, complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 302
            unless @header.nil?
                @header = @header.dup
                # TODO Process redirect_to to make it an uri
                @header.store('Reason-Phrase', 'Bad Request')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.store('Location', redirect_to)
                @header.freeze
            end
            self
        end
    end

    class HttpResponseBadRequest < HttpResponse
        def initialize complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 400
            unless @header.nil?
                @header = @header.dup
                @header.store('Reason-Phrase', 'Bad Request')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.freeze
            end
            self
        end
    end

    class HttpResponseNotFound < HttpResponse
        def initialize complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 404
            unless @header.nil?
                @header = @header.dup
                @header.store('Reason-Phrase', 'Not Found')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.freeze
            end
            self
        end
    end

    class HttpResponseMethodNotAllowed < HttpResponse
        def initialize complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 405
            unless @header.nil?
                @header = @header.dup
                @header.store('Reason-Phrase', 'Method Not Allowed')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.freeze
            end
            self
        end
    end

    class HttpResponseInternalServerError < HttpResponse
        def initialize complete='', header={}, content=''
            super(complete, header, content)
            @status_code = 500
            unless @header.nil?
                @header = @header.dup
                @header.store('Reason-Phrase', 'Internal Server Error')                
                @header.store('HTTP-Version', 'HTTP/1.1')
                @header.store('Status-Code', @status_code)
                @header.freeze
            end
            self
        end
    end
end

