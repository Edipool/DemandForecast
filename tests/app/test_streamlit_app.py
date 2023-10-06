import unittest


class Test_streamlit_app(unittest.TestCase):
    def test_urls(self):
        with open("web_app/streamlit_app.py", "r") as file:
            lines = file.readlines()

        # Check that there are at least 5 URLS
        for line in lines:
            # If the line contains 'http://' or 'https://'
            if "http://" in line or "https://" in line:
                # Check that there is 'app' in the URL
                self.assertIn("app", line, f"URL without 'app' found: {line.strip()}")
                # Check that there is no 'localhost' in the URL
                self.assertNotIn(
                    "localhost", line, f"URL with 'localhost' found: {line.strip()}"
                )


if __name__ == "__main__":
    unittest.main()
