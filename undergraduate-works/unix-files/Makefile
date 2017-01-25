CC=gcc
CFLAGS=-lm
DEBUG=-DDEBUG
.PHONY: default build clean test
default:
	$(info <make build> to create the binaries at bin/)
	$(info )
build:
	mkdir -p bin
	$(CC) src/lfiles.c -o bin/lfiles $(CFLAGS)
	$(CC) src/shrink.c -o bin/shrink $(CFLAGS)
	$(CC) src/finfo.c -o bin/finfo $(CFLAGS)
	$(CC) src/htree.c -o bin/htree $(CFLAGS)
debug:
	mkdir -p bin
	$(CC) src/lfiles.c -o bin/lfiles $(CFLAGS) $(DEBUG)
	$(CC) src/shrink.c -o bin/shrink $(CFLAGS) $(DEBUG)
	$(CC) src/finfo.c -o bin/finfo $(CFLAGS) $(DEBUG)
	$(CC) src/htree.c -o bin/htree $(CFLAGS) $(DEBUG)
clean:
	rm -f bin/lfiles
	rm -f bin/shrink
	rm -f bin/finfo
	rm -f bin/htree
	rm -fr bin
