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

#define USAGE "Usage: finfo <option> [file-name]\n\
Options:\n\
-h\t\t\tPrint this help message and exit\n\
[file-name]\t\tPrint information about [file-name] file\n\
\n\n"

int
main (int argc, char **argv)
{
  int c, strlen_fname, i;
  char *filename, buffer[80];
  struct stat st;
  struct tm *timeinfo;

  if (argc < 2)
    {
      fprintf (stderr, USAGE);
      return 0;
    }
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
  if (optind == argc)
    {
      fprintf (stderr, "Error: missing [file-name] element\n");
      fprintf (stderr, USAGE);
      return 0;
    }
  filename = argv[optind];
  strlen_fname = strlen(filename);
  if (stat (filename, &st) < 0)
    {
      fprintf (stderr, "Error: [file-name] doens't point to a file\n");
      fprintf (stderr, USAGE);
      return 0;
    }
  fprintf (stdout, "%s:", filename);
  fprintf (stdout, " dev:%d ", st.st_dev);
  fprintf (stdout, " rdev:%d ", st.st_rdev);
  fprintf (stdout, " ino:%d ", st.st_ino);
  fprintf (stdout, " nlink:%d ", st.st_nlink);
  fprintf (stdout, " uid:%d  gid:%d \n", st.st_uid, st.st_gid);
  for (i = 0; i <= strlen_fname; i++)
    fprintf (stdout, " ");
  fprintf (stdout, " blksize:%d  blocks:%d ", st.st_blksize, st.st_blocks);
  fprintf (stdout, " size:%d bytes \n", st.st_size);
  for (i = 0; i <= strlen_fname; i++)
    fprintf (stdout, " ");
  fprintf (stdout, " acess mode: ");
  fprintf (stdout, (S_ISDIR (st.st_mode)) ? "d" : "-");
  fprintf (stdout, (st.st_mode & S_IRUSR) ? "r" : "-");
  fprintf (stdout, (st.st_mode & S_IWUSR) ? "w" : "-");
  fprintf (stdout, (st.st_mode & S_IXUSR) ? "x" : "-");
  fprintf (stdout, (st.st_mode & S_IRGRP) ? "r" : "-");
  fprintf (stdout, (st.st_mode & S_IWGRP) ? "w" : "-");
  fprintf (stdout, (st.st_mode & S_IXGRP) ? "x" : "-");
  fprintf (stdout, (st.st_mode & S_IROTH) ? "r" : "-");
  fprintf (stdout, (st.st_mode & S_IWOTH) ? "w" : "-");
  fprintf (stdout, (st.st_mode & S_IXOTH) ? "x" : "-");
  fprintf (stdout, "\n");
  for (i = 0; i <= strlen_fname; i++)
    fprintf (stdout, " ");
  timeinfo = localtime (&st.st_atime);
  strftime (buffer, 80, "%a %h %d %H:%M %Y", timeinfo);
  fprintf (stdout, " at: %s\n", buffer);
  for (i = 0; i <= strlen_fname; i++)
    fprintf (stdout, " ");
  timeinfo = localtime (&st.st_mtime);
  strftime (buffer, 80, "%a %h %d %H:%M %Y", timeinfo);
  fprintf (stdout, " mt: %s\n", buffer);
  for (i = 0; i <= strlen_fname; i++)
    fprintf (stdout, " ");
  timeinfo = localtime (&st.st_ctime);
  strftime (buffer, 80, "%a %h %d %H:%M %Y", timeinfo);
  fprintf (stdout, " ct: %s\n", buffer);
  fprintf (stdout, "\n");

  return 0;
}
