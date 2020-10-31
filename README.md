# pyconsolequiz

[![Build Status](https://travis-ci.org/HenryFBP/pyconsolequiz.svg?branch=master)](https://travis-ci.org/HenryFBP/pyconsolequiz)

[![Coverage Status](https://coveralls.io/repos/github/HenryFBP/pyconsolequiz/badge.svg?branch=master)](https://coveralls.io/github/HenryFBP/pyconsolequiz?branch=master)

## What is this?

Quiz program with simple yml format.

## Dependencies

    pip install pipenv
    pipenv install
    pipenv shell

## Running tests

    pipenv run coverage run -m pytest

## Running a quiz

    python runQuiz.py -f quizzes/exampleQuiz.yml
