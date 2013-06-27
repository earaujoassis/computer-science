CC=gcc
CFLAGS=-lm
DEBUG=-DDEBUG
.PHONY: default build clean test
default:
	$(info <make build> to create the lfiles binary at .)
	$(info )
build:
	$(CC) src/lfiles.c -o lfiles $(CFLAGS)
	$(CC) src/shrink.c -o shrink $(CFLAGS)
debug:
	$(CC) src/lfiles.c -o lfiles $(CFLAGS) $(DEBUG)
	$(CC) src/shrink.c -o shrink $(CFLAGS) $(DEBUG)
clean:
	rm -f lfiles
	rm -f shrink
