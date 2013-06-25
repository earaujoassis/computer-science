cafezinho
=========

A smaller and minimalist fork of the C programming language. Cafezinho (noun)
is portuguese for small cup of coffee.

## Compile

The statement `make build` creates the compiler (cafezinho) at the source
folder root. It needs Flex 2.5.x and Bison 2.7.x. Tested under Unix-like
systems only.

## Test

The statement `make test` run a test case for some source-code placed at test/
folder. It needs Python 2.7+ to run the test case; it wasn't tested under 
Python 3.x. There's a descriptor file for the tests in tests/descriptor.json.

## Regenerate source folder

The statement `make clean` removes the files created from Flex and Bison and
also removes the compiler (cafezinho) binary.

Copyright &copy; 2013 Ewerton Assis (earaujoassis at gmail dot com).
