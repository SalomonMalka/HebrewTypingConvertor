import unittest
from layout_fixer import translate_text, contains_hebrew

class TestLayoutTranslator(unittest.TestCase):
    def test_contains_hebrew(self):
        self.assertTrue(contains_hebrew("שלום"))
        self.assertTrue(contains_hebrew("hello שלום"))
        self.assertFalse(contains_hebrew("hello"))
        self.assertFalse(contains_hebrew("12345!@#"))

    def test_english_to_hebrew(self):
        # Normal lowercase English to Hebrew
        self.assertEqual(translate_text("hello"), "יקךךם")
        self.assertEqual(translate_text("vello"), "הקךךם")
        self.assertEqual(translate_text("akuo"), "שלום")
        
        # Capitals (Shifted) English to Hebrew layout
        self.assertEqual(translate_text("HElLO"), "יקךךם")
        
        # Spaces and punctuation
        self.assertEqual(translate_text("hello world!"), "יקךךם 'םרךג!")

    def test_hebrew_to_english(self):
        # Hebrew to English
        self.assertEqual(translate_text("הקךךם"), "vello")
        self.assertEqual(translate_text("יקךךם"), "hello")
        self.assertEqual(translate_text("שלום"), "akuo")
        
        # Mixed and punctuation
        self.assertEqual(translate_text("שלום מה שלומך?"), "akuo nv akunl?")

if __name__ == "__main__":
    unittest.main()
