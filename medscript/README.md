# MedSicript

A simple domain-specific language for medical conditions and alerts.

## Features

- Type-safe variable declarations with medical units (Years, mmHg)
- Blood pressure handling with systolic/diastolic values
- Conditional statements for medical decision making
- Alert and recommendation system

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Create a `.med` file with your medical logic. Example:

```medscript
let patient_age: Years = 65
let blood_pressure: mmHg = 160/100

if blood_pressure.systolic > 140 and patient_age > 60 {
    alert "Stage 2 Hypertension"
    recommend "Start antihypertensive therapy"
}
```

Run the script:
```bash
python src/interpreter.py
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
    // statements
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
