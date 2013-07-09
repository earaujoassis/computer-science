CC=gcc
CFLAGS=-lm
DEBUG=-DDEBUG
.PHONY: default build clean test
default:
	$(info <make build> to create the lfiles binary at .)
	$(info )
build:
	mkdir -p bin
	$(CC) src/lfiles.c -o bin/lfiles $(CFLAGS)
	$(CC) src/shrink.c -o bin/shrink $(CFLAGS)
	$(CC) src/finfo.c -o bin/finfo $(CFLAGS)
debug:
	mkdir -p bin
	$(CC) src/lfiles.c -o bin/lfiles $(CFLAGS) $(DEBUG)
	$(CC) src/shrink.c -o bin/shrink $(CFLAGS) $(DEBUG)
	$(CC) src/finfo.c -o bin/finfo $(CFLAGS) $(DEBUG)
clean:
	rm -f bin/lfiles
	rm -f bin/shrink
	rm -f bin/finfo
	rm -fr bin
