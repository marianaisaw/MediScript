# MediScript
MediScript is a domain-specific programming language designed to simplify the expression of medical logic and clinical decision rules.

Features
-> Purpose: Clinical logic
-> Syntax: Minimal and natural
-> Execution: Interpreter (Lark, LLVM)
-> Domain fit: Medical alerts & recs
-> Target user: Clinicians, medical developers (software and hardware)

Code example:
let age: Years = 65
if age > 60 {
    alert "Senior patient"
    recommend "Annual heart checkup"
}

Inspired by TypeScript/based on Python, I created MediScript to bring stronger typing and more precise syntax to medical logic, helping avoid variable errors and making clinical rules more coherent and readable.

Clinical Statements

alert - warnings.
recommend - for treatment guidance.

This project is just for fun. I am gonna be working on more complex data types soon.

Run the program: python src/interpreter.py hello.med

## Features

- Type-safe variable declarations with medical units (Years, mmHg)
- Blood pressure handling with systolic/diastolic values
- Conditional statements for medical decision making
- Alert and recommendation system

## Installation

1. Make sure you are in the project directory:
```bash
cd medscript
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Create a `.med` file with your medical logic. Example:

```medscript
#This is test.med (You should be able to find the test in this repository)
let patient_age: Years = 65
let blood_pressure: mmHg = 160/100

if blood_pressure.systolic > 140 and patient_age > 60 {
    alert "Stage 2 Hypertension"
    recommend "Start antihypertensive therapy"
}
```

Run the script:
```bash
python3 src/interpreter.py test.med
```

## Language Features

### Variable Declaration
```medscript
let variable_name: TYPE = value
```

Supported types:
- Years
- mmHg
- String
- Number

### Blood Pressure
Blood pressure values are specified as systolic/diastolic:
```medscript
let bp: mmHg = 120/80
```

### Conditional Statements
```medscript
if condition {
    # statements
}
```

### Alerts and Recommendations
```medscript
alert "Your message"
recommend "Your recommendation"
```

## Example Output

When running the example code, you'll see:
```
ALERT: Stage 2 Hypertension
RECOMMENDATION: Start antihypertensive therapy
``` 


