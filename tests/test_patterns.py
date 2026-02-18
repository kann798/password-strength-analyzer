import unittest
from app.core_logic import evaluate_password


class TestPasswordStrength(unittest.TestCase):

    def test_weak_password(self):
        strength, _, _, _, _ = evaluate_password("abc")
        self.assertEqual(strength, "Weak")

    def test_medium_password(self):
        strength, _, _, _, _ = evaluate_password("abc12345")
        self.assertEqual(strength, "Medium")

    def test_strong_password(self):
        strength, _, _, _, _ = evaluate_password("Abc@1234")
        self.assertEqual(strength, "Strong")

    def test_no_uppercase(self):
        strength, _, _, _, _ = evaluate_password("abc@1234")
        self.assertNotEqual(strength, "Strong")

    def test_short_password(self):
        strength, _, _, _, _ = evaluate_password("A@1a")
        self.assertEqual(strength, "Weak")

    def test_only_letters(self):
        strength, _, _, _, _ = evaluate_password("Abcdefgh")
        self.assertEqual(strength, "Medium")


if __name__ == "__main__":
    unittest.main()
