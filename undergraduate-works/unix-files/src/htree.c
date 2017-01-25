// Copyright 2013-2017 Ewerton Assis
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#include "files-info.h"

#define USAGE "Usage: htree <option> [path]\n\
Options:\n\
-h\t\tPrint this help message and exit\n\
[path]\t\tCount, recursively, how many regular files,\n\
\t\tdirectories and symbolic links a given [path] has\n\
\n\n"

int
main (int argc, char **argv)
{
  int c;

  while ((c = getopt (argc, argv, "h")) != -1)
    {
      switch (c)
        {
          case 'h':
            fprintf (stdout, USAGE);
            return 0;
          case '?':
            if (isprint (optopt))
              fprintf (stderr, "Unknown option '-%c'.\n", optopt);
            else
              fprintf (stderr, "Unknown option character '\\x%x'.\n", optopt);
            fprintf (stderr, USAGE);
            return 1;
          default:
            abort ();
        }
    }
  set_htree_counter ();
  if (nftw ((argc < 2) ? "." : argv[1], &compute_htree_info, 20, FTW_PHYS) == -1)
    {
      fprintf (stderr, "There was an error at nftw function\n");
      exit (EXIT_FAILURE);
    }
  if (argc < 2)
    fprintf (stdout, "WARNING: Executed from '.'\n");
  print_htree_counter (stdout);
  unset_htree_counter ();
  exit (EXIT_SUCCESS);
}
