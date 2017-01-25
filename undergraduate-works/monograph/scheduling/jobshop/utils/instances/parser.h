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

#ifndef __jobshop_parser_h__
#define __jobshop_parser_h__

#define TAILLARD_N_INSTANCES     10

#include "../support.h"

jobshop_t *
init_instance (FILE *stream,
               instance_t type)
{
  jobshop_t *problem;
  size_t i, j;
  size_t n_jobs, m_machines;
  unsigned long int **tech_constraints;
  unsigned long int **processing_time;
  if (type == taillard)
    {
      unsigned long int time_seed, machine_seed;
      unsigned long int upper_bound, lower_bound;
      fscanf (stream, "%*[^\n]");
      fscanf (stream, " %ld %ld %*ld %*ld %*ld %*ld ", &n_jobs, &m_machines);
      tech_constraints = create_matrix (n_jobs, m_machines);
      processing_time = create_matrix (n_jobs, m_machines);
      fscanf (stream, "%*[^\n]");
      for (i = 0; i < n_jobs; i++)
        for (j = 0; j < m_machines; j++)
          fscanf (stream, " %ld ", &processing_time[i][j]);
      fscanf (stream, "%*[^\n]");
      for (i = 0; i < n_jobs; i++)
        for (j = 0; j < m_machines; j++)
          fscanf (stream, " %ld ", &tech_constraints[i][j]);
      problem = init_jobshop (n_jobs, m_machines, tech_constraints, processing_time, type);
      return problem;
    }
  else if (type == orlibrary)
    {
      fscanf (stream, "%*[^\n]");
      fscanf (stream, "%ld %ld", &n_jobs, &m_machines);
      tech_constraints = create_matrix (n_jobs, m_machines);
      processing_time = create_matrix (n_jobs, m_machines);
      for (i = 0; i < n_jobs; i++)
        for (j = 0; j < m_machines; j++)
          {
            fscanf (stream, " %ld ", &tech_constraints[i][j]);
            fscanf (stream, " %ld ", &processing_time[i][j]);
          }
      problem = init_jobshop (n_jobs, m_machines, tech_constraints, processing_time, type);
      return problem;
    }
  return NULL;
}

#endif

