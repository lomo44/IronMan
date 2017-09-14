import unittest
from marvel_wikia_module import get_marvel_basic_info,marvel_hero_name


class test_marvel_wikia_module(unittest.TestCase):
    def test_unknown_type(self):
        iron_man_info = get_marvel_basic_info(0)
        self.assertIsInstance(iron_man_info, dict)
        self.assertDictEqual(iron_man_info, {})

    def test_iron_man(self):
        iron_man_info = get_marvel_basic_info(marvel_hero_name.eMarvel_Hero_Iron_Man)
        self.assertIsInstance(iron_man_info,dict)
        self.assertNotEqual(iron_man_info,{})
        self.assertListEqual(['Anthony Edward "Tony" Stark'],iron_man_info['Real Name'])

    def test_captain_america(self):
        iron_man_info = get_marvel_basic_info(marvel_hero_name.eMarvel_Hero_Captain_America)
        self.assertIsInstance(iron_man_info,dict)
        self.assertNotEqual(iron_man_info,{})
        self.assertListEqual(['Steven "Steve" Grant Rogers'],iron_man_info['Real Name'])


if __name__ == "__main__":
    unittest.main()