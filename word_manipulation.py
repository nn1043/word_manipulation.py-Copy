"""
word_manipulation.py
This is a python file that takes in words.csv and various .txt files to output
relevant information to the user.
Patrick Azzo & Nicholas Noboa
Created 11/20/19
Updated 12/16/19
"""

global words_by_rank
words_by_rank = {}

global temp_foreign_common_words
temp_foreign_common_words = {}

global parts_of_speech
parts_of_speech = {
    "a": [], "v": [], "c": [], "i": [], "t": [], "p": [], "d": [], "x": [],
    "r": [], "m": [], "n": [], "e": [], "j": [], "u": []
    }


def english_setup(filename):
    """
This function extracts data from the words5000.csv files and places it into
usuable global variables. This function is run automatically when the program
is started.
Uses several strings as placeholders for data obtained from words5000.csv
before they are inputted into words_by_rank, a global dictionary comprised of
lists as values, and parts_of_speech, a global dictionary that divides the
words by their respective parts of speech.
    """
    rank_temp = ""
    word_temp = ""
    speech_temp = ""
    freq_temp = ""
    disp_temp = ""

    survey = open(filename, "r")
    for line in survey.readlines():
        survey_readable = line.split(",")   # splits apart the file to prep
        for value in survey_readable:       # for data movement
            if survey_readable.index(value) == 0:   # word rank
                rank_temp = value
            if survey_readable.index(value) == 1:   # word
                word_temp = value
            if survey_readable.index(value) == 2:   # part of speech
                speech_temp = value
                for key in parts_of_speech:
                    if key == value:
                        parts_of_speech[key].append(word_temp)
            if survey_readable.index(value) == 3:   # frequency
                freq_temp = value
            if survey_readable.index(value) == 4:   # dispersion
                disp_temp = value
                words_by_rank[rank_temp] = [
                    word_temp, rank_temp, speech_temp, freq_temp, disp_temp
                ]   # this puts together the global dictionary to be used
    survey.close()
    words_by_rank.pop("Rank", None)
    print("English loaded.")


###############################################################################
def most_common_by_parts_of_speech():
    """
This function allows the user to determine which part of speech they want to
investigate and how many of the most common words they want returned.
Uses rank_temp to hold data before moving it to end_result, both lists. Makes
use of user inputs as strings to search parts_of_speech, a global list. A
dictionary is used for user experience purposes, translating parts of speech
abbreviations to the full word(s). Various data transformation variables are
also used. A list, end_result, is outputted to the user.
    """
    end_result = []
    rank_temp = []
    print(
        "Parts of speech: article (a), verb (v), conjunction (c), " +
        "preposition (i), infinitive (t), pronoun (p), pronoun (d), " +
        "not or n't (x), adverb (r), number (m), noun (n), there (e), " +
        "adjective (j), interjection (u)."
        )
    if testing_on is True:  # bypass user input while test_cases() is running
        search_parts_of_speech = test_speech_input
        number_words = test_speech_numbers
    else:
        search_parts_of_speech = input("What part of speech: ")
        number_words = input("How many words: ")
    counter = int(number_words)
    print_translation = {
        "a": "article", "v": "verb", "c": "conjunction", "i": "preposition",
        "t": "infinitive", "p": "pronoun", "d": "pronoun", "x": "not or n't",
        "r": "adverb", "m": "number", "n": "noun", "e": "there",
        "j": "adjective", "u": "interjection"
        }   # dictionary used to translate user input to readable print output
    if search_parts_of_speech in parts_of_speech:
        rank_temp = parts_of_speech[search_parts_of_speech]
        for rank in rank_temp:
            if counter > 0:
                end_result.append(rank)
                counter = counter - 1
            else:
                pass
        print(
            "The " + number_words + " most common words that belong to the '"
            + print_translation[search_parts_of_speech] +
            "' part of speech are:"
            )
        print(end_result)
    else:
        print("Not a part of speech.")  # exception handler


###############################################################################
def usage_percent():
    """
This function allows the user to view how many times the top x number of words
are used in comparison to the bottom y number of words. This includes both the
frequency numbers and an accurate percentage usage.
Uses a variety of integers and strings to hold temporary information before
performing several calculations and outputting the data to the user in a
readable string format.
    """
    top_percent = 0
    bottom_percent = 0
    counter = 0

    if testing_on is True:
        str_words_to_check = test_usage
    else:
        str_words_to_check = input("How many words: ")

    words_to_check = int(str_words_to_check) - 1    # math and data management
    int_words_not_checked = 5000 - int(str_words_to_check)
    str_words_not_checked = str(int_words_not_checked)

    for rank in words_by_rank:
        for info in words_by_rank[rank]:
            if words_by_rank[rank].index(info) == 3:
                word_usage = int(info)
                if counter <= words_to_check:   # while below input number, add
                    top_percent = top_percent + word_usage
                    counter = counter + 1
                else:   # otherwise, send value to 'other' variable
                    bottom_percent = bottom_percent + word_usage
    total_usage = top_percent + bottom_percent  # various math to prep output
    top_percent_worth = (top_percent / total_usage) * 100
    response_top_percent = str(top_percent)
    response_bottom_percent = str(bottom_percent)
    response_top_percent_worth = str(top_percent_worth)
    print(
        "The top " + str_words_to_check + " words are used "
        + response_top_percent + " times."
        )
    print(
        "The bottom " + str_words_not_checked + " words are used "
        + response_bottom_percent + " times."
        )
    print(
        "The top " + str_words_to_check + " words account for "
        + response_top_percent_worth + "% of all English words used."
        )


###############################################################################
def foreign_word_list():
    """
This function parses the chosen text file and preps a global dictionary for use
in compare_foreign_english().
Uses user input to decide which .txt file is to be parsed and inputted into the
global variable temp_foreign_common_words, which is later used by
compare_foreign_english. Data transformation is similar to that of
english_setup.
    """
    usable_languages = ["SPANISH", "FRENCH", "GERMAN", "RUSSIAN", "JAPANESE"]
    rank_temp = ""
    foreign_temp = ""
    print("Available languages: Spanish, French, German, Russian, Japanese.")
    make_choice = True
    while make_choice is True:
        global filename     # prep for usage in other functions
        if testing_on is True:
            filename = test_language_load
        else:
            filename = input("Language: ")
        if filename.upper() not in usable_languages:    # exception handler
            print("Not a valid language.")
        else:
            make_choice = False
            language_file = filename + ".txt"   # file prep
            language = open(language_file, "r")
            for line in language.readlines():
                language_readable = line.split()
                for word in language_readable:  # build new dictionary
                    if language_readable.index(word) == 0:   # word rank
                        rank_temp = word
                    if language_readable.index(word) == 1:   # foreign word
                        foreign_temp = word
                    if language_readable.index(word) == 2:   # English word
                        temp_foreign_common_words[rank_temp] = [
                            foreign_temp, word, rank_temp
                            ]
    print(filename.upper() + " loaded.")    # no output to user, background use


###############################################################################
def compare_foreign_english():
    """
This function parses the global dictionary words_by_rank using the global
dictionary temp_foreign_common_words to find the appropriate English words,
and returns them in a readable format to the user.
Takes in the global dictionary temp_foreign_common_words, parses through it,
and returns to the user the data in a legible string-concatenated print. Data
is held in lists prior to output.
    """
    to_compare = []     # English word taken from foreign language list
    temp_foreign = []   # Foreign word saved from foreign language list
    counter = 20    # Counter to hold how many words to compare
    response_counter = 0
    for rank in temp_foreign_common_words:
        for value in temp_foreign_common_words[rank]:
            if counter > 0:
                if temp_foreign_common_words[rank].index(value) == 0:  # for.
                    temp_foreign.append(value)
                if temp_foreign_common_words[rank].index(value) == 1:  # eng.
                    to_compare.append(value)
                    counter = counter - 1
    print(
        "The twenty the most common words in the " + filename.upper() +
        " language and their corresponding English words are..."
        )
    for word in temp_foreign:
        number_output = str(response_counter + 1)
        print(
            filename.upper() + ": " + number_output + " " +
            temp_foreign[response_counter] + "| English: " +
            to_compare[response_counter]
        )
        response_counter = response_counter + 1


###############################################################################
def task_manager():
    """
This function allows the user to select functions and use the program as a
whole. User interface for the program.
User inputs are taken in, and the respective functions are loaded. There are no
dedicated outputs from this function.
    """
    run_program = True
    while run_program is True:
        print("What would you like to do?")
        print("MENU |")
        user_response = input("Selection: ")
        if user_response.upper() == "MENU":
            print("Load Foreign Language (LOAD) |")
            print("Compare Foreign Language (COMPARE) |")
            print("View Usage by Ranking (USAGE)")
            print("Most Common by Parts of Speech (SPEECH) |")
            print("Run Test Cases (TEST) |")
            print("Exit Program (EXIT) |")
        elif user_response.upper() == "LOAD":
            foreign_word_list()
        elif user_response.upper() == "COMPARE":
            if temp_foreign_common_words == {}:
                print("No language set. Please choose LOAD.")
            else:
                compare_foreign_english()
        elif user_response.upper() == "USAGE":
            usage_percent()
        elif user_response.upper() == "SPEECH":
            most_common_by_parts_of_speech()
        elif user_response.upper() == "TEST":
            test_cases()
        elif user_response.upper() == "EXIT":
            print("Goodbye.")
            run_program = False
        elif user_response.upper() == "QUIT":
            print("Goodbye.")
            run_program = False
        else:
            print("Not a valid command.")


###############################################################################
def test_cases():
    """
This function works to test functions that display outputs to the user, doing
so by bypassing user input requirements.
There are no inputs or outputs from this function. Variables are merely set and
booleans turned on and off. User outputs are coming from the called functions.
    """
    global testing_on
    global test_speech_input
    global test_speech_numbers
    global test_language_load
    global test_usage
    testing_on = True

    # Test Case 1 TESTS WORDS BY PART OF SPEECH SPEECH
    test_speech_input = "n"
    test_speech_numbers = "5"
    most_common_by_parts_of_speech()

    # Test Case 2 LOADS SPANISH AND COMPARES TO ENGLISH
    test_language_load = "SPANISH"
    foreign_word_list()
    compare_foreign_english()

    # Test Case 3 TESTS WORD USAGE FREQUENCY
    test_usage = "25"
    usage_percent()

    testing_on = False


###############################################################################
english_setup("words5000.csv")
task_manager()
