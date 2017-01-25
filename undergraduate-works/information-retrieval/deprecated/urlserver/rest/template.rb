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

module Template
    def getfrom context, element
        value = nil
        begin
            value = context.send("#{element}")
        rescue NoMethodError
            begin
                if context.send("key?", element)
                    value = context.send("[]", element)
                elsif context.send("key?", element.intern)
                    value = context.send("[]", element.intern)
                end
            rescue NoMethodError
                raise Template::Exceptions::ParserError, "Unkown element: #{element}"
            end
        end
        value
    end

    def getcalls value, calls
        variables = calls
        while not variables.empty?
            variable = variables.delete_at(0)
            begin
                value = value.send("#{variable}")
            rescue NoMethodError
                begin
                    if value.send("key?", variable)
                        value = value.send("[]", variable)
                    elsif value.send("key?", variable.intern)
                        value = value.send("[]", variable.intern)
                    end
                rescue NoMethodError
                    raise Template::Exceptions::ParserError, "Unkown call element: #{variable}"
                end
            end
        end
        value
    end

    def setvalue block, name, value
        block = block.dup #Necessary, by the way
        block.scan(/\{\%[ ]?#{name}[._A-Za-z!?]*[ ]?\%\}/).each do |code|
            calls = code.scan(/[!?A-Za-z_]+/)
            calls.delete_at(0)
            value = Template.getcalls(value, calls)
            block[code] = value.to_s
        end
        block
    end
    module_function :getfrom, :getcalls, :setvalue

    module Exceptions
        class ParserError < RuntimeError
        end

        class MalformedTag < RuntimeError
        end
    end

    class ProcessContext
        attr_reader :file, :content
        def initialize file_name
            @file, @content, @size = File.new(file_name, "r"), String.new, nil
            file.each {|line| @content << line}
        end

        def process context
            processed_content = String.new
            content = @content.dup
            tags = content.scan(/\{\$[ _A-Za-z.]*\$\}.*[-!\"\#$%&\'()*+,.\/:;<=>?@\[\\\]\^_\`{|}~A-Za-z0-9<>\/%_ \t\r\n\v\f]*\{\$.*end.*\$\}/)
            tags.each do |tag|
                result = Template::Tags::Parsing.parsing(tag, context)
                content[tag] = result.to_s
            end
            content.each_line do |line|
                local_line = line.dup
                line.scan(/\{\%[!?._A-Za-z ]*\%\}+/) do |word|
                    variables = word.scan(/[!?A-Za-z_]+/)
                    variable = variables.delete_at(0)
                    value = Template.getfrom(context, variable)
                    value = Template.getcalls(value, variables)
                    unless value.nil?
                        local_line[word] = value.to_s
                    else
                        local_line[word] = ""
                    end
                end
                processed_content << local_line
            end
            @size = processed_content.length
            processed_content
        end

        def size
            if @size.nil?
                return @file.stat.size
            end
            @size
        end
    end

    module Tags
        class RegisterTag
            attr_reader :tags
            def initialize
                @tags = Hash.new
            end

            def determine tag_name, tag_class
                @tags.store(tag_name, tag_class)
            end
        end

        class TagParser
            def initialize
                @signalized = RegisterTag.new
            end

            def signalize
                if block_given?
                    yield @signalized
                end
            end

            def tags
                @signalized.tags
            end

            def parsing block, context
                tag_name = block.scan(/\{\$[ _A-Za-z.]*\$\}/).at(0).scan(/\w+/).at(0)
                tag_class = @signalized.tags[tag_name]
                instance = Kernel.const_get(tag_class).new(block)
                result = instance.parser(context)
            end
        end

        Parsing = TagParser.new

        class Parser
            def initialize block
                @block = block
            end

            def parser context
            end

            private
            def cleaned_block
                block = @block.dup
                block.scan(/\{\$[ _A-Za-z.]*\$\}/).each {|trash| block[trash] = "" }
                block
            end
        end
    end
end

