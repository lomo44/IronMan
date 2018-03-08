import unittest
from IronMan_MK1.modules.nlg.IM_NLG_Module import IM_NLG_Module
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
class NLGTestCases(unittest.TestCase):
    def setUp(self):
        self.nlg_module = IM_NLG_Module(json_file="IronMan_MK1/modules/nlg/iron_man_data2.json")
        pass

    def testBase(self):
        test_recipe = NLG_Recipe("opinion")
        test_recipe.AddContents({"subject": ["I"], "object": ["you"]})
        test_recipe.AddAttribute("assertion", True)
        test_recipe.AddAttribute("preferences", False)


    def testRecipeGenerateClauses(self):
        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject": ["I"]})
        self.assertEqual(test_recipe.GetContents(), {"subject":"I"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject": ["David"]})
        self.assertEqual(test_recipe.GetContents(), {"subject": "David"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["I", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "Mary and I"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["me", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "Mary and me"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["David", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David and Mary"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["I", "David", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and I"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["David", "I", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and I"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["David", "Mary", "I"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and I"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["me", "David", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and me"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["David", "me", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and me"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["David", "Mary", "me"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "David, Mary and me"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject:": ["Steven", "David", "Mary"]})
        self.assertEqual(test_recipe.GetContents(), {"subject:": "Steven, David and Mary"})

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"subject": ["Peter"], "subject2": ["Tom","I"], "subject3": ["Steven", "David", "Mary"], "object": ["her", "me"]})
        self.assertEqual(test_recipe.GetContents(), {"subject": "Peter", "subject2": "Tom and I", "subject3": "Steven, David and Mary", "object": "her and me"})

    def testRealizationPositiveTests(self):
        test_recipe = NLG_Recipe("greetings")
        results = self.nlg_module.Realization(test_recipe, "templates")
        
        test_recipe = NLG_Recipe("initialization")
        test_recipe.AddDescriptor("question", "What would you do if you were me?")
        results = self.nlg_module.Realization(test_recipe, "templates")

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents({"content": ["Pepper", "I"]})
        test_recipe.AddAttribute("assertion", True)
        results = self.nlg_module.Realization(test_recipe, "templates")

        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents({"content": "burgers"})
        test_recipe.AddAttribute("preference", True)
        results = self.nlg_module.Realization(test_recipe, "templates")

        test_recipe = NLG_Recipe("opinion")
        test_recipe.AddContents({"topic": ["Climate change"], "content": ["happening"]})
        results = self.nlg_module.Realization(test_recipe, "templates")

        test_recipe = NLG_Recipe("experience")
        test_recipe.AddDescriptor("experience", "I don't know how to drive!")
        test_recipe.AddDescriptor("opinion", "Personally, I think driving is really hard")
        results = self.nlg_module.Realization(test_recipe, "templates")

    def testRealizationNegativeTests(self):
        test_recipe = NLG_Recipe("invalid intent")
        results = self.nlg_module.Realization(test_recipe, "templates")
        self.assertEqual([], results)

        test_recipe = NLG_Recipe("experience")
        results = self.nlg_module.Realization(test_recipe, "templates")
        self.assertEqual([], results)

        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents({"content": "burgers"})
        test_recipe.AddAttribute("preference", True)
        test_recipe.AddAttribute("seriousness", True)
        results = self.nlg_module.Realization(test_recipe, "templates")
        self.assertEqual([], results)

    def testSelectResult(self):
        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents({"content": "burgers"})
        test_recipe.AddAttribute("preference", True)
        results = self.nlg_module.Realization(test_recipe, "templates")
        result = self.nlg_module.SelectResult(test_recipe, results)

        test_recipe = NLG_Recipe("experience")
        results = self.nlg_module.Realization(test_recipe, "templates")
        result = self.nlg_module.SelectResult(test_recipe, results)




if __name__ == "__main__":
    unittest.main()