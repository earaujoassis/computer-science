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

#ifndef __lfiles_info_h__
#define __lfiles_info_h__

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <limits.h>
#include <string.h>
#include <math.h>

int
generate_histogram (const size_t bytes_class, const char *folder_root)
{
  int i, index;
  char current_dir_alloc_flag = 0;
  size_t *histogram, histogram_size, total_files, folder_root_length, current_path_to_file_length, omitted_classes;
  char *current_dir, *current_path_to_file;
  struct dirent *pDirent;
  struct stat st;
  DIR *pDir;

  omitted_classes = total_files = 0;
  histogram_size = 1;
  histogram = (size_t *) calloc (histogram_size, sizeof (size_t));
  folder_root_length = strlen (folder_root);
  if (!strcmp(folder_root, ".") || !strcmp(folder_root, "..")
      || folder_root[folder_root_length - 2] != '/')
    {
      current_dir = (char *) calloc (4, sizeof (char));
      sprintf (current_dir, "%s/", folder_root);
      current_dir_alloc_flag = 1;
    }
  else  
    current_dir = (char *) folder_root;
  pDir = opendir (current_dir);
  if (pDir == NULL)
    {
      fprintf (stderr, "Fatal error: Cannot open directory: %s\n", current_dir);
      exit (1);
    }
  while ((pDirent = readdir (pDir)) != NULL)
    {
      if (pDirent->d_name[0] == '.' || pDirent->d_type != DT_REG) continue;
      const char *current_file = pDirent->d_name;
      total_files++;
      current_path_to_file_length = strlen (current_dir) + strlen (current_file);
      current_path_to_file = (char *) calloc (current_path_to_file_length + 1, sizeof (char));
      sprintf (current_path_to_file, "%s%s", current_dir, current_file);
      stat (current_path_to_file, &st);
      index = (int) floorf ((float) st.st_size / (float) bytes_class);
      if (index > histogram_size)
        {
          size_t *temp_histogram;
          size_t old_size = histogram_size;
          histogram_size = index + 1;
          temp_histogram = (size_t *) calloc (histogram_size, sizeof (size_t));
          for (i = 0; i < old_size; i++)
            temp_histogram[i] = histogram[i];
          free (histogram);
          histogram = temp_histogram;
        }
      histogram[index] =+ 1;
#ifdef DEBUG
      fprintf (stdout, "%s: %d; index: %d\n", current_path_to_file, st.st_size, index);
#endif
      free (current_path_to_file);
    }
  fprintf (stdout, "total files: %d\n", total_files);
  for (i = 0; i < histogram_size; i++)
    switch (histogram[i])
      {
        case 0:
          omitted_classes++;
#ifdef DEBUG
          fprintf (stdout, "% 8d  % 8d  no files\n", i * bytes_class, (i + 1) * bytes_class - 1);
#endif
          break;
        case 1:
          fprintf (stdout, "% 8d  % 8d  1 file\n", i * bytes_class, (i + 1) * bytes_class - 1);
          break;
        default:
          fprintf (stdout, "% 8d  % 8d  %d files\n", i * bytes_class, (i + 1) * bytes_class - 1, histogram[i]);
          break;
      }
  fprintf (stdout, "%d omitted classe(s)\n", omitted_classes);
  closedir (pDir);
  if (current_dir_alloc_flag) free (current_dir);
  free (histogram);
  return 0;
}

int
inode_files ()
{
  return 0;
}

int
list_directories (int argc_begin, int argc_final, const char **argv)
{
  int i;
  char final_slash_flag;
  size_t total_files;
  struct dirent *pDirent;
  struct stat st;
  DIR *pDir;

  for (i = argc_begin; i < argc_final; i++)
    {
      size_t current_dir_length, current_path_to_file_length;
      char *current_dir, *current_path_to_file;
      total_files = 0;
      current_dir_length = strlen (argv[i]);
      current_dir = (char *) calloc (current_dir_length + 1, sizeof (char));
      if (!strcmp(argv[i], ".") || !strcmp(argv[i], "..")
          || argv[i][current_dir_length - 1] != '/')
        sprintf (current_dir, "%s/", argv[i]);
      else
        sprintf (current_dir, "%s", argv[i]);
      pDir = opendir (current_dir);
      if (pDir == NULL)
        {
          fprintf (stderr, "Fatal error: Cannot open directory: %s\n", current_dir);
          exit (1);
        }
      while ((pDirent = readdir (pDir)) != NULL)
        {
          if (pDirent->d_name[0] == '.' || pDirent->d_type != DT_REG) continue;
          const char *current_file = pDirent->d_name;
          total_files++;
          current_path_to_file_length = strlen (current_dir) + strlen (current_file);
          current_path_to_file = (char *) calloc (current_path_to_file_length + 1, sizeof (char));
          sprintf (current_path_to_file, "%s%s", current_dir, current_file);
          stat (current_path_to_file, &st);
          fprintf (stdout, "% 8d  %s%s\n", st.st_size, current_dir, current_file);
        }
      closedir (pDir);
      fprintf (stdout, "total files: %d\n", total_files);
      if (i != argc_final - 1) printf ("\n");
    }  
  return 0;
}

#endif