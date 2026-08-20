from main_single import main_single
from pathlib import Path

# קביעת שם התיקייה כברירת מחדל גלובלית
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

        # בדיקה שקיים קלט
        if "input" not in case:
            result["status"] = "FAIL"
            result["message"] = "Missing input"
            results.append(result)
            continue

        # קבלת שם הפונקציה: per-case או ברירת מחדל
        program = case.get("program to run", default_program)
        if not program:
            # fallback: שם התיקייה הנוכחית (cwd) אם לא סופק
            program = Path.cwd().name

        # הרצת main_single עם שם הפונקציה והקלט
        input_str = str(case["input"])
        actual_output = main_single(program, input_str)

        # קבלת הפלט הצפוי והמרה לרשימה אם צריך
        expected_outputs = case.get("output", [])
        if not isinstance(expected_outputs, list):
            expected_outputs = [str(expected_outputs)] if expected_outputs is not None else []
        else:
            expected_outputs = [str(x) for x in expected_outputs]  # המרת כל הערכים למחרוזות

        # המרת הפלט בפועל למחרוזת לצורך השוואה
        actual_output_str = str(actual_output)

        # השוואת הפלט שהתקבל לכל אחד מהפלטים הצפויים
        if any(actual_output_str == expected for expected in expected_outputs):
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
            result["message"] = case.get("fail message", 
                f"Expected one of {expected_outputs}, got {actual_output_str}")

        # בדיקת exit code אם קיים
        if "expected exit code" in case:
            expected_exit_code = case["expected exit code"]
            if expected_exit_code != 0 and "ERROR" not in actual_output:
                result["status"] = "FAIL"
                result["message"] = f"Expected exit code {expected_exit_code}, but no error occurred"
            elif expected_exit_code == 0 and "ERROR" in actual_output:
                result["status"] = "FAIL"
                result["message"] = f"Expected exit code 0, but got error: {actual_output}"

        results.append(result)

    return results

if __name__ == "__main__":
    from read_vpl_value_cases import read_vpl_cases
    current_dir = Path(__file__).parent
    case_file = current_dir / "vpl_value_cases"
    cases = read_vpl_cases(case_file)

    results = main(cases)  # שם התיקייה יילקח מ-DEFAULT_PROGRAM
    for res in results:
        print(f"Case: {res['case']}")
        print(f"Status: {res['status']}")
        if res["message"]:
            print(f"Message: {res['message']}")
        print()