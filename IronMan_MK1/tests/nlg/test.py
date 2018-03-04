import unittest
from IronMan_MK1.modules.nlg.IM_NLG_Module import IM_NLG_Module
from IronMan_MK1.modules.base.nlg_recipe import NLG_Recipe
class test_nlg(unittest.TestCase):
    def setUp(self):
        self.nlg_module = IM_NLG_Module(json_file="IronMan_MK1/modules/nlg/iron_man_data2.json")
        pass

    def testBase(self):
        test_recipe = NLG_Recipe("opinion")
        test_recipe.AddContents([["I"],["you"]])
        test_recipe.AddAttribute("assertion", True)
        test_recipe.AddAttribute("preferences", False)


    def testRecipeGenerateClauses(self):
        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["I"]])
        self.assertEqual(test_recipe.GetContents(), ["I"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David"]])
        self.assertEqual(test_recipe.GetContents(), ["David"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["I", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["Mary and I"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["me", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["Mary and me"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["David and Mary"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["I", "David", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and I"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David", "I", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and I"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David", "Mary", "I"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and I"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["me", "David", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and me"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David", "me", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and me"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["David", "Mary", "me"]])
        self.assertEqual(test_recipe.GetContents(), ["David, Mary and me"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["Steven", "David", "Mary"]])
        self.assertEqual(test_recipe.GetContents(), ["Steven, David and Mary"])

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["Peter"], ["Tom","I"], ["Steven", "David", "Mary"], ["her", "me"]])
        self.assertEqual(test_recipe.GetContents(), ["Peter", "Tom and I", "Steven, David and Mary", "her and me"])

    def testRealizationPositiveTests(self):
        test_recipe = NLG_Recipe("greetings")
        results = self.nlg_module.Realization(test_recipe)
        
        test_recipe = NLG_Recipe("initialization")
        test_recipe.AddDescriptor("question", "What would you do if you were me?")
        results = self.nlg_module.Realization(test_recipe)

        test_recipe = NLG_Recipe("person")
        test_recipe.AddContents([["Pepper", "I"]])
        test_recipe.AddAttribute("assertion", True)
        results = self.nlg_module.Realization(test_recipe)

        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents(["burgers"])
        test_recipe.AddAttribute("preference", True)
        results = self.nlg_module.Realization(test_recipe)

        test_recipe = NLG_Recipe("opinion")
        test_recipe.AddContents([["Climate change"], ["happening"]])
        results = self.nlg_module.Realization(test_recipe)

    def testRealizationNegativeTests(self):
        test_recipe = NLG_Recipe("invalid intent")
        results = self.nlg_module.Realization(test_recipe)
        self.assertEqual([], results)

        test_recipe = NLG_Recipe("experience")
        results = self.nlg_module.Realization(test_recipe)
        self.assertEqual([], results)

        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents(["burgers"])
        test_recipe.AddAttribute("preference", True)
        test_recipe.AddAttribute("seriousness", True)
        results = self.nlg_module.Realization(test_recipe)
        self.assertEqual([], results)

    def testSelectResult(self):
        test_recipe = NLG_Recipe("preference")
        test_recipe.AddContents(["burgers"])
        test_recipe.AddAttribute("preference", True)
        results = self.nlg_module.Realization(test_recipe)
        result = self.nlg_module.SelectResult(test_recipe, results)

        test_recipe = NLG_Recipe("experience")
        results = self.nlg_module.Realization(test_recipe)
        result = self.nlg_module.SelectResult(test_recipe, results)




if __name__ == "__main__":
    unittest.main()