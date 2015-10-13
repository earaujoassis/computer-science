# Cafezinho

> A smaller and minimalist fork of the C programming language. Cafezinho (noun)
> is Portuguese for a small cup of coffee.

## Compile

   ```sh
   $ make build
   ```

It creates the compiler (cafezinho) at the source folder root. Tested under
Unix-like systems only.

### Dependencies

 * Flex 2.5.x
 * Bison 2.7.x

## Test

   ```sh
   $ make test
   ```

It runs a test case for some source-code placed at test/folder. There's a
descriptor file for the tests in tests/descriptor.json.

### Dependencies

 * Python 2.7.x (not tested in Python 3.x)

## Regenerate source folder

   ```sh
   $ make clean
   ```

It removes the files created from Flex and Bison and also removes the compiler
(cafezinho) binary.

## License

[MIT License](http://earaujoassis.mit-license.org/) &copy; Ewerton Assis
