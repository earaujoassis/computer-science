cafezinho
=========

A smaller and minimalist fork of the C programming language. Cafezinho (noun) is portuguese for small cup of coffee.

## Compile

It needs Flex 2.5.x and Bison 2.7.x. Tested under Unix-like systems only.
It creates the compiler binary (cafezinho) at the source folder root.


    make build


## Test

It needs Python 2.7+. It wasn't tested under Python 3.x. There's a descriptor
file for the tests in tests/descriptor.json.


    make test


## Regenerate source folder

It removes the files created from Flex and Bison and also removes the compiler
(cafezinho) binary.


    make clean


Copyright &copy; 2013. Ewerton Assis (earaujoassis at gmail dot com).
