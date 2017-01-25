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

module ResourceData
    ConfigPath = File.expand_path('../../../config',  __FILE__) unless defined? ConfigPath

    class Node
        attr_accessor :element, :coming, :previous
        def initialize element, coming=nil, previous=nil
            @element = element
            @coming = coming
            @previous = previous
        end
    end

    class ExternalList
        attr_reader :size
        def initialize filename
            @size, @head, @filename = 0, nil, filename
            File.new("#{ConfigPath}/#{@filename}", "a+") unless File.exist? "#{ConfigPath}/#{@filename}"
            @file = File.open("#{ConfigPath}/#{@filename}", "r+")
            @file.sync = true
            return process
        end

        def clear
            @size, @head = 0, nil; @file.close
            File.delete("#{ConfigPath}/#{@filename}")
            File.new("#{ConfigPath}/#{@filename}", "a+")
            @file = File.open("#{ConfigPath}/#{@filename}", "r+")
            @file.sync = true
        end

        def delete url
            return nil if self.empty?
            # I'm using the temporary file solution. It's working =/
            temporary = File.new("#{ConfigPath}/#{@filename}~", "a+")
            deleted = nil; node = @head; @file.rewind
            while not node.nil?
                index = node.element
                @file.seek(index, IO::SEEK_SET)
                content = @file.read(512)
                content = content.delete("\0")
                if content == url
                    deleted = content
                else
                    temporary.syswrite(content.ljust(512, "\0"))
                end
                node = node.coming
            end
            return nil if deleted.nil?
            @file.close; temporary.close
            File.delete("#{ConfigPath}/#{@filename}")
            File.rename("#{ConfigPath}/#{@filename}~", "#{ConfigPath}/#{@filename}")
            @file = File.open("#{ConfigPath}/#{@filename}", "r+")
            @file.sync = true
            node = @head
            while not node.coming.nil?; node = node.coming; end
            coming = node.coming; previous = node.previous
            previous.coming = coming unless previous.nil?
            coming.previous = previous unless coming.nil?
            @size -= 1
            @head = nil if @size == 0
            deleted
        end

        def each            
            if block_given?
                self.to_a.each { |element| yield element }
            end
        end

        def empty?
            @size == 0
        end

        def include? url
            @file.rewind
            while not @file.eof?
                content = @file.read(512) # TODO Aparentemente essa parte do código retorna um nil
                content = content.delete("\0")
                if content.match(url) or url.match(content) or content == url
                    return true
                    break
                end
            end
            false
        end

        def length
            @size
        end

        def pop
            # TODO Implement it!
        end

        def push url
            url_normalized = url.ljust(512, "\0")
            @file.seek(0, IO::SEEK_END)
            if url_normalized.length > 512
                # TODO Implement it! It'll change a lot the whole solution! =/
            else
                node = Node.new(@file.pos, nil, nil)
                @file.syswrite(url_normalized)
            end
            unless @head.nil?
                previous = @head
                while not previous.coming.nil?; previous = previous.coming; end
                previous.coming = node; node.previous = previous
            else
                @head = node
            end
            @size += 1
            url
        end

        def lindex
            array, node = Array.new, @head
            while not node.nil?
                array << (node.element)
                node = node.coming
            end
            array
        end

        def to_a
            @file.rewind
            array = Array.new
            indexes = self.lindex
            indexes.each do |index|
                @file.seek(index, IO::SEEK_SET)
                content = @file.read(512)
                content = content.delete("\0")
                array << content
            end
            array
        end

        def flush
            @file.flush; @file.fsync
        end

        private
        def process
            return if @file.eof?
            previous = nil
            while not @file.eof?
                node = Node.new(@file.pos, nil, nil)
                @file.read(512)
                @size += 1
                previous.coming = node unless previous.nil?
                node.previous = previous
                previous = node
            end
            previous = previous
            while not previous.previous.nil?
                previous = previous.previous
            end
            @head = previous
            nil
        end
    end

    class ExternalList
        alias << push
    end
end

