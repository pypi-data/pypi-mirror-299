# tests/test_interactive_terminal.py

import unittest
from interactive_terminal.interactive_terminal import (
    Question,
    QuestionType,
    ask_text_question,
    ask_number_question,
    ask_confirm_question,
    ask_list_question,
)

class TestInteractiveTerminal(unittest.TestCase):

    def test_ask_text_question_valid(self):
        """Test asking a text question with valid input."""
        question = Question(QuestionType.TEXT, 'username', 'What is your name?')
        
        # Simulate user input for testing
        with unittest.mock.patch('builtins.input', return_value='Alice'):
            response = ask_text_question(question)
            self.assertEqual(response, 'Alice')

    def test_ask_text_question_invalid_empty(self):
        """Test asking a text question and handling empty input."""
        question = Question(QuestionType.TEXT, 'username', 'What is your name?')

        with unittest.mock.patch('builtins.input', side_effect=['', 'Bob']):
            response = ask_text_question(question)
            self.assertEqual(response, 'Bob')

    def test_ask_number_question_valid(self):
        """Test asking a number question with valid input."""
        question = Question(QuestionType.NUMBER, 'age', 'How old are you?')

        with unittest.mock.patch('builtins.input', return_value='30'):
            response = ask_number_question(question)
            self.assertEqual(response, 30)

    def test_ask_number_question_invalid(self):
        """Test asking a number question and handling invalid input."""
        question = Question(QuestionType.NUMBER, 'age', 'How old are you?')

        with unittest.mock.patch('builtins.input', side_effect=['invalid', '25']):
            response = ask_number_question(question)
            self.assertEqual(response, 25)

    def test_ask_confirm_question(self):
        """Test confirming a question."""
        question = Question(QuestionType.CONFIRM, 'proceed', 'Do you want to proceed?')

        with unittest.mock.patch('builtins.input', side_effect=['yes', '']):
            response = ask_confirm_question(question)
            self.assertTrue(response)

        with unittest.mock.patch('builtins.input', return_value='no'):
            response = ask_confirm_question(question)
            self.assertFalse(response)

    def test_ask_list_question(self):
        """Test asking a list question."""
        question = Question(QuestionType.LIST, 'color', 'Choose your favorite color:', options=['Red', 'Green', 'Blue'])

        with unittest.mock.patch('builtins.input', return_value='1'):
            response = ask_list_question(question)
            self.assertEqual(response, 'Red')

if __name__ == '__main__':
    unittest.main()