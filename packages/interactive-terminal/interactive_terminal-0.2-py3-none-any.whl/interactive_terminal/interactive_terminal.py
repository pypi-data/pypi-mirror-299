# interactive_terminal.py

import sys
import colorama
import keyboard
from colorama import Fore, Style

colorama.init(autoreset=True)

class QuestionType:
    """Enumeration of question types for the interactive terminal."""    
    TEXT = 'text'
    LIST = 'list'
    CONFIRM = 'confirm'
    NUMBER = 'number'  # For numeric input
    RANGE = 'range'    # For a range of values
    CHOICE = 'choice'  # For selecting one option from a list


class Question:
    """Represents a question in the interactive terminal.

    Attributes:
        question_type (str): The type of question (TEXT, LIST, CONFIRM, NUMBER, RANGE, CHOICE).
        key (str): The key under which the answer will be stored.
        prompt (str): The question prompt to display to the user.
        options (list, optional): A list of options for choice or range questions.
        validate (callable, optional): A function to validate the user's input.
    """

    def __init__(self, question_type, key, prompt, options=None, validate=None):
        self.question_type = question_type
        self.key = key
        self.prompt = prompt
        self.options = options
        self.validate = validate


def ask_questions(questions):
    """Asks a series of questions and collects user responses.

    Args:
        questions (list of Question): A list of Question objects to ask the user.

    Returns:
        dict: A dictionary of user answers keyed by the question keys.
    """
    answers = {}
    for question in questions:
        if question.question_type == QuestionType.TEXT:
            answers[question.key] = ask_text_question(question)
        elif question.question_type == QuestionType.LIST:
            answers[question.key] = ask_list_question(question)
        elif question.question_type == QuestionType.CONFIRM:
            answers[question.key] = ask_confirm_question(question)
        elif question.question_type == QuestionType.NUMBER:
            answers[question.key] = ask_number_question(question)
        elif question.question_type == QuestionType.RANGE:
            answers[question.key] = ask_range_question(question)
        elif question.question_type == QuestionType.CHOICE:
            answers[question.key] = ask_choice_question(question)
            
        print('')  # Newline for spacing
    return answers


def ask_text_question(question):
    """Prompts the user with a text question and handles input with validation.

    Args:
        question (Question): The Question object containing details for the text question.

    Returns:
        str: The validated user input.
    """
    while True:
        print(format_question(question))

        # Capture user input
        input_value = input('')

        # Check for empty input
        if input_value.strip() == "":
            print(Fore.RED + "\nInput cannot be empty.\n")
            continue

        # Validate input
        is_valid, validation_message = validate_input(question, input_value)
        if is_valid:
            return input_value
        print(Fore.RED + '\n' + validation_message + '\n')


def ask_list_question(question):
    """Prompts the user with a list question and allows them to choose an item.

    Args:
        question (Question): The Question object containing details for the list question.

    Returns:
        str: The selected item from the list.
    """
    print(format_question(question))
    print("Available options:")
    for index, option in enumerate(question.options):
        print(f"{index + 1}. {option}")

    while True:
        try:
            selection = int(input("Select an option (1-{}): ".format(len(question.options)))) - 1
            if 0 <= selection < len(question.options):
                return question.options[selection]
            print(Fore.RED + "\nInvalid selection. Please try again.\n")
        except ValueError:
            print(Fore.RED + "\nPlease enter a number.\n")


def ask_confirm_question(question):
    """Prompts the user with a confirmation question.

    Args:
        question (Question): The Question object containing details for the confirmation question.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        print(format_question(question))
        input_value = input("[Y/n]: ").strip().lower()
        if input_value in ['y', 'yes', '']:
            return True
        elif input_value in ['n', 'no']:
            return False
        print(Fore.RED + "Please respond with 'y' or 'n'.")


def ask_number_question(question):
    """Prompts the user for a number input with validation.

    Args:
        question (Question): The Question object containing details for the number question.

    Returns:
        int: The validated numeric input from the user.
    """
    while True:
        print(format_question(question))
        input_value = input("Enter a number: ")

        try:
            number = int(input_value)
            is_valid, validation_message = validate_input(question, number)
            if is_valid:
                return number
            print(Fore.RED + '\n' + validation_message + '\n')
        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter a valid number.\n")


def ask_range_question(question):
    """Prompts the user for a range of numeric values.

    Args:
        question (Question): The Question object containing details for the range question.

    Returns:
        tuple: A tuple containing the validated minimum and maximum values.
    """
    while True:
        print(format_question(question))
        input_value = input("Enter the range (min-max): ")

        try:
            min_val, max_val = map(int, input_value.split('-'))
            if min_val < max_val:
                return (min_val, max_val)
            print(Fore.RED + "\nInvalid range. Minimum must be less than maximum.\n")
        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter a valid range (min-max).\n")


def ask_choice_question(question):
    """Prompts the user to choose one option from a list of choices.

    Args:
        question (Question): The Question object containing details for the choice question.

    Returns:
        str: The selected choice from the list.
    """
    print(format_question(question))
    print("Available choices:")
    for index, choice in enumerate(question.options):
        print(f"{index + 1}. {choice}")

    while True:
        try:
            selection = int(input("Select your choice (1-{}): ".format(len(question.options)))) - 1
            if 0 <= selection < len(question.options):
                return question.options[selection]
            print(Fore.RED + "\nInvalid selection. Please try again.\n")
        except ValueError:
            print(Fore.RED + "\nPlease enter a number.\n")


def format_question(question):
    """Formats the question prompt for display.

    Args:
        question (Question): The Question object containing details for the question.

    Returns:
        str: The formatted question prompt string.
    """
    question_prompt = f"[{Fore.YELLOW}?{Style.RESET_ALL}] {question.prompt}:"
    return question_prompt


def validate_input(question, current):
    """Validates the user's input based on the provided validation function.

    Args:
        question (Question): The Question object containing validation logic.
        current (str): The user's input to validate.

    Returns:
        tuple: A tuple containing a boolean indicating validity and a validation message.
    """
    if question.validate:
        return question.validate([], current)
    return True, ""