import pytest
from src.interpreter import interpret
import io
import sys

def capture_output(code):
    # Capture stdout to test print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Run the interpreter
    interpret(code)
    
    # Restore stdout and get output
    sys.stdout = sys.__stdout__
    return captured_output.getvalue().strip()

def test_basic_variable_declaration():
    code = """
    let age: Years = 25
    """
    output = capture_output(code)
    assert output == ""  # Variable declarations don't produce output

def test_blood_pressure_declaration():
    code = """
    let bp: mmHg = 120/80
    """
    output = capture_output(code)
    assert output == ""

def test_hypertension_stage2():
    code = """
    let patient_age: Years = 65
    let blood_pressure: mmHg = 160/100

    if blood_pressure.systolic > 140 and patient_age > 60 {
        alert "Stage 2 Hypertension"
        recommend "Start antihypertensive therapy"
    }
    """
    output = capture_output(code)
    assert "ALERT: Stage 2 Hypertension" in output
    assert "RECOMMENDATION: Start antihypertensive therapy" in output

def test_normal_blood_pressure():
    code = """
    let patient_age: Years = 45
    let blood_pressure: mmHg = 120/80

    if blood_pressure.systolic > 140 and patient_age > 60 {
        alert "Stage 2 Hypertension"
        recommend "Start antihypertensive therapy"
    }
    """
    output = capture_output(code)
    assert output == ""  # No alerts for normal blood pressure

def test_blood_pressure_properties():
    code = """
    let bp: mmHg = 150/95
    if bp.systolic > 140 {
        alert "High systolic pressure"
    }
    if bp.diastolic > 90 {
        alert "High diastolic pressure"
    }
    """
    output = capture_output(code)
    assert "ALERT: High systolic pressure" in output
    assert "ALERT: High diastolic pressure" in output

def test_multiple_conditions():
    code = """
    let age: Years = 70
    let bp: mmHg = 170/100
    
    if bp.systolic > 160 and age > 65 {
        alert "Severe hypertension in elderly"
        recommend "Immediate medical attention"
    }
    """
    output = capture_output(code)
    assert "ALERT: Severe hypertension in elderly" in output
    assert "RECOMMENDATION: Immediate medical attention" in output 