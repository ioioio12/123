import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class UserCRUDTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_crud_operations(self):
        driver = self.driver
        driver.get(f"{self.base_url}/users_view")

        name_input = driver.find_element(By.NAME, "name")
        name_input.send_keys("Test User")
        add_button = driver.find_element(By.CSS_SELECTOR, "form[action='/add_user'] button")
        add_button.click()

        time.sleep(1)

        self.assertIn("Test User", driver.page_source)

        user_list_items = driver.find_elements(By.TAG_NAME, "li")
        user_id = None
        for item in user_list_items:
            if "Test User" in item.text:
                user_id = item.text.split(" - ")[0].strip()
                break

        self.assertIsNotNone(user_id, "Пользователь не найден")

        import requests
        response = requests.put(f"{self.base_url}/users/{user_id}", json={"name": "Updated User"})
        self.assertEqual(response.status_code, 200)

        driver.get(f"{self.base_url}/users_view")
        time.sleep(1)
        self.assertIn("Updated User", driver.page_source)

        delete_button = driver.find_element(By.CSS_SELECTOR, f"form[action='/delete_user/{user_id}'] button")
        delete_button.click()
        time.sleep(1)

        self.assertNotIn("Updated User", driver.page_source)


if __name__ == '__main__':
    unittest.main()
