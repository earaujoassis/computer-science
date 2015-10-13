# Linux Files

> File tools written for Unix-like systems.

## Compile

The command `make build` creates the binaries at the bin/ folder.

## Debug

The command `make debug` creates a debug version of the binaries. Each of them prints more information
for each function available in the binaries (see "How to use" below).

## Regenerate source folder

The command `make clean` removes the binaries (it purges the source folder).

## How to use

Just execute `lfiles -h`, `finfo -h`, or `shrink -h` to see instructions. `lfiles` has three major
functions: a histogram for files size (the user sets each histogram class); a function that searches
every file in the filesystem with two hard links; and a function that lists every file for a set of
folders. `shrink` just shrinks a file using a signal byte: for every four or more occurrencies of that
signal, it shrinks it to just one. `finfo` prints information about a file-name. `htree` counts,
recursively, how many regular files, directories, and symbolic links a given directory has.

## License

[MIT License](http://earaujoassis.mit-license.org/) &copy; 2013-2015 Ewerton Assis
