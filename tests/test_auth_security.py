import unittest

from app.auth.security import hash_password, verify_password


class TestPasswordSecurity(unittest.TestCase):

    def test_password_is_hashed(self):
        password = "MtaaFixSecure123"

        hashed = hash_password(password)

        self.assertNotEqual(password, hashed)

    def test_correct_password_is_verified(self):
        password = "MtaaFixSecure123"
        hashed = hash_password(password)

        self.assertTrue(verify_password(password, hashed))

    def test_incorrect_password_is_rejected(self):
        hashed = hash_password("MtaaFixSecure123")

        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_empty_password_is_rejected(self):
        with self.assertRaises(ValueError):
            hash_password("")

    def test_password_hash_is_not_plain_text(self):
        password = "MySecretPassword123"
        hashed = hash_password(password)

        self.assertNotEqual(password, hashed)


if __name__ == "__main__":
    unittest.main()
