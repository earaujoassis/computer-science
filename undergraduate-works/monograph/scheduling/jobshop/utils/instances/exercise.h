// Copyright 2011 Éwerton Assis
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

#ifndef __jobshop_exercise_h__
#define __jobshop_exercise_h__

#include <string.h>
#include "../support.h"
#include "parser.h"

void
fetch_execute (FILE *input_stream,
               instance_t instance_type,
               algorithm_t alg_type)
{
  jobshop_t *problem;
  stats_t *stats;
  problem = init_instance (input_stream, instance_type);
  if (problem == NULL)
    return;
  stats = executor (problem, alg_type);
  print_common_info (stats, NULL);
  del_stats (stats);
  del_jobshop (problem);
}

void
exercise_instances (algorithm_t heuristic,
                    FILE *input_stream,
                    FILE *output_stream)
{
  int i, num_files, length;
  FILE *instance_file;
  char *instance, *path, *file;
  instance_t type_instance;
  jobshop_t *problem;
  stats_t *stats;

  instance = calloc (15, sizeof (char));
  fscanf (input_stream, "%d", &num_files);
  fscanf (input_stream, "%s", instance);
  if (!strcmp(instance, "orlibrary"))
    type_instance = orlibrary;
  else if (!strcmp(instance, "taillard"))
    type_instance = taillard;
  free (instance);
  path = calloc (100, sizeof (char));
  fscanf (input_stream, "%s", path);
  fprintf (output_stream, "Instance,Best,Mean,Worst,Interval,Evaluations,\"Population Size\"\n");
  for (i = 0; i < num_files; i++)
    {
      file = calloc (20, sizeof (char));
      fscanf (input_stream, "%s", file);
      length = strlen (file) + strlen (path);
      instance = calloc (length + 3, sizeof (char));
      strcpy (instance, path);
      strcat (instance, "/");
      strcat (instance, file);
      instance_file = fopen (instance, "r");
      if (!instance_file)
        {
          printf ("File not found: %s\n", instance);
          free (instance);
          free (file);
          continue;
        }
      free (instance);
      /* TODO Taillard's instances are not being iterated through the 10 configurations */
      problem = init_instance (instance_file, type_instance);
      if (problem == NULL)
        {
          free (file);
          fclose (instance_file);
          continue;
        }
      stats = executor (problem, heuristic);
      fprintf (output_stream, "%s,%lf,%lf,%lf,%ld,%ld,%ld\n", file, stats->max_fitness, stats->ave_fitness, stats->min_fitness, \
        stats->time, stats->evaluations_counted, stats->population_size);
      free (file);
      del_stats (stats);
      del_jobshop (problem);
      fclose (instance_file);
    }
  free (path);
}

int
exercises_executor (int argc, char **argv)
{
  int i;
  char *input, *output;
  FILE *exercise_file, *csv_file;
  algorithm_t heuristic;
  input = output = NULL;
  if (argc > 1)
    for (i = 1; i < argc; i++)
      if (!strcmp(argv[i], "-f"))
        input = argv[++i];
      else if (!strcmp(argv[i], "-o"))
        output = argv[++i];
  if (input == NULL)
    return 0;
  exercise_file = fopen (input, "r");
  if (!exercise_file)
    {
      printf ("File not found: %s\n", input);
      exit (-1);
    }
  if (output == NULL)
    output = "a.csv";
  csv_file = fopen (output, "w");
  heuristic = algorithm_type (argc, argv);
  exercise_instances (heuristic, exercise_file, csv_file);
  fclose (exercise_file);
  fclose (csv_file);
  return 1;
}

#endif

