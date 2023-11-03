from i18.parser import sub

__author__ = "sanchezcarlosjr"
__copyright__ = "sanchezcarlosjr"
__license__ = "MIT"


def test_replacement():
    assert "(0+( 1 + 0 ) + 1 )     +1" == sub("""
    start: expression

    expression: atom ("+"|"-"|"*"|"/") expression | atom

    atom: SIGNED_NUMBER -> group
        | "(" expression ")"

    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, lambda token: str(int(token) % 2), "(4+( 5 + 6 ) + 5 )     +3")
    assert "1" == sub("""
        start: expression
        expression: /123/ -> group
        """, lambda token: "1", "123")
