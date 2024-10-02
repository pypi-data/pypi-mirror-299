import unittest
from unittest.mock import MagicMock, PropertyMock

import numpy as np
from palaestrai.agent import ActuatorInformation, SensorInformation
from palaestrai.types import Box
from palaestrai_mosaik.config import AGENT_FULL_ID
from palaestrai_mosaik.environment import MosaikInterfaceComponent
from palaestrai_mosaik.environment.mosaik_ifs import check_value, restore_value


class TestMosaikInterfaceComponent(unittest.TestCase):
    def setUp(self):
        self.sen_infos = [
            {
                "uid": "MySim-0.MyMod-0.attr",
                "space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            },
            SensorInformation(
                value=0,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-0.MyMod-1.attr",
            ),
            {
                "uid": "MySim-1.MyMod-0.attr",
                "space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            },
            SensorInformation(
                value=0,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-1.MyMod-1.attr",
            ),
        ]
        self.act_infos = [
            ActuatorInformation(
                value=None,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-0.MyMod-0.attr2",
            ),
            {
                "uid": "MySim-0.MyMod-1.attr2",
                "space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            },
            {
                "uid": "MySim-1.MyMod-0.attr2",
                "space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            },
        ]

        self.new_acts = [
            ActuatorInformation(
                value=0.2,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-0.MyMod-0.attr2",
            ),
            ActuatorInformation(
                value=0.2,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-0.MyMod-1.attr2",
            ),
            ActuatorInformation(
                value=0.2,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-1.MyMod-0.attr2",
            ),
            ActuatorInformation(
                value=0.4,
                space=Box(0, 1, (1,), np.float32),
                uid="MySim-0.MyMod-0.attr2",
            ),
        ]

    def test_create_sensors(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)

        sensors = mifs.create_sensors()

        self.assertIsInstance(sensors, list)
        self.assertEqual(4, len(sensors))
        for sen in sensors:
            self.assertIsInstance(sen, SensorInformation)
            self.assertIsInstance(sen.space, Box)
            self.assertTrue(sen.space.contains(sen.value))

    def test_trigger_sensors(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)
        sensors = mifs.create_sensors()

        df_cache = {
            0: {
                "MySim-0": {
                    "MyMod-0": {"attr": 0.5},
                    "MyMod-1": {"attr": 0.5},
                },
                "MySim-1": {
                    "MyMod-0": {"attr": 0.5},
                    "MyMod-1": {"attr": 0.5},
                },
            }
        }
        world = MagicMock()
        type(world)._df_cache = PropertyMock(return_value=df_cache)

        mifs.trigger_sensors(world, 0)

        self.assertEqual(len(sensors), len(mifs.sensors))
        for new_sen in mifs.sensors:
            match = False
            for old_sen in sensors:
                if new_sen.uid == old_sen.uid:
                    match = True
                    self.assertNotEqual(
                        new_sen.value, old_sen.value
                    )
                    break
            self.assertTrue(match)

    def test_get_sensor_readings(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)
        sensors = mifs.create_sensors()

        readings = mifs.get_sensor_readings()

        self.assertEqual(len(sensors), len(readings))
        for sen, reading in zip(sensors, readings):
            self.assertEqual(sen.uid, reading.uid)
            self.assertEqual(sen.value, reading.value)
            self.assertEqual(sen.space, reading.space)

    def test_create_actuators(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)

        actuators = mifs.create_actuators()

        self.assertIsInstance(actuators, list)
        self.assertEqual(3, len(actuators))
        for act in actuators:
            self.assertIsInstance(act, ActuatorInformation)
            self.assertIsInstance(act.space, Box)
            self.assertIsNone(act.value)

    def test_update_actuators(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)

        mifs.create_actuators()
        mifs.update_actuators(self.new_acts)

        expected = [0.2, 0.2, 0.2, 0.4]

        for idx, actuator in enumerate(mifs.actuators):
            self.assertEqual(expected[idx], actuator.value)

    def test_trigger_actuators(self):
        mifs = MosaikInterfaceComponent(self.sen_infos, self.act_infos, 0)

        mifs.create_actuators()
        mifs.update_actuators(self.new_acts)

        sim = MagicMock()
        type(sim).sid = PropertyMock(return_value="MySim-0")
        input_data = dict()
        with self.assertLogs("palaestrai_mosaik.environment", "DEBUG") as cm:
            mifs.trigger_actuators(sim, input_data)

        self.assertIn("more than one agent", cm.output[-1])

        for eid, attrs in input_data.items():
            self.assertIsInstance(attrs, dict)
            for attr, src_ids in attrs.items():
                self.assertIsInstance(src_ids, dict)
                for src_id, val in src_ids.items():
                    self.assertEqual(AGENT_FULL_ID, src_id)
                    self.assertEqual(0.2, val)  # Depends on the seed!

    def test_check_value(self):
        value = {
            "MyKey": "my_value",
            "My2ndKey": {
                "MySubKey": 0,
            },
        }

        checked = check_value(value)
        self.assertIsInstance(checked, str)

    def test_restore_value(self):
        value1 = '{"MyKey": "my_value", "My2ndKey": {"MySubKey": 0}}'
        value2 = "Just a string"
        restored1 = restore_value(value1)
        restored2 = restore_value(value2)
        self.assertIsInstance(restored1, dict)
        self.assertIsInstance(restored2, str)


if __name__ == "__main__":
    unittest.main()
