import unittest

from api.auth.password import hash_password

class PasswordTest(unittest.TestCase):
    def test_password(self):
        self.assertEqual(hash_password("password123"), b'$2b$12$wsyxh9HogoHWD6Sp1EmhSeKeBwC5zrsdxHFo87ZwGSPxzuwtwlZY6')

if __name__ == '__main__':
    unittest.main()
    