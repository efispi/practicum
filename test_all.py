from pathlib import Path
from main import main  # זה הקובץ שמכיל את הפונקציה main

# קובץ מקרי הבדיקה
case_file = Path(__file__).parent / "vpl_value_cases"

# קריאה למקרי הבדיקה
from read_vpl_value_cases import read_vpl_cases
cases = read_vpl_cases(case_file)

# הרצת המערכת על כל המקרים
results = main(cases)

# הדפסת תוצאות
for idx, res in enumerate(results, 1):
    print(f"Case {idx}: {res.get('case', 'Unnamed Case')}")
    print(f"Status: {res['status']}")
    if res['message']:
        print(f"Message: {res['message']}")
    print("-" * 40)
