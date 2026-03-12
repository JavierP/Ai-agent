from functions.get_file_content import get_file_content
from config import *

test_cases = [
    get_file_content('calculator', 'lorem.txt'),
    get_file_content('calculator', 'main.py'),
    get_file_content('calculator', 'pkg/calculator.py'),
    get_file_content('calculator', '/bin/cat'),
    get_file_content('calculator', 'pkg/does_not_exist.py')
]

for test in test_cases:
    t_len = len(test)
    if t_len <= MAX_LEN:
        print(f"Length: {t_len}")
        print(f"End of result: {test}")
    else:
        print(f"Length: {t_len}")
        print(f"End of result: {test[-100:]}")
        