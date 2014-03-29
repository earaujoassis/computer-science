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

#ifndef __jobshop_criteria_h__
#define __jobshop_criteria_h__

#include "../support.h"

long int
makespan (unsigned int *jobs_index,
          jobshop_t *problem)
{
  long int i, k, penalty, makespan;
  size_t dimension;
  unsigned int job, machine, operation, *operations_vector;
  unsigned long int processing_time, *machines_values, *machines_status;

  dimension = problem->n_jobs * problem->m_machines;
  operations_vector = calloc (problem->n_jobs, sizeof (unsigned int));
  machines_values = calloc (problem->m_machines, sizeof (unsigned long int));
  machines_status = calloc (dimension, sizeof (unsigned long int));
  for (i = 0; i < dimension; i++)
    {
      penalty = -1;
      job = jobs_index[i];
      operation = operations_vector[job - 1];
      operations_vector[job - 1] += 1;
      processing_time = problem->processing_time[job - 1][operation];
      machine = problem->tech_constraints[job - 1][operation];
      if (problem->instance_type == taillard)
        machine -= 1;
      for (k = i - 1; k >= 0; k--)
        if (job == jobs_index[k])
          if (machines_status[k] > machines_values[machine])
            {
              penalty = machines_status[k] - machines_values[machine];
              machines_values[machine] += processing_time + penalty;
              machines_status[i] = machines_values[machine];
              break;
            }
      if (penalty < 0)
        {
          machines_values[machine] += processing_time;
          machines_status[i] = machines_values[machine];
        }
    }
  makespan = machines_status[0];
  for (i = 1; i < dimension; i++)
    makespan = makespan < machines_status[i] ? machines_status[i] : makespan;
  free (operations_vector);
  free (machines_values);
  free (machines_status);
  return makespan;
}

#endif

