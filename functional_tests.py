from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User wants to visit the home page of the todo list application
        self.browser.get('http://localhost:8000/')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # She is now greeted with another empty text box in order to enter another item
        # She enters 'Use peacock feathers to make a fly.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page updates again, now showing two items.
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        
        # Edith wonders if the site will remember her lists 
        # She notices that the site shows a unique url and some explanatory text
        
        self.fail('Finish the test!')
        # She visits that url and notices that her todo list was saved
        # Satisfied, she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')