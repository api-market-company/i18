import pytest

from i18.lexer import Lexer

__author__ = "sanchezcarlosjr"
__copyright__ = "sanchezcarlosjr"
__license__ = "MIT"


def get_values(tokens):
    return [(str(token), token.label_) for token in tokens]

def test_basic_expressions():
    lexer = Lexer()
    print(lexer.analyze("Hello World"))

