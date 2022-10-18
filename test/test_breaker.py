import os
import unittest
import sys

SRC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src'
sys.path.append(SRC_FOLDER)

import Breaker, contextlib, os

fetcher = Breaker.Fetcher("test@gmail.com", True)

class HaveBeenPwnedTests(unittest.TestCase):
    def test_pwned_true(self):
        self.assertEqual(Breaker.CheckPwned.check_pwned("admin@admin.com"), True)
    def test_pwned_false(self):
        self.assertEqual(Breaker.CheckPwned.check_pwned("falseemail@randomdomainthatdoesnotexist.com"), False)

class HashesTests(unittest.TestCase):
    def test_csrf_token(self):
        csrf_token_length = 32
        self.assertEqual(len(Breaker.Hashes.get_csrf_token()), csrf_token_length)
    def test_dehash_decrypt(self):
        hash = "7110eda4d09e062aa5e4a390b0a572ac0d2c0220"
        result_hash = "1234"
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            self.assertEqual(Breaker.Hashes.dehash(hash, 's'), hash + ':' + result_hash)
    def test_dehash_no_decrypt(self):
        hash = "d033e22ae348aeb5660fc2140aec35850c4da997"
        result_hash = "d033e22ae348aeb5660fc2140aec35850c4da997"
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            self.assertEqual(Breaker.Hashes.dehash(hash, 'n'), result_hash)

class FetcherTests(unittest.TestCase):
    def test_counts(self):
        fetcher.check_tries()
        self.assertEqual(fetcher.current_tries, 1)
        fetcher.check_tries()
        self.assertEqual(fetcher.current_tries, 2)
    def test_pattern(self):
        self.assertEqual(fetcher.pattern, "test@gmail.com")
    def test_max_tries(self):
        FETCHER_TRIES = Breaker.SOFTWARE_CONFIG.MAX_TRIES
        self.assertEqual(fetcher.max_tries, int(FETCHER_TRIES))
    def test_software_hash_email(self):
        HASH_DATA = len(Breaker.SOFTWARE_CONFIG.MD5_DECRYPT_EMAIL) not in [0, None]
        self.assertEqual(HASH_DATA, True)
    def test_software_hash_password(self):
        HASH_DATA = len(Breaker.SOFTWARE_CONFIG.MD5_DECRYPT_PASSWORD) not in [0, None]
        self.assertEqual(HASH_DATA, True)
    def test_source(self):
        self.assertEqual(fetcher.source, "https://breachdirectory.org/usersearch.php?term=")
    def test_google_captcha_anchor_url(self):
        self.assertEqual(fetcher.google_anchor_url, "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcdcfIUAAAAACF6YXBGfZeWvtOz3BbZB667xkj8&co=aHR0cHM6Ly9icmVhY2hkaXJlY3Rvcnkub3JnOjQ0Mw..&hl=es&v=vP4jQKq0YJFzU6e21-BGy3GP&size=invisible&cb=jtbjuddi4p5c")


if __name__ == '__main__':
    unittest.main()