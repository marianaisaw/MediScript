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

Inspired by TypeScript/ Based in Python, I created MedScript to bring stronger typing and more precise syntax to medical logic, helping avoid variable errors and making clinical rules more coherent and readable.

Medical-Specific Types (so far):

: Years - for age.
: mmHg - for blood pressure.
: Number - for general values.

Clinical Statements

alert - warnings.
recommend - for treatment guidance.

This project is just for fun. I am gonna be working on more complex data types soon.

Run the program: python src/interpreter.py hello.med

