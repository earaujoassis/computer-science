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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIGNAL '#'
#define FILE_PREFIX "shrinked-"
#define USAGE "Usage: shrink <options>\n\
Options:\n\
-h\t\tPrint this help message\n\
<filepath>\tIt shrinks the <filepath> size\n\n"

int
main (int argc, char **argv)
{
  char *filepath, *newfilepath, c;
  size_t filepath_len;
  FILE *ifile, *shrinked;

  if (argc < 2)
    {
      fprintf (stderr, "Error: <filepath> is missing\n");
      fprintf (stderr, USAGE);
      return 0;
    }
  else if (argc == 2)
    while ((c = getopt (argc, argv, "h")) != -1)
      switch (c)
        {
          case 'h':
            fprintf (stdout, USAGE);
            return 0;
        }
  filepath = argv[1];
  filepath_len = strlen (filepath);
  ifile = fopen (filepath, "rb");
  if (ifile != NULL)
    {
      char current_B, previous_B;
      char counter, i;
      newfilepath = (char *) calloc ((filepath_len + 10), sizeof (char));
      sprintf (newfilepath, "%s%s", FILE_PREFIX, filepath);
      shrinked = fopen (newfilepath, "w");
      fscanf (ifile, "%c", &previous_B);
      while (fscanf (ifile, "%c", &current_B) != EOF)
        {
          if (current_B == previous_B)
            counter++;
          else if (current_B != previous_B)
            {
              if (counter < 4)
                if (counter == 0)
                  fprintf (shrinked, "%c", previous_B);
                else
                  for (i = 0; i < counter; i++)
                    fprintf (shrinked, "%c", previous_B);
              else
                fprintf (shrinked, "%c%c%c", SIGNAL, counter, previous_B);
              counter = 0;
            }
          previous_B = current_B;
        }
      fprintf (shrinked, "%c", previous_B);
      fprintf (stdout, "New shrinked file created: %s.\n\n", newfilepath);
      fclose (ifile);
      fclose (shrinked);
      free (newfilepath);
      return 0;
    }
  fprintf (stderr, "Could not open \"%s\" file.\n\n", filepath);
  return 0;
}
