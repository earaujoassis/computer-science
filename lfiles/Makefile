CC=gcc
CFLAGS=-lm
DEBUG=-DDEBUG
.PHONY: default build clean test
default:
	$(info <make build> to create the lfiles binary at .)
	$(info <make test> to test the lfiles binary)
	$(info )
build:
	$(CC) src/lfiles.c -o lfiles $(CFLAGS)
debug:
	$(CC) src/lfiles.c -o lfiles $(CFLAGS) $(DEBUG)
clean:
	rm -f lfiles
