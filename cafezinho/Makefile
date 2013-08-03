CPP=g++
CPPFLAGS=-O2
DEBUG=-DDEBUG
.PHONY: default build clean test
default:
	$(info <make build> to create the cafezinho binary at .)
	$(info <make test> to test the cafezinho compiler)
	$(info )
build:
	bison -o src/cafezinho-parser.cpp -y -d src/cafezinho-parser.y
	flex -o src/cafezinho-lexer.cpp src/cafezinho-scanner.l
	$(CPP) src/*.cpp -o cafezinho $(CPPFLAGS)
	rm -f src/*.cpp
	rm -f src/*.hpp
debug:
	bison -o src/cafezinho-parser.cpp -y -d src/cafezinho-parser.y
	flex -o src/cafezinho-lexer.cpp src/cafezinho-scanner.l
	$(CPP) src/*.cpp -o cafezinho $(CPPFLAGS) $(DEBUG)
	rm -f src/*.cpp
	rm -f src/*.hpp
clean:
	rm -f cafezinho
	rm -f src/*.cpp
	rm -f src/*.hpp
test:
	python test-build.py
