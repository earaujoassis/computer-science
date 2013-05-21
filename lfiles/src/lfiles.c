// Copyright 2013 Ewerton Assis
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

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#include "files-info.h"

#define USAGE "Usage: lfiles <option>\n\
Options:\n\
-h\t\t\t\t\tPrint this help message\n\
-s <size in bytes> <folder root>\tGenerate a histogram for files; <size in bytes>\n\
\t\t\t\t\tdetermines each class\n\
-i\t\t\t\t\tSearch for all i-nodes with estrict connections\n\
\t\t\t\t\twith 2 as value; list all those files related\n\
-l (<dirname>)+\t\t\t\tShow files for every <dirname> listed\n\n"

int
main (int argc, char **argv)
{
  int c;
  int iflag = 0, sflag = 0, lflag = 0;
  char *svalue = NULL;

  if (argc < 2)
    {
      fprintf (stderr, USAGE);
      return 0;
    }
  while ((c = getopt (argc, argv, "hs:il")) != -1)
    {
      switch (c)
        {
          case 'h':
            fprintf (stdout, USAGE);
            return 0;
          case 's':
            svalue = optarg;
            sflag = 1;
            break;
          case 'i':
            iflag = 1;
            break;
          case 'l':
            lflag = 1;
            break;
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
  if (sflag + iflag + lflag > 1)
    {
      fprintf (stderr, "It's not allowed to use more than one function at a time.\n");
      fprintf (stderr, USAGE);
      return 1;
    }
  if (sflag)
    {
      if (argc == optind)
        {
          fprintf (stderr, "Error: -h: <folder root> is missing\n");
          fprintf (stderr, USAGE);
          return 1;
        }
      if (argc > optind + 1)
        {
          fprintf (stderr, "Error: -h: One and only <folder root>\n");
          fprintf (stderr, USAGE);
          return 1;
        }
      size_t bytes_class = strtol (svalue, (char **) NULL, 10);
      if (bytes_class <= 0)
        {
          fprintf (stderr, "Error: -h: Improper value for <size in bytes>: it should be > 0\n");
          fprintf (stderr, USAGE);
          return 1;
        }
      char *folder_root = argv[optind];
      return generate_histogram (bytes_class, folder_root);
    }
  if (iflag)
    {
      return inode_files ();
    }
  if (lflag)
    {
      if (argc == optind)
        {
          fprintf (stderr, "Error: -l: At least one <dirname>\n");
          fprintf (stderr, USAGE);
          return 1;
        }
      return list_directories (optind, argc, (const char**) argv);
    }
  return 0;
}
