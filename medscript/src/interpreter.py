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
            systolic, diastolic = map(float, value.split('//'))
            return cls(systolic, diastolic)
        except ValueError:
            raise MedScriptError("Blood pressure must be in format 'systolic//diastolic'")

@dataclass
class Glucose:
    value: float

    @classmethod
    def from_string(cls, value: str) -> 'Glucose':
        try:
            return cls(float(value))
        except ValueError:
            raise MedScriptError("Glucose value must be a number")
    
    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.value > other
        if isinstance(other, Glucose):
            return self.value > other.value
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, (int, float)):
            return self.value < other
        if isinstance(other, Glucose):
            return self.value < other.value
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, (int, float)):
            return self.value >= other
        if isinstance(other, Glucose):
            return self.value >= other.value
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, (int, float)):
            return self.value <= other
        if isinstance(other, Glucose):
            return self.value <= other.value
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.value == other
        if isinstance(other, Glucose):
            return self.value == other.value
        return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, (int, float)):
            return self.value != other
        if isinstance(other, Glucose):
            return self.value != other.value
        return NotImplemented

class MedScriptError(Exception):
    pass

class MedScriptTransformer(Transformer):
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.current_type: str = None

    def start(self, items):
        return items

    def statement(self, items):
        return items[0]

    def variable_declaration(self, items):
        name, type_, value = items
        self.current_type = type_
        if type_ == "mmHg":
            if not isinstance(value, BloodPressure):
                raise MedScriptError("Blood pressure values must be in format 'systolic//diastolic'")
        elif type_ == "mg/dL":
            if not isinstance(value, (float, int, Glucose)):
                raise MedScriptError("Glucose values must be numbers")
            if isinstance(value, (float, int)):
                value = Glucose(value)
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
        if len(items) == 1:
            value = items[0]
            if isinstance(value, str) and value in self.variables:
                return self.variables[value]
            return value
        return items[0]

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

    def add(self, items):
        left, right = items
        return float(left) + float(right)

    def sub(self, items):
        left, right = items
        return float(left) - float(right)

    def mul(self, items):
        left, right = items
        return float(left) * float(right)

    def div(self, items):
        left, right = items
        if float(right) == 0:
            raise MedScriptError("Division by zero")
        return float(left) / float(right)

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
            result = transformer.transform(tree)
            for item in result:
                if item is not None:
                    print(item)
        except Exception as e:
            print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Parse error: {str(e)}")

if __name__ == "__main__":
    print("Starting interpreter...")
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
            interpret(code)

# sys.stdout.write("ALERT: Hello, World!\n")
# sys.stdout.flush() 

