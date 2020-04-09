import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # User wants to visit the home page of the todo list application
        self.browser.get(self.live_server_url)

        # She notices the page header and title mention To-Do lists!
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a todo item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Enter a to-do item'
        )

        # She types 'Buy peacock feathers' into the text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates to show:
        # "1: Buy Peacock Feathers" as an item in her todo list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She is now greeted with another empty text box in order to enter another item
        # She enters 'Use peacock feathers to make a fly.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # the page updates again, now showing two items.
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        
        # Edith wonders if the site will remember her lists 
        # She notices that the site shows a unique url and some explanatory text
        
        # She visits that url and notices that her todo list was saved
        # Satisfied, she goes to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Editth vistis todolist website.
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that the site shows a unique url and some explanatory text
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis decides to visit the todolist website. There is no sign of Edith's items.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # She decides to add an item to her list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # The page updates and she sees the item she entered
        self.wait_for_row_in_list_table('1: Buy milk')

        # She notices that she has a unique url
        francis_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists.+')
        self.assertNotEqual(edith_url, francis_url)

        # Again, no sign of Edith's items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
