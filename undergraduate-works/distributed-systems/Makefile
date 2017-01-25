CC=gcc
CFLAGS=
DEBUG=-DDEBUG
.PHONY: default build test clean
default:
	$(info <make build> to create the binaries at .)
	$(info <make test> to test a stub context)
	$(info )
build:
	mkdir -p bin
	mkdir -p cls
	javac -d ./cls/ -cp ./cls/ ./src/java-rmi/UpperInterface.java
	javac -d ./cls/ -cp ./cls/ ./src/java-rmi/UpperServer.java
	javac -d ./cls/ -cp ./cls/ ./src/java-rmi/UpperApp.java
test:
	python test-build.py java-rmi
	python test-build.py py-crbc
clean:
	rm -f src/python/*.pyc
	rm -f src/python/crbc/*.pyc
	rm -f src/python/crbc/net/*.pyc
	rm -f src/python/crbc/support/*.pyc
	rm -f cls/*.class
	rm -fr cls/
	rm -fr bin/
