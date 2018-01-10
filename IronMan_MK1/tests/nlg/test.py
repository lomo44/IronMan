import unittest
from IronMan_MK1.modules.nlg.IM_NLG_Module import IM_NLG_Module
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
class test_nlg(unittest.TestCase):
    def setUp(self):
        self.nlg_module = IM_NLG_Module()
        pass
    def test_basic_integrity(self):
        test_recipe = NLG_Recipe()
        test_recipe.add_subject("I")
        test_recipe.add_object("you")
        test_recipe.attribute["preference"] = 0.5
        test_recipe.attribute["verbal_strength"] = 1.5
        final_str = self.nlg_module.realization(test_recipe)
        self.assertTrue(final_str == "Well, I really like you" or final_str == "Tell you what, I really like you" )
    def test_recipe_generate_subjects(self):
        test_recipe = NLG_Recipe()
        test_recipe.add_subject("I")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "I")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("you")
        test_recipe.add_subject("Mary")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "you and Mary")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("you")
        test_recipe.add_subject("I")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "you and I")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("I")
        test_recipe.add_subject("you")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "you and I")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("Mary")
        test_recipe.add_subject("you")
        test_recipe.add_subject("John")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "Mary, you and John")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("Mary")
        test_recipe.add_subject("you")
        test_recipe.add_subject("I")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "Mary, you and I")

        test_recipe = NLG_Recipe()
        test_recipe.add_subject("I")
        test_recipe.add_subject("Mary")
        test_recipe.add_subject("you")
        result = test_recipe.generate_subjects()
        self.assertEqual(result, "Mary, you and I")

    def test_recipe_generate_objects(self):
        test_recipe = NLG_Recipe()
        test_recipe.add_object("me")
        result = test_recipe.generate_objects()
        self.assertEqual(result,"me")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("Mary")
        test_recipe.add_object("John")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "Mary and John")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("her")
        test_recipe.add_object("me")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "her and me")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("me")
        test_recipe.add_object("her")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "her and me")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("Mary")
        test_recipe.add_object("John")
        test_recipe.add_object("Sally")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "Mary, John and Sally")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("Mary")
        test_recipe.add_object("her")
        test_recipe.add_object("me")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "Mary, her and me")

        test_recipe = NLG_Recipe()
        test_recipe.add_object("me")
        test_recipe.add_object("Mary")
        test_recipe.add_object("her")
        result = test_recipe.generate_objects()
        self.assertEqual(result, "Mary, her and me")
    def test_template_selection(self):
        pass
if __name__ == "__main__":
    unittest.main()