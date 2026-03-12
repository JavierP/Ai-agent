import sys
import os
base = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base)
from functions.write_file import write_file

test_cases = [
    write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
]

for test in test_cases:
    print("Result for current Test:")
    print(f"{test}\n")
    
    