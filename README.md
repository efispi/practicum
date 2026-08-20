
[ Instructor Defines Function & Cases ]
│
▼
[ Student Submits Code via VPL ]
│
▼
[ VPL Creates Temporary Directory ]
│
▼
[ Copies Runner Scripts & Case Files ]
│
▼
┌───────────────────────────┐
│     main.py (Runner)      │
└─────────────┬─────────────┘
│
▼
┌───────────────────────────┐
│  main_single.py (Engine)  │
└─────────────┬─────────────┘
│
├──► importlib (Load Student Code)
├──► ParserFactory (Parse Inputs)
└──► Execute Student Function
│
▼
[ Compare Outputs & Exit Codes ]
│
▼
[ Return Detailed Feedback / Status (PASS/FAIL) ]
│
▼
[ Clean Up Temporary Directory ]


---

## 🛠️ Tech Stack & Software Tools (טכנולוגיות וכלים)

| Tool / Technology | Role in Project |
| :--- | :--- |
| **Python** | Core logic implementation for testing runners, string parsing, and test execution. |
| **Moodle** | Primary Learning Management System (LMS) host. |
| **VPL (Virtual Programming Lab)** | Moodle extension for managing coding assignments and student code submission. |
| **VPL Jail & Docker** | Isolated container environment for running un-trusted student code safely. |
| **WSL (Windows Subsystem for Linux)** | Linux runtime environment under Windows for Docker & VPL Jail execution. |
| **Git & GitHub** | Version control, collaboration, and repository management. |
| **VS Code** | Code editing, debugging, and local test environment execution. |

---

## 📂 Project Structure & Core Components (מבנה הקוד והקבצים)

.
├── main.py                     # Entry point for processing test cases and logging results
├── main_single.py              # Executes individual student functions safely with arguments
├── read_vpl_value_cases.py     # Helper to load test cases from VPL case definitions
├── data_structures_and_parser.py # Contains ParserFactory for converting string input to data structures
├── vpl_value_cases             # Test cases definition file
└── README.md                   # Project documentation


---

## 💻 Core Code Structure (קוד הליבה)

### 1. Test Harness Runner (`main.py`)
Responsible for iterating through all test cases, running `main_single` for each, comparing expected outputs against actual results, and returning structured status reports.

```python
from main_single import main_single
from pathlib import Path

DEFAULT_PROGRAM = Path(__file__).parent.name

def main(cases, default_program=None):
    if default_program is None:
        default_program = DEFAULT_PROGRAM
    results = []

    for case in cases:
        result = {
            "case": case.get("case", "Unnamed Case"),
            "status": "PASS",
            "message": ""
        }
        if "input" not in case:
            result["status"] = "FAIL"
            result["message"] = "Missing input"
            results.append(result)
            continue

        program = case.get("program_to_run", default_program)
        input_str = str(case["input"])
        actual_output = main_single(program, input_str)
        
        expected_outputs = case.get("output", [])
        if not isinstance(expected_outputs, list):
            expected_outputs = [str(expected_outputs)] if expected_outputs is not None else []
        else:
            expected_outputs = [str(x) for x in expected_outputs]

        actual_output_str = str(actual_output)
        if any(actual_output_str == expected for expected in expected_outputs):
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
            result["message"] = case.get("fail_message", f"Expected one of {expected_outputs}, got {actual_output_str}")

        results.append(result)
    return results
2. Single Function Execution Engine (main_single.py)
Dynamically imports student modules, uses ParserFactory to parse inputs, and safely catches execution errors.

Python
import importlib
from pathlib import Path
from data_structures_and_parser import ParserFactory

def main_single(student_function_name, input_string):
    try:
        current_dir_name = Path(__file__).parent.name
        if not student_function_name:
            student_function_name = current_dir_name

        try:
            student_module = importlib.import_module(current_dir_name)
            importlib.reload(student_module)
        except ImportError:
            return f"ERROR: {current_dir_name}.py not found"

        student_func = getattr(student_module, student_function_name, None)
        if student_func is None or not callable(student_func):
            return f"ERROR: Function '{student_function_name}' not found"

        try:
            parser = ParserFactory()
            parsed_inputs = parser.parse(input_string)
        except ValueError as e:
            return f"ERROR: Invalid input format: {e}"

        try:
            if isinstance(parsed_inputs, (tuple, list)):
                result = student_func(*parsed_inputs)
            else:
                result = student_func(parsed_inputs)
        except TypeError as e:
            return f"ERROR: Invalid arguments: {e}"
        except Exception as e:
            return f"ERROR: {e}"

        return str(result)
    except Exception as e:
        return f"ERROR: {e}"
👩‍💻 Credits & Metadata (קרדיטים ומידע על הפרויקט)
Developer: Efrat Cohen (אפרת כהן)

Academic Institution: Seminar "Meir" Netivot (סמינר "מאיר" נתיבות)

Industry Partners: KamaTech & ExtraTech (קמא טק / אקסטרה טק)

Personal Mentor: Moriah Davidov (מוריה דוידוב)

Academic Mentor: Miri Weichlder (מירי וייכלדר)

Project Duration: March - July 2025
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md created successfully!")


```text?code_stdout&code_event_index=2
README.md created successfully!

את יכולה בשמחה להעלות את הקובץ. יצרתי עבורך קובץ README.md מקצועי, מעוצב ומפורט על בסיס ספר הפרויקט שלך ("מערכת אוטומטית לבדיקת קוד סטודנטים").

סמל של MD
README
 MD 
פתוח
מה הקובץ כולל?
כותרת ותגיות (Badges): תגיות מותאמות עבור Python, Docker, Moodle ו-VPL.  
PDF

תקציר הפרויקט (Overview): הסבר תמציתי וברור על המערכת שפיתחת עבור קמא טק / ExtraTech וסמינר "מאיר" נתיבות.  
PDF

תכונות מרכזיות (Key Features):

הרצה בסביבה מבודדת (Jail VPL + Docker + WSL).  
PDF

המרה וניתוח קלט/פלט דינמי באמצעות ParserFactory.  
PDF

מנגנון הרצה ודיווח סטטוס מפורט (PASS / FAIL).  
PDF

ניקוי וניהול תיקיות זמניות בסיום הרצה.  
PDF

תרשים זרימת עבודה (Architecture & Workflow): תרשים ASCII קריא המציג את שלבי הבדיקה – מהגדרת המרצה ועד להחזרת הסטטוס לתלמיד.  
PDF

טבלת הטכנולוגיות (Tech Stack): פירוט הכלים (Python, Moodle, Docker, WSL, Git, VS Code) ותפקידם.  
PDF

מבנה הפרויקט (Project Structure): היררכיית קבצים מסודרת.  
PDF

קוד הליבה (Core Code): הצגת הקוד של main.py ו-main_single.py כפי שמופיעים בספר הפרויקט עם עיצוב קוד מתאים ל-GitHub.  
PDF

קרדיטים ופרטי הגשה (Credits): פרטי המפתחת, המנחות, המוסד הלימודי והשותפים.  
PDF

איך להעלות ל-GitHub?
הורידי את קובץ ה-README.md מהקישור למעלה.

העתיקי אותו לתיקיית שורש הפרויקט שלך (Root Folder).

בצעי Commit ו-Push ל-GitHub:

Bash
git add README.md
git commit -m "Add professional README file"
git push origin main



‫Gemini מבוסס על AI ויכול לטעות.

מנתח את הנתונים
# Automated Student Code Verification System (מערכת אוטומטית לבדיקת קוד סטודנטים)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Moodle](https://img.shields.io/badge/Moodle-LMS-orange.svg)](https://moodle.org/)
[![VPL](https://img.shields.io/badge/VPL-Virtual%20Programming%20Lab-green.svg)](https://vpl.dis.ulpgc.es/)

## 📝 Overview (סקירת הפרויקט)

This project presents an automated system for executing, validating, and testing student code submissions. Developed as part of a practicum with **KamaTech** and **ExtraTech** for Seminar "Meir" Netivot, the platform provides a secure, isolated, and standardized environment for real-time code evaluation and detailed feedback generation.

The system integrates directly with **Moodle** and **VPL (Virtual Programming Lab)** using Docker containers and Linux subsystems to guarantee safe execution while providing modular Python test runners (`main.py` and `main_single.py`) and data structure parsers.

---

## 🔑 Key Features (תכונות מרכזיות)

- **Isolated Execution Environment (Jail VPL):** Runs student code in secure Docker containers using WSL to prevent system exploits or unwanted side effects.
- **Dynamic Input/Output Parsing:** Utilizes a custom `ParserFactory` (`data_structures_and_parser.py`) to parse input strings into complex data structures (lists, tuples, matrices) and evaluate student functions accurately.
- **Automated Test Harness (`main.py` & `main_single.py`):**
  - Dynamic module loading using `importlib` and automatic reloading to ensure clean execution.
  - Granular `PASS` / `FAIL` status checking with exact and multi-option output comparisons.
  - Exception handling for missing files, signature mismatches (`TypeError`), syntax errors, and exit codes.
- **Clean Workspace Management:** Dynamically creates isolated directories per test execution and automatically cleans up temporary files upon completion.
- **VS Code Integration:** Enhanced development and debugging capabilities for instructors and developers.

---

## 🏗️ Architecture & Workflow (ארכיטקטורה וזרימת עבודה)

```
[ Instructor Defines Function & Cases ]
                  │
                  ▼
   [ Student Submits Code via VPL ]
                  │
                  ▼
  [ VPL Creates Temporary Directory ]
                  │
                  ▼
[ Copies Runner Scripts & Case Files ]
                  │
                  ▼
    ┌───────────────────────────┐
    │     main.py (Runner)      │
    └─────────────┬─────────────┘
                  │
                  ▼
    ┌───────────────────────────┐
    │  main_single.py (Engine)  │
    └─────────────┬─────────────┘
                  │
                  ├──► importlib (Load Student Code)
                  ├──► ParserFactory (Parse Inputs)
                  └──► Execute Student Function
                  │
                  ▼
   [ Compare Outputs & Exit Codes ]
                  │
                  ▼
[ Return Detailed Feedback / Status (PASS/FAIL) ]
                  │
                  ▼
   [ Clean Up Temporary Directory ]
```

---

## 🛠️ Tech Stack & Software Tools (טכנולוגיות וכלים)

| Tool / Technology | Role in Project |
| :--- | :--- |
| **Python** | Core logic implementation for testing runners, string parsing, and test execution. |
| **Moodle** | Primary Learning Management System (LMS) host. |
| **VPL (Virtual Programming Lab)** | Moodle extension for managing coding assignments and student code submission. |
| **VPL Jail & Docker** | Isolated container environment for running un-trusted student code safely. |
| **WSL (Windows Subsystem for Linux)** | Linux runtime environment under Windows for Docker & VPL Jail execution. |
| **Git & GitHub** | Version control, collaboration, and repository management. |
| **VS Code** | Code editing, debugging, and local test environment execution. |

---

## 📂 Project Structure & Core Components (מבנה הקוד והקבצים)

```
.
├── main.py                     # Entry point for processing test cases and logging results
├── main_single.py              # Executes individual student functions safely with arguments
├── read_vpl_value_cases.py     # Helper to load test cases from VPL case definitions
├── data_structures_and_parser.py # Contains ParserFactory for converting string input to data structures
├── vpl_value_cases             # Test cases definition file
└── README.md                   # Project documentation
```

---

## 💻 Core Code Structure (קוד הליבה)

### 1. Test Harness Runner (`main.py`)
Responsible for iterating through all test cases, running `main_single` for each, comparing expected outputs against actual results, and returning structured status reports.

```python
from main_single import main_single
from pathlib import Path

DEFAULT_PROGRAM = Path(__file__).parent.name

def main(cases, default_program=None):
    if default_program is None:
        default_program = DEFAULT_PROGRAM
    results = []

    for case in cases:
        result = {
            "case": case.get("case", "Unnamed Case"),
            "status": "PASS",
            "message": ""
        }
        if "input" not in case:
            result["status"] = "FAIL"
            result["message"] = "Missing input"
            results.append(result)
            continue

        program = case.get("program_to_run", default_program)
        input_str = str(case["input"])
        actual_output = main_single(program, input_str)
        
        expected_outputs = case.get("output", [])
        if not isinstance(expected_outputs, list):
            expected_outputs = [str(expected_outputs)] if expected_outputs is not None else []
        else:
            expected_outputs = [str(x) for x in expected_outputs]

        actual_output_str = str(actual_output)
        if any(actual_output_str == expected for expected in expected_outputs):
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
            result["message"] = case.get("fail_message", f"Expected one of {expected_outputs}, got {actual_output_str}")

        results.append(result)
    return results
```

### 2. Single Function Execution Engine (`main_single.py`)
Dynamically imports student modules, uses `ParserFactory` to parse inputs, and safely catches execution errors.

```python
import importlib
from pathlib import Path
from data_structures_and_parser import ParserFactory

def main_single(student_function_name, input_string):
    try:
        current_dir_name = Path(__file__).parent.name
        if not student_function_name:
            student_function_name = current_dir_name

        try:
            student_module = importlib.import_module(current_dir_name)
            importlib.reload(student_module)
        except ImportError:
            return f"ERROR: {current_dir_name}.py not found"

        student_func = getattr(student_module, student_function_name, None)
        if student_func is None or not callable(student_func):
            return f"ERROR: Function '{student_function_name}' not found"

        try:
            parser = ParserFactory()
            parsed_inputs = parser.parse(input_string)
        except ValueError as e:
            return f"ERROR: Invalid input format: {e}"

        try:
            if isinstance(parsed_inputs, (tuple, list)):
                result = student_func(*parsed_inputs)
            else:
                result = student_func(parsed_inputs)
        except TypeError as e:
            return f"ERROR: Invalid arguments: {e}"
        except Exception as e:
            return f"ERROR: {e}"

        return str(result)
    except Exception as e:
        return f"ERROR: {e}"
```

---

## 👩‍💻 Credits & Metadata (קרדיטים ומידע על הפרויקט)

- **Developer:** Efrat Cohen (אפרת כהן)
- **Academic Institution:** Seminar "Meir" Netivot (סמינר "מאיר" נתיבות)
- **Industry Partners:** KamaTech & ExtraTech (קמא טק / אקסטרה טק)
- **Personal Mentor:** Moriah Davidov (מוריה דוידוב)
- **Academic Mentor:** Miri Weichlder (מירי וייכלדר)
- **Project Duration:** March - July 2025
README.md
הפריט README.md מוצג.
