import unittest

from modules.wit_ai_module import wit_ai_module, wit_ai_context


class test_wit_ai(unittest.TestCase):
    def setUp(self):
        self.wit_context = wit_ai_context("KQPROP4YWPPURXOOT6U3FCY4APDGXC2H","NUZVZ5V2JWA5RXMYSHROS74C4KG7VPZM")
        self.wit_module = wit_ai_module(self.wit_context)
    def test_get_entities(self):
        entities = self.wit_module.get_all_entities()
        self.assertNotEqual(entities,None)
    def test_get_entity_value(self):
        values = self.wit_module.get_entity_values('kobe_object')
        self.assertNotEqual(values,None)

if __name__ == "__main__":
    unittest.main()