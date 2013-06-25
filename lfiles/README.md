lfiles
=========

A files tool written for Unix-like systems.

## Compile

The command `make build` creates the `lfiles` binary at the source folder root.

## Debug

The command `make debug` creates a debug version of the `lfiles` binary. It
prints more information for each function available in the binary (see "How
to use" below).

## Regenerate source folder

The command `make clean` removes the binary (it purges the source folder).

## How to use

Just execute `lfiles -h` to see instructions. It has three major functions: a
histogram for files size (the user sets each histogram class); a function that
searches every file in the filesystem with two hard links; and a function that
lists every file for a set of folders.

Copyright &copy; 2013. Ewerton Assis (earaujoassis at gmail dot com).
