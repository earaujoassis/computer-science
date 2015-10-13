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

# The URL Server policy statement
#
# 1. First of all, every URL has its right to be crawled/fetched,
#     then, one has more priority than others.
# 2. Second, every host has its right to rest for a while (I would
#    say... some bit of seconds)
# 3. Every path, within a host address, should be processed (It
#    must exist some policy to make the URL picker randomic)
# 4. Who has said that the URL Server has to be stateless? It must
#    know what its clients are doing with its resources, in a fancy
#    and painless way, instead
# 5. This server is not for anyone. Where are the security people?
#    Are they alredy dead? Who have hired them?
#

require 'data'

module Policy
    class Strategies
        def initialize
            @blacklist = ResourceData::ExternalList.new("blacklist")
            # OLD @pool = Array.new
            @pool = ResourceData::UrlTree.new
            @trash = Array.new
        end

        def allowed? url
            # TODO Implement it!
            # TODO Check for the last path element (for the URI: http://www.host.com/lero/lero/image.png?lero=lero)
            @blacklist.include? url
        end

        def awaiting
            # TODO Implement it!
            # OLD @pool.dup
            @pool.to_a - @trash
        end

        def fetched? url
            # TODO Implement it!
            @trash.include? url
        end

        def insert url
            # TODO Implement it!
            @pool << url if not @pool.include? url or not @trash.include? url
        end

        def isknown? url
            # TODO Implement it!
            @pool.include? url or @trash.include? url
        end

        def pick
            # TODO Implement it!
            # OLD range = @pool.length
            # OLD @pool.at(rand(range))
            picked = @pool.pick
            unless picked.nil?
                while @trash.include? picked
                    picked = @pool.pick
                end
            end
            picked
        end

        def purge url
            # TODO Implement it!
            @pool.delete url
            @trash.push url unless @trash.include? url
        end

        def resources
            # TODO Implement it!
            # OLD return @pool.dup + @trash.dup
            return @pool.to_a + @trash.dup
        end
    end

    Maker = Strategies.new
end

