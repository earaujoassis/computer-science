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

class ForParser < Template::Tags::Parser
    def parser context
        caller = @block.scan(/\{\$[ _A-Za-z.]*\$\}/).at(0).scan(/\w+/)
        if caller.length != 4
            raise MalformedTag, "for tag format: 'for <item_name> in <iterable_element>'"
        end
        block = cleaned_block
        item_name, iterable_element = caller[1], caller[3]
        iterable_element = Template.getfrom context, iterable_element
        final_block = String.new
        iterable_element.each do |value|
            final_block << Template.setvalue(block, item_name, value)
        end
        final_block
    end
end

Template::Tags::Parsing.signalize do |signalizer|
    signalizer.determine 'for', 'ForParser'
end

