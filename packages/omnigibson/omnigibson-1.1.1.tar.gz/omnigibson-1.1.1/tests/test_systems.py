import pytest
from utils import SYSTEM_EXAMPLES, og_test

import omnigibson as og
from omnigibson.object_states import Covered
from omnigibson.systems import *


@og_test
def test_system_clear(env):
    breakfast_table = env.scene.object_registry("name", "breakfast_table")
    for system_name, system_class in SYSTEM_EXAMPLES.items():
        for _ in range(3):
            system = env.scene.get_system(system_name)
            assert isinstance(system, system_class)
            if issubclass(system_class, VisualParticleSystem):
                assert breakfast_table.states[Covered].set_value(system, True)
            else:
                system.generate_particles(positions=[[0, 0, 1]])
            assert system.n_particles > 0
            og.sim.step()
            env.scene.clear_system(system_name)
