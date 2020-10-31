from runQuiz import *


def test_example():
    assert True


def test_more():
    assert [1, 2, 3] == [1, 2, 3]


def test_loading_quiz():
    with open('quizzes/exampleQuiz.yml') as f:
        quizYaml = yaml.load(f, Loader=yaml.UnsafeLoader)

    questionBank = QuestionBank()

    for questionData in quizYaml['questions']:
        question = Question(data=questionData)
        questionBank.add_question(question)
        # print(question)

    questionBank.randomize_question_order()

    # questionBank.run_quiz()
