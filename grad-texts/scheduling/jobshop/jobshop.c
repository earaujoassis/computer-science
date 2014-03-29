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

#include "utils/settings.h"
#include "utils/repr/rkey.h"
#include "utils/instances/exercise.h"

int
main (int argc, char **argv)
{
  int i;
  set_options (argc, argv);
  if (exercises_executor (argc, argv))
    return;
  instance_t instance_type = input_type (argc, argv);
  algorithm_t alg_type = algorithm_type (argc, argv); /*
  if (!feof (stdin)) TODO Not working
    return; */
  if (instance_type == taillard)
    for (i = 0; i < TAILLARD_N_INSTANCES; i++)
      fetch_execute (stdin, instance_type, alg_type);
  else
    fetch_execute (stdin, instance_type, alg_type);
  destroy_options ();
}

