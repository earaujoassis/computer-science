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
    ConfigPath = File.expand_path('../../../../config',  __FILE__) unless defined? ConfigPath

    class InvalidUrl < RuntimeError
    end

    def uri_pruner url
        return Array.new if url.nil? or url.empty?
        begin
            url = url.dup
            scheme = authority = path = query = nil
            if url.include? 'http://'
                url['http://'] = ''
                scheme = 'http://'
            elsif url.include? 'https://'
                url['https://'] = ''
                scheme = 'https://'
            end
            pieces = url.split(/[\/]/)
            authority = pieces.delete_at(0)
            path = '/' << pieces.join('/')
            if path.include? '?'
                pieces = path.split(/[?]/)
                path = pieces.delete_at(0)
                query = '?' << pieces.join('?')
            end
            if path.include? '#'
                pieces = path.split(/[#]/)
                path = pieces.delete_at(0)
                query = query.to_s << '#' << pieces.join('#')
            end
            path = path.split(/[\/]/)
            path.delete_at(path.length - 1)
            path = path.compact.delete_if{|element| element.empty?}.collect!{|element| '/' << element}
            path = path.join("")
        rescue
            raise InvalidUrl, "Invalid URI format; a valid one: uri-scheme://hierarchical-part/path?query#fragment"
        end
        scheme.to_s + authority.to_s + path.to_s + query.to_s
    end
    module_function :uri_pruner

    def uri_elements url
        return Array.new if url.nil? or url.empty?
        begin
            url = url.dup
            scheme = authority = path = query = nil
            if url.include? 'http://'
                url['http://'] = ''
                scheme = 'http://'
            elsif url.include? 'https://'
                url['https://'] = ''
                scheme = 'https://'
            end
            pieces = url.split(/[\/]/)
            authority = pieces.delete_at(0)
            path = '/' << pieces.join('/')
            if path.include? '?'
                pieces = path.split(/[?]/)
                path = pieces.delete_at(0)
                query = '?' << pieces.join('?')
            end
            if path.include? '#'
                pieces = path.split(/[#]/)
                path = pieces.delete_at(0)
                query = query.to_s << '#' << pieces.join('#')
            end
            path = path.split(/[\/]/).compact.delete_if{|element| element.empty?}.collect!{|element| '/' << element}
        rescue
            raise InvalidUrl, "Invalid URI format; a valid one: uri-scheme://hierarchical-part/path?query#fragment"
        end
        # What should I do? [uri_elements] + [authority] + path + [query]
        [scheme.to_s + authority] + path + [query]
    end
    module_function :uri_elements

    class UrlTreeNode
        attr_accessor :son, :brother, :element, :priority
        def initialize element
            @element = element
            @bother = @son = nil
            @priority = 0
        end
    end

    class UrlTree
        def initialize
            @root = nil
        end

        def delete url
            father = nil
            pointer = @root
            elements = ResourceData.uri_elements(url).compact
            while not elements.empty?
                element = elements.delete_at(0)
                return nil if pointer.nil?
                brother = nil
                while not pointer.brother.nil?
                    break if pointer.element == element
                    brother = pointer
                    pointer = pointer.brother
                end
                if pointer.element == element
                    if elements.empty?
                        # If pointer doesn't have a son, neither a brother
                        if pointer.brother.nil? and pointer.son.nil?
                            @root = nil if brother.nil? and father.nil?
                            if brother.nil?
                                father.son = nil unless father.nil?
                                pruned_url = ResourceData.uri_pruner(url)
                                self.delete pruned_url
                            else
                                brother.brother = nil
                            end
                        # If pointer doesn't have a son but it has a brother
                        elsif pointer.son.nil? and not pointer.brother.nil?
                            brother = pointer.brother unless brother.nil?
                            father.son = pointer.brother if brother.nil? and not father.nil?
                        end
                        return url
                    end
                    father = pointer
                    pointer = pointer.son
                    next
                else
                    return nil
                end
            end
            nil
        end

        def each            
            if block_given?
                self.to_a.each { |element| yield element }
            end
        end

        def include? url
            father = nil
            pointer = @root
            elements = ResourceData.uri_elements(url).compact
            while not elements.empty?
                element = elements.delete_at(0)
                return false if pointer.nil?
                #brother = nil
                while not pointer.brother.nil?
                    break if pointer.element == element
                    #brother = pointer
                    pointer = pointer.brother
                end
                if pointer.element == element
                    return true if elements.empty?
                    father = pointer
                    pointer = pointer.son
                    next
                else
                    return false
                end
            end
            false
        end

        def patriarchalism
            def wrapped_patriarch pointer
	            result = nil
	            unless pointer.nil?
	                result = wrapped_pick(pointer.son) unless pointer.son.nil?
	                return pointer.element if result.nil?
                    return (pointer.element.to_s + result.to_s)
                end
                result
            end
            return wrapped_patriarch(@root) unless @root.nil?
        end

        def pick
            def wrapped_pick root
                return Array.new if root.nil?
                return [[root.element, root]] if root.son.nil? and root.brother.nil?
                descendants = Array.new
                descendants += wrapped_pick(root.son) unless root.son.nil?
                descendants.each { |node| node[0] = root.element + node[0] }
                brotherhood = Array.new
                result = wrapped_pick(root.brother)
                brotherhood += result
                return [[root.element, root]] + brotherhood + descendants
            end
            picked = wrapped_pick(@root)
            return nil if picked.empty?
            begin
                chosen = picked[1]
                picked.each { |node| chosen = node if chosen[1].priority <= node[1].priority }
                picked.each { |node| node[1].priority += 1 }
                chosen[1].priority -= 2
            rescue
                return nil
            end
            return chosen[0]
        end

        def insert url
            father = nil
            pointer = @root
            elements = ResourceData.uri_elements(url).compact
            while not elements.empty?
                if pointer.nil?
                    primogenitus = UrlTreeNode.new(elements.delete_at(0))
                    father.son = primogenitus unless father.nil?
                    father = primogenitus
                    pointer = primogenitus.son
                    @root = father if @root.nil?
                    next
                end
                while not pointer.brother.nil?
                    break if pointer.element == elements.at(0)
                    pointer = pointer.brother
                end
                if pointer.element == elements.at(0)
                    father = pointer
                    pointer = pointer.son
                    elements.delete_at(0)
                    next
                else
                    primogenitus = UrlTreeNode.new(elements.delete_at(0))
                    pointer.brother = primogenitus
                    father = primogenitus
                    pointer = primogenitus.son
                    next
                end
            end
            url
        end

        def to_a
            def wrapped_to_a root
                return Array.new if root.nil?
                return [root.element] if root.son.nil? and root.brother.nil?
                descendants = Array.new
                descendants += wrapped_to_a(root.son) unless root.son.nil?
                descendants.collect! { |element| element = root.element + element }
                brotherhood = Array.new
                result = wrapped_to_a(root.brother)
                brotherhood += result
                return [root.element] + brotherhood + descendants
            end
            return wrapped_to_a(@root)
        end
    end

    class UrlTree
        alias << insert
    end
end

