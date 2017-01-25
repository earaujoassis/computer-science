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

module Routes
    module Exceptions
        class RouteNotFound < RuntimeError
        end
    end

    class RegisterRoutes
        attr_reader :connections
        def initialize
            @connections = Hash.new
        end

        def connect url, map={}
            @connections.store(url, map)
        end

        def parse regex, map={}
        end
    end

    class RoutingParser
        attr_reader :signalized
        def initialize
            @signalized = RegisterRoutes.new
        end

        def signalize
            if block_given?
                yield @signalized
            end
        end

        def connections
            @signalized.connections
        end

        def controller_for uri
            raise Routes::Exceptions::RouteNotFound, "Route not found" unless Routes::Routing.connections.key? uri
            map = Routes::Routing.connections[uri]
            resource = "#{map[:resource].capitalize}Resource"
            return :class => resource, :method => map[:method]
        end
    end

    Routing = RoutingParser.new
end

