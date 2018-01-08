import unittest
from IronMan_MK1.modules.nlg.IM_NLG_Module import IM_NLG_Module
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
class test_nlg(unittest.TestCase):
    def setUp(self):
        self.nlg_module = IM_NLG_Module()
        pass
    def test_basic_integrity(self):
        test_recipe = NLG_Recipe()
        test_recipe.add_object("I")
        test_recipe.add_subject("you")
        test_recipe.attribute["preference"] = 0.5
        final_str = self.nlg_module.realization(test_recipe)
        self.assertEqual(final_str,"I like you")


if __name__ == "__main__":
    unittest.main()