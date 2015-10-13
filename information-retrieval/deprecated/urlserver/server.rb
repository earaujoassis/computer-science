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

require 'rest'
require 'solution'
require 'config'
require 'socket'

ServerPath = File.expand_path('../',  __FILE__)

class Server
    def initialize host='localhost', port='8080', backlog=10
        @host, @port, @backlog = host, port, backlog
        @serving = false
    end

    def serve
        @server_socket = Socket.new Socket::Constants::AF_INET, Socket::Constants::SOCK_STREAM, 0
        server_sock_addr = Socket.sockaddr_in @port, @host
        begin
            @server_socket.bind server_sock_addr
        rescue Errno::EADDRINUSE => error
            puts error.message
            exit
        end
        @server_socket.listen @backlog
        trap("SIGINT") do
            @serving = false
            @server_socket.close
            puts "\nServer finished\n"
            return
        end
        @serving = true
        while @serving
            begin
                client_socket, client_sock_addr = @server_socket.accept_nonblock
                Thread.start client_socket do |client|
                    begin
                        request = client.recv 16384
                        request = Http::HttpRequest.new request
                        processor = Processors::ReponseProcessor.new request
                        response = processor.response
                        begin
                            client.write response.writable
                            client.close_write
                        rescue Errno::EPIPE
                        end
                    rescue => error
                        puts error.message
                        puts error.backtrace.join("\n")
                    ensure
                        client.close
                    end
                end
            rescue Errno::EAGAIN, Errno::ECONNABORTED, Errno::EPROTO, Errno::EINTR
                IO.select [@server_socket]
                retry
            end
        end
    end

    def shutdown
        @serving = false
        @server_socket.close
        puts "\nServer finished\n"
        return
    end
end

