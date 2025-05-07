import pytest
from src.interpreter import interpret
from lark import UnexpectedCharacters, UnexpectedToken

def test_invalid_blood_pressure_format():
    code = """
    let bp: mmHg = 120
    """
    with pytest.raises(UnexpectedToken):
        interpret(code)

def test_invalid_type():
    code = """
    let age: InvalidType = 25
    """
    with pytest.raises(UnexpectedToken):
        interpret(code)

def test_missing_type():
    code = """
    let age = 25
    """
    with pytest.raises(UnexpectedToken):
        interpret(code)

def test_invalid_property():
    code = """
    let bp: mmHg = 120/80
    if bp.invalid > 140 {
        alert "Error"
    }
    """
    with pytest.raises(UnexpectedToken):
        interpret(code)

def test_missing_braces():
    code = """
    let age: Years = 65
    if age > 60
        alert "Elderly"
    """
    with pytest.raises(UnexpectedToken):
        interpret(code) 