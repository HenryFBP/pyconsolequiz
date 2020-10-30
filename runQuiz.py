import yaml
from pprint import pprint
import argparse
from enum import Enum
from typing import Dict, List, Union, Tuple
import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class QuestionType(Enum):
    FREE_RESPONSE = 0
    MULTIPLE_CHOICE = 1
    MATCHING = 2
    UNKNOWN = 3


QuestionTypeDict = {
    'FREE RESPONSE': QuestionType.FREE_RESPONSE,
    'MATCHING': QuestionType.MATCHING,
    'MULTIPLE CHOICE': QuestionType.MULTIPLE_CHOICE,
}


def reversedDict(d: dict) -> dict:
    return {v: k for k, v in d.items()}


QuestionTypeDictReversed = reversedDict(QuestionTypeDict)


def createObjectList(size=10, fillWith=False):
    l = []
    for i in range(size):
        l.append(fillWith)
    return l


def shuffledRange(*args, **kwargs):
    l = list(range(*args, **kwargs))
    random.shuffle(l)
    return l


def countMatchingElements(l1, l2) -> int:
    assert(len(l1) == len(l2))

    matches = 0
    for i in range(0, len(l1)):
        if(l1[i] == l2[i]):
            matches += 1

    return matches


assert(countMatchingElements([1, 2, 3], [1, 2, 4]) == 2)


def alphaToNumeric(c: str) -> int:
    """Given a character, return its numerical position. A=1, etc."""
    char = c[0].lower()
    return (ord(char) - ord('a')) + 1


assert(alphaToNumeric('a') == 1)
assert(alphaToNumeric('b') == 2)


def numericToAlpha(i: int) -> str:
    return chr(i + ord('a') - 1)


assert(numericToAlpha(1) == 'a')
assert(numericToAlpha(3) == 'c')
assert(alphaToNumeric(numericToAlpha(20)) == 20)
assert(numericToAlpha(alphaToNumeric('x')) == 'x')


def validateIntegerResponse(s: str) -> bool:
    """Return true if input looks like '1', '20', etc"""
    # string
    if(type(s) != str):
        return False

    #  string is numeric
    try:
        int(s)
    except ValueError:
        return False

    # int part must be less than 0 and not equal to 0
    if int(s) <= 0:
        return False

    return True


def validateMatchingResponse(s: str) -> bool:
    """Return true if input looks like 'A1', 'b2', etc"""

    # string
    if(type(s) != str):
        return False

    # not empty
    if(len(s) == 0):
        return False

    # 1st char is alphabetic
    if(s[0].upper() not in ALPHABET.upper()):
        return False

    # rest of string is numeric
    try:
        int(s[1:])
    except ValueError:
        return False

    # int part must be less than 0 and not equal to 0
    if int(s[1:]) <= 0:
        return False

    return True


assert(validateMatchingResponse('A2'))
assert not validateMatchingResponse('b0')
assert(validateMatchingResponse('x10'))


def parseMatchingResponse(s: str, offset=0) -> List[int]:
    """Given a matching response input (A3, B20, etc), return
    that response input as 2 ints in a tuple."""

    lhs, rhs = s[0], s[1:]

    ret = [alphaToNumeric(lhs), int(rhs)]

    ret[0] = ret[0]+offset
    ret[1] = ret[1]+offset

    return ret


assert(parseMatchingResponse('A3') == [1, 3])
assert(parseMatchingResponse('b4') == [2, 4])
assert(parseMatchingResponse('X20') == [24, 20])


def promptMatchingResponse(offset=0) -> Tuple[int]:
    """Get a matching response input from stdin."""
    while True:
        answer = input('[a-zA-Z][1-9]+ (ex. "b10")\n > ')

        if validateMatchingResponse(answer):
            return parseMatchingResponse(answer, offset)


def promptIntegerResponse(offset=0) -> Tuple[int]:
    """Get an integer response input from stdin."""
    while True:
        answer = input('[1-9]+ (ex. "20")\n > ')

        if validateIntegerResponse(answer):
            return int(answer)


def promptYN() -> bool:
    """Get y/n from a user."""
    while True:
        answer = input('[Yy]es/[Nn]o \n > ')

        if answer[0].capitalize() == 'Y':
            return True
        if answer[0].capitalize() == 'N':
            return False


class Question:
    def __init__(self, data):
        self.data = data
        self.answered = False
        self.answer = None
        self.correct = False

    @staticmethod
    def validate_free_response(correct_answers: List[str], proposed_answer: str) -> bool:
        """Given a list of correct answers and 1 proposed answer, return True if the answer exists in the list of correct answers."""
        answers_uppercase = [x.upper() for x in correct_answers]
        proposed_answer_u = proposed_answer.upper()

        if proposed_answer_u in answers_uppercase:
            return True

        return False

    @staticmethod
    def validate_matching_response(correct_mappings: Dict[str, str],
                                   proposed_mappings: Dict[str, str]) -> Dict[str, str]:
        """Given a list of proposed mappings of a matching question response, return a mapping of correct answers that were not answered correctly.

        If the returned mapping is empty, then all answers are correct."""

        missed_correct_mappings = {}

        for key in correct_mappings:
            if not (correct_mappings[key] == proposed_mappings[key]):
                missed_correct_mappings[key] = correct_mappings[key]

        return missed_correct_mappings

    def printQuestion(self):
        print(f"Question:   {self.getTitle()}")

    def printQuestionHeader(self):
        print('-' * 30)
        print(f"Type:       {self.getQuestionTypePretty()}")
        self.printQuestion()

    def printAnswersAsList(self):
        for s in self.getAnswers():
            print(f"- {s}")

    def askMultipleChoiceQuestion(self):
        """Ask a multiple choice question to stdin and store requests in myself."""

        print("Select the correct answer(s).")
        print("Type in numbers to toggle selection of a choice.")
        print("Example: Typing '3' toggles selection of the 3rd option.")

        questions, correctChoices = self.getMatchingAnswersAs2Lists()
        userChoices = createObjectList(len(correctChoices))

        # pprint(questions)
        # pprint(correctChoices)
        # pprint(userChoices)

        boolmap = {True: 'x', False: ' '}
        rightwrongmap = {True: "Right", False: "Wrong"}

        while True:

            self.printQuestion()
            print("Type 'submit' to submit your answers.")

            for i in range(0, len(questions)):
                print(f'{i+1:2d}. [{boolmap[userChoices[i]]}] {questions[i]}')

            userInput = input('[1-9]+ (ex. "20")\n > ')

            if('submit'.upper() == userInput.upper()):

                correctNumber = countMatchingElements(
                    userChoices, correctChoices)

                print("Submitted.")
                print("{}/{} answers are correct.".format(correctNumber, len(questions)))

                self.answered = True
                self.answer = userChoices
                self.correct = (self.answer == correctChoices)

                for i in range(0, len(questions)):
                    correctness = self.answer[i] == correctChoices[i]

                    print(
                        f"{rightwrongmap[correctness]}: [{boolmap[self.answer[i]]}] {questions[i]}")

                return

            if validateIntegerResponse(userInput):
                userInputNumeric = int(userInput)

                if(userInputNumeric) > len(questions):
                    print(f"{userInputNumeric} is too large.")

                else:  # actually use their input
                    userChoices[userInputNumeric -
                                1] = not userChoices[userInputNumeric - 1]

            else:
                print(f"{userInput} is not numeric.")

    def askMatchingQuestion(self):
        """Ask a matching question to stdin and store results in myself."""

        print("Match the alphabetic items to the numeric items.")
        print("Example: Typing 'B2' matches item B to item 2.")
        print("Don't enter more than 1 choice at a time.")
        print("Also, you can match things you've already chosen...")
        print("    Ex: B1 <ENTER> B2 <ENTER> B3 <ENTER> is a totally valid input sequence.")

        answerLists = self.getMatchingAnswersAs2Lists()
        numQuestions = len(answerLists[0])

        userChoices = {}
        doneAnswering = False

        # randomized answer list positions. Item 1 still maps to item a, b-2, etc.
        answerListPositions = (
            shuffledRange(0, len(answerLists[0])),
            shuffledRange(0, len(answerLists[1]))
        )

        random.shuffle(answerListPositions[0])
        random.shuffle(answerListPositions[1])

        # pprint(answerListPositions)

        while not doneAnswering:

            i = 0
            for idx in answerListPositions[0]:
                print(f"{numericToAlpha(i+1)}: {answerLists[0][idx]}")
                i += 1

            print()

            i = 0
            for idx in answerListPositions[1]:
                print(f"{(i+1)}: {answerLists[1][idx]}")
                i += 1

            print()

            if userChoices != {}:
                print("Current choices:")
                for key in userChoices:
                    print(f"{key:10s} : {userChoices[key]:10s}")

            while True:
                matchingResponse = promptMatchingResponse(offset=-1)
                if (matchingResponse[0] >= numQuestions) or \
                        (matchingResponse[1] >= numQuestions):
                    print("Letter/number too high/low. Please try again.")
                    print(
                        f"Highest letter/number: {numericToAlpha(numQuestions)}/{numQuestions}")
                else:
                    break

            # print(f"user typed ints {matchingResponse}")
            matchingIndices = (
                answerListPositions[0][matchingResponse[0]],
                answerListPositions[1][matchingResponse[1]],
            )
            # print(f"user indices were {matchingIndices}")

            userChoice = [answerLists[0][matchingIndices[0]],
                          answerLists[1][matchingIndices[1]]]
            # print(f"user thinks '{userChoice[0]}' matches with {userChoice[1]}")

            # if(matchingIndices[0] == matchingIndices[1]):
            #     print("user is right")
            # else:
            #     print("user is wrong")

            userChoices[userChoice[0]] = userChoice[1]

            # if they've answered all the questions,
            # see if they want to be done.
            if(len(userChoices.keys()) == numQuestions):
                print(
                    f"You've answered {numQuestions}/{numQuestions} questions.")
                print(f"Are you ready to submit this question?")
                if promptYN():
                    doneAnswering = True
                    self.answered = True
                    self.answer = userChoices
                    # print("TODO submit and validate the question lol")

                    missed_correct_answers = self.validate_matching_response(
                        self.getAnswers(), self.answer)

                    if(missed_correct_answers == {}):
                        self.correct = True
                        print(
                            "You got all {n}/{n} answers correct!".format(n=numQuestions))
                    else:
                        self.correct = False
                        print("You got {}/{} answers wrong.".format(
                            len(missed_correct_answers.keys()), numQuestions
                        ))

                        print("These were your wrong answers:")
                        for key in missed_correct_answers:
                            print("{} matched with '{}' but should have been matched with '{}'.".format(
                                key, self.answer[key], missed_correct_answers[key]))

                else:
                    print("Continuing.")

    def askFreeResponseQuestion(self):
        """Ask a free response question to stdin and store results in myself."""
        user_input = input(" > ")

        if self.validate_free_response(self.getAnswers(), user_input):
            self.correct = True
            self.answered = True
            self.answer = user_input
            print(
                f"Correct! You answered '{user_input}'. The correct answers were:")
            self.printAnswersAsList()

        else:
            print("These were the correct answers:")
            self.printAnswersAsList()
            print(
                "You may be potentially incorrect, but I cannot tell as I'm just a computer.")
            print(f"Did your answer of '{user_input}' match the above answers enough to be counted as a correct "
                  f"answer? Please be honest.")
            self.correct = promptYN()
            self.answered = True
            self.answer = user_input

    def askQuestion(self):
        """Ask a question to stdin and store results in myself."""

        self.printQuestionHeader()

        if self.getQuestionType() == QuestionType.FREE_RESPONSE:
            self.askFreeResponseQuestion()

        if self.getQuestionType() == QuestionType.MATCHING:
            self.askMatchingQuestion()

        if self.getQuestionType() == QuestionType.MULTIPLE_CHOICE:
            self.askMultipleChoiceQuestion()

        if self.getQuestionType() == QuestionType.UNKNOWN:
            print("lol you need to fix this question:")
            print(self)
            exit(1)

    def __str__(self):
        return f"""{self.getTitle()}
Type: {self.getQuestionType().name}"""

    def getTitle(self) -> str:
        return self.data['title']

    def getAnswers(self) -> List:
        return self.data['answers']

    def getMatchingAnswersAs2Lists(self) -> Tuple[List[str]]:
        # pprint(self.getAnswers())

        answersTuple = ([], [])
        answers = self.getAnswers()

        for k in self.getAnswers():
            answersTuple[0].append(k)
            answersTuple[1].append(answers[k])

        if(len(answersTuple[0]) != len(answersTuple[1])):
            pprint(answersTuple)
            print(
                f"{len(answersTuple[0])} on left hand side, {len(answersTuple[1])} on right hand side!")
            raise AssertionError(
                "Must have equal number of matching question answers on both sides!")

        return answersTuple

    def getQuestionTypeRaw(self) -> str:
        return self.data['type']

    def getQuestionTypePretty(self) -> str:
        return self.getQuestionTypeRaw().lower().capitalize()

    def getQuestionType(self) -> QuestionType:
        if self.getQuestionTypeRaw().upper() in QuestionTypeDict:
            return QuestionTypeDict[self.getQuestionTypeRaw().upper()]

        return QuestionType.UNKNOWN


class QuestionBank():
    def __init__(self, questions=None):
        if questions is None:
            questions = []

        self.questions = questions

    def add_question(self, question: Question):
        self.questions.append(question)

    def randomize_question_order(self):
        random.shuffle(self.questions)

    def run_quiz(self):
        for question in self.questions:
            if not question.answered:
                question.askQuestion()


assert(Question.validate_free_response(['cat', 'kitty'], 'CAT'))
assert(Question.validate_matching_response(
    {'bug': 'lots of legs',
     'mammal': '2 legs',
     'cell': 'no legs'},

    {'bug': 'no legs',
     'mammal': '2 legs',
     'cell': 'no legs'}) == {
    'bug': 'lots of legs'
}
)

if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--file", required=True, help="Quiz datafile")

    # Read arguments from command line
    args = parser.parse_args()

    print("Using quiz file " + args.file)

    with open(args.file) as f:
        quizYaml = yaml.load(f, Loader=yaml.UnsafeLoader)

    questionBank = QuestionBank()

    for questionData in quizYaml['questions']:
        question = Question(data=questionData)
        questionBank.add_question(question)
        # print(question)

    questionBank.randomize_question_order()
    questionBank.run_quiz()

    exit(0)
