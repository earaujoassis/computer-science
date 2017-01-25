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

#ifndef __jobshop_support_h__
#define __jobshop_support_h__

typedef enum { orlibrary, taillard } instance_t;
typedef enum { ga, ivf, ivfls } algorithm_t;

typedef struct {
  size_t n_jobs;
  size_t m_machines;
  unsigned long int **tech_constraints;
  unsigned long int **processing_time;
  instance_t instance_type;
} jobshop_t;

jobshop_t *
init_jobshop (size_t n_jobs,
              size_t m_machines,
              unsigned long int **tech_constraints,
              unsigned long int **processing_time,
              instance_t instance_type)
{
  jobshop_t *problem = (jobshop_t *) malloc (sizeof (jobshop_t));
  problem->n_jobs = n_jobs;
  problem->m_machines = m_machines;
  problem->tech_constraints = tech_constraints;
  problem->processing_time = processing_time;
  problem->instance_type = instance_type;
  return problem;
}

unsigned long int **
create_matrix (size_t n,
               size_t m)
{
  size_t i;
  unsigned long int **matrix;
  matrix = (unsigned long int **) calloc (n, 1 + sizeof (unsigned long int *));
  matrix[n] = NULL;
  for (i = 0; i < n; i++)
    matrix[i] = (unsigned long int *) calloc (m, sizeof (unsigned long int));
  return matrix;
}

void
delete_matrix (unsigned long int **matrix)
{
  size_t i;
  for (i = 0; matrix[i] != NULL; i++)
    free (matrix[i]);
  free (matrix);
}

void
del_jobshop (jobshop_t *problem)
{
  if (problem == NULL)
    return;
  delete_matrix (problem->tech_constraints);
  delete_matrix (problem->processing_time);
  free (problem);
}

instance_t
input_type (int argc, char **argv)
{
  int i;
  if (argc > 1)
    for (i = 1; i < argc; i++)
      if (!strcmp (argv[i], "--orlibrary"))
        return orlibrary;
      else if (!strcmp (argv[i], "--taillard"))
        return taillard;
  return orlibrary;
}

algorithm_t
algorithm_type (int argc, char **argv)
{
  int i;
  if (argc > 1)
    for (i = 1; i < argc; i++)
      if (!strcmp (argv[i], "--ivf"))
        return ivf;
      else if (!strcmp (argv[i], "--ga"))
        return ga;
  return ivf;
}

void
set_options (int argc, char **argv)
{
  int i;
  selection_method_t selection = proportional;
  recombination_method_t recombination = onepoint;
  mutation_method_t mutation = permutation;
  if (argc > 1)
    for (i = 1; i < argc; i++)
      {
        if (!strcmp (argv[i], "-s"))
          {
            if ((i + 1 < argc) && !strcmp (argv[i + 1], "proportional"))
                selection = proportional;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "tournament"))
                selection = tournament;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "ranking"))
              selection = ranking;
            continue;
          }
        else if (!strcmp (argv[i], "-r"))
          {
            if ((i + 1 < argc) && !strcmp (argv[i + 1], "onepoint"))
              recombination = onepoint;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "npoint"))
              recombination = npoint;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "uniform"))
              recombination = uniform;
            continue;
          }
        else if (!strcmp (argv[i], "-m"))
          {
            if ((i + 1 < argc) && !strcmp (argv[i + 1], "permutation"))
              mutation = permutation;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "regenerated"))
              mutation = regenerated;
            else if ((i + 1 < argc) && !strcmp (argv[i + 1], "both"))
              mutation = regenerated_permutation;
            continue;
          }
      }
  init_options (selection, recombination, mutation);
}

void
show_problem_data (jobshop_t *problem)
{
  size_t i, j;
  printf ("jobs: %ld, machines: %ld\n", problem->n_jobs, problem->m_machines);
  printf ("technological constraints:\n");
  for (i = 0; i < problem->n_jobs; i++)
    {
      for (j = 0; j < problem->m_machines; j++)
        printf ("%3ld ", problem->tech_constraints[i][j]);
      printf ("\n");
    }
  printf ("processing time:\n");
  for (i = 0; i < problem->n_jobs; i++)
    {
      for (j = 0; j < problem->m_machines; j++)
        printf ("%3ld ", problem->processing_time[i][j]);
      printf ("\n");
    }
}

#endif

