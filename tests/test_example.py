from runQuiz import *


def test_example():
    assert True


def test_more():
    assert [1, 2, 3] == [1, 2, 3]


def test_loading_quiz():
    with open('../quizzes/exampleQuiz.yml') as f:
        quizYaml = yaml.load(f, Loader=yaml.UnsafeLoader)

    questionBank = QuestionBank()

    for questionData in quizYaml['questions']:
        question = Question(data=questionData)
        questionBank.addQuestion(question)
        # print(question)

    questionBank.randomizeQuestionOrder()

    # questionBank.run_quiz()


def test_alphanum():
    assert (alphaToNumeric('a') == 1)
    assert (alphaToNumeric('b') == 2)

    assert (numericToAlpha(1) == 'a')
    assert (numericToAlpha(3) == 'c')
    assert (alphaToNumeric(numericToAlpha(20)) == 20)
    assert (numericToAlpha(alphaToNumeric('x')) == 'x')


def test_validation():
    assert (Question.validate_free_response(['cat', 'kitty'], 'CAT'))
    assert (Question.validate_matching_response(
        {'bug': 'lots of legs',
         'mammal': '2 legs',
         'cell': 'no legs'},

        {'bug': 'no legs',
         'mammal': '2 legs',
         'cell': 'no legs'}) == {
                'bug': 'lots of legs'
            })
