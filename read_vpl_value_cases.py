from pathlib import Path
def parse_value(value):
    """Converts a string to a number if possible, otherwise returns a regular string"""
    value = value.strip()
    if value.replace('.', '', 1).isdigit():
        # Integer or decimal number
        return float(value) if '.' in value else int(value)
    return value


def read_vpl_cases(filename):
    """
    Parses a test case file and returns a list of dictionaries.
    Repeated keys are stored as lists.
    Handles missing or empty files gracefully.
    """
    cases = []
    current_case = {}
    KEY_VALUE_DELIMITER = '='

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    if current_case:
                        cases.append(current_case)
                        current_case = {}
                    continue

                if KEY_VALUE_DELIMITER in line:
                    key, value = line.split(KEY_VALUE_DELIMITER, 1)
                    key = key.strip().lower()
                    value = parse_value(value)

                    if key in current_case:
                        if isinstance(current_case[key], list):
                            current_case[key].append(value)
                        else:
                            current_case[key] = [current_case[key], value]
                    else:
                        current_case[key] = value

            # Add the last case if any
            if current_case:
                cases.append(current_case)

        if not cases:
            print(f"Warning: File '{filename}' is empty or contains no valid cases.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")

    return cases



# Usage:
def main(case_file_path):
    vpl_evaluate = type("VplEvaluate", (), {})()
    vpl_evaluate.cases = read_vpl_cases(case_file_path)
    return vpl_evaluate
#
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    file_path = current_dir / "vpl_evaluate.cases"
    vpl = main(file_path)

    for case in vpl.cases:
     print(case)