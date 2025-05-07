from lark import Lark, Transformer, UnexpectedToken
from dataclasses import dataclass
from typing import Dict, Any, List, Union
import sys

@dataclass
class BloodPressure:
    systolic: float
    diastolic: float

    @classmethod
    def from_string(cls, value: str) -> 'BloodPressure':
        try:
            systolic, diastolic = map(float, value.split('/'))
            return cls(systolic, diastolic)
        except ValueError:
            raise MedScriptError("Blood pressure must be in format 'systolic/diastolic'")

class MedScriptError(Exception):
    pass

class MedScriptTransformer(Transformer):
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.current_type: str = None

    def start(self, statements):
        return statements

    def variable_declaration(self, items):
        name, type_, value = items
        self.current_type = type_
        if type_ == "mmHg":
            if not isinstance(value, BloodPressure):
                raise MedScriptError("Blood pressure values must be in format 'systolic/diastolic'")
        self.variables[name] = value
        return None

    def if_statement(self, items):
        condition, *statements = items
        if condition:
            for statement in statements:
                if statement is not None:
                    print(statement)
        return None

    def condition(self, items):
        return all(items)

    def expression(self, items):
        return items[0]

    def comparison(self, items):
        left, op, right = items
        if left is None or right is None:
            raise MedScriptError("Invalid comparison: one or both operands are invalid")
        return eval(f"{left} {op} {right}")

    def alert_statement(self, items):
        return f"ALERT: {items[0]}"

    def recommend_statement(self, items):
        return f"RECOMMENDATION: {items[0]}"

    def value(self, items):
        value = items[0]
        if isinstance(value, str) and value in self.variables:
            return self.variables[value]
        return value

    def property_access(self, items):
        obj_name, prop_name = items
        if obj_name not in self.variables:
            raise MedScriptError(f"Variable '{obj_name}' not found")
        
        obj = self.variables[obj_name]
        if isinstance(obj, BloodPressure):
            if prop_name == "systolic":
                return obj.systolic
            elif prop_name == "diastolic":
                return obj.diastolic
        raise MedScriptError(f"Invalid property access")

    def blood_pressure(self, items):
        try:
            return BloodPressure(float(items[0]), float(items[1]))
        except ValueError:
            raise MedScriptError("Invalid blood pressure values")

    def NAME(self, name):
        return str(name)

    def TYPE(self, type_):
        return str(type_)

    def NUMBER(self, number):
        return float(number)

    def STRING(self, string):
        return string.strip('"')

    def COMPARISON(self, op):
        return str(op)

    def PROPERTY_NAME(self, prop_name):
        return str(prop_name)

def interpret(code: str) -> None:
    with open('src/grammar.lark') as f:
        grammar = f.read()
    
    parser = Lark(grammar, parser='lalr')
    transformer = MedScriptTransformer()
    
    try:
        tree = parser.parse(code)
        try:
            transformer.transform(tree)
        except Exception as e:
            if isinstance(e, UnexpectedToken):
                raise e
            raise UnexpectedToken(None, str(e))
    except UnexpectedToken as e:
        raise e

if __name__ == "__main__":
    print("Starting interpreter...")
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            code = f.read()
            interpret(code)
    else:
        # Example usage
        code = """
        let patient_age: Years = 65
        let blood_pressure: mmHg = 160/100

        if blood_pressure.systolic > 140 and patient_age > 60 {
            alert "Stage 2 Hypertension"
            recommend "Start antihypertensive therapy"
        }
        """
        interpret(code)

sys.stdout.write("ALERT: Hello, World!\n")
sys.stdout.flush() 