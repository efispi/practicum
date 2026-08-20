import importlib
from pathlib import Path
from data_structures_and_parser import ParserFactory

def main_single(student_function_name, input_string):
    """
    מריץ פונקציה מתוך קובץ Python בשם התיקייה הנוכחית.
    שם הקובץ ושם הפונקציה זהים לשם התיקייה.
    """
    try:
        # קבלת שם התיקייה - ישמש גם כשם הקובץ וגם כשם הפונקציה
        current_dir_name = Path(__file__).parent.name
        
        # אם לא נמסר שם פונקציה - השתמש בשם התיקייה
        if not student_function_name:
            student_function_name = current_dir_name

        # ייבוא וטעינה מחדש של מודול התלמיד (שם הקובץ כשם התיקייה)
        try:
            student_module = importlib.import_module(current_dir_name)
            importlib.reload(student_module)
        except ImportError:
            return f"ERROR: {current_dir_name}.py not found"

        # איתור הפונקציה של התלמיד
        student_func = getattr(student_module, student_function_name, None)
        if student_func is None or not callable(student_func):
            return f"ERROR: Function '{student_function_name}' not found"

        # המרת מחרוזת הקלט למבנה נתונים
        parser = ParserFactory()
        try:
            parsed_inputs = parser.parse(input_string)
        except ValueError as e:
            return f"ERROR: Invalid input format: {e}"

        # הרצת הפונקציה של התלמיד
        try:
            if isinstance(parsed_inputs, (tuple, list)):
                result = student_func(*parsed_inputs)
            else:
                result = student_func(parsed_inputs)
        except TypeError as e:
            return f"ERROR: Invalid arguments: {e}"
        except Exception as e:
            return f"ERROR: {e}"

        # המרת התוצאה למחרוזת
        try:
            return str(result)
        except Exception as e:
            return f"ERROR: Failed to format output: {e}"

    except Exception as e:
        return f"ERROR: {e}"