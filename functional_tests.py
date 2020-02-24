from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User wants to visit the home page of the todo list application
        self.browser.get('http://localhost:8000/')

        # She notices the page title has 'To-Do' in it
        self.assertIn("To-Do", self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a todo item right away
        # She types 'Buy peacock feathers' into the text box

        # When she hits enter, the page updates to show:
        # "1: Buy Peacock Feathers" as an item in her todo list

        # She is now greeted with another empty text box in order to enter another item
        # She enters 'Use peacock feathers to make a lure.

        # the page updates again, now showing two items.

        #Edith wonders if the site will remember her lists 
        #She notices that the site shows a unique url and some explanatory text
        # She visits that url and notices that her todo list was saved
        # Satisfied, she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')