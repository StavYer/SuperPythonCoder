"""Module for interfacing with the OpenAI API."""
import os
import random
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv('API_KEY')
client = OpenAI(api_key=API_KEY)

PROGRAMS_LIST = [
    '''Given two strings str1 and str2, prints all interleavings of the given
    two strings. You may assume that all characters in both strings are
    different.Input: str1 = "AB", str2 = "CD"
    Output:
    ABCD
    ACBD
    ACDB
    CABD
    CADB
    CDAB
    Input: str1 = "AB", str2 = "C"
    Output:
    ABC
    ACB
    CAB ''',
    "a program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree.",
    """The string 'PAYPALISHIRING' is written in a zigzag pattern 
    on a given number of rows like this (you may want to display this pattern in a fixed font for better legibility): 
    P   A   H   N
    A P L S I I G
    Y   I   R
    And then read line by line: 'PAHNAPLSIIGYIR'.
    Write the code that will take a string and make this conversion given a number of rows:
    string convert(string s, int numRows);
     Example 1:
    Input: s = "PAYPALISHIRING", numRows = 3
    Output: "PAHNAPLSIIGYIR"
    Example 2:
    Input: s = "PAYPALISHIRING", numRows = 4
    Output: "PINALSIGYAHRPI"
    Explanation:
    P     I    N
    A   L S  I G
    Y A   H R
    P     I
    Example 3:
    Input: s = "A", numRows = 1
    Output: "A"
    Constraints:
    1 <= s.length <= 1000
    s consists of English letters (lower-case and upper-case), ',' and '.'.
    1 <= numRows <= 1000""",
    """A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
    For example, for arr = [1,2,3], the following are all the permutations of arr: [1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1].
    The next permutation of an array of integers is the next lexicographically greater permutation of its integer. 
    More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, 
    then the next permutation of that array is the permutation that follows it in the sorted container. 
    If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).
    For example, the next permutation of arr = [1,2,3] is [1,3,2].
    Similarly, the next permutation of arr = [2,3,1] is [3,1,2].
    While the next permutation of arr = [3,2,1] is [1,2,3] because [3,2,1] does not have a lexicographical larger rearrangement.
    Given an array of integers nums, find the next permutation of nums.
    The replacement must be in place and use only constant extra memory.
    Example 1:
    Input: nums = [1,2,3]
    Output: [1,3,2]
    Example 2:
    Input: nums = [3,2,1]
    Output: [1,2,3]
    Example 3:
    Input: nums = [1,1,5]
    Output: [1,5,1]
    Constraints:
    1 <= nums.length <= 100
    0 <= nums[i] <= 100"""
]

def get_program_request():
    choice = input(("Im Super Python Coder. Tell me, which program would you like me to code for you?\n"
         "If you don't have an idea, just press enter and"
          " I will choose a random program to code:"))
    if choice.strip() == "":
        choice = random.choice(PROGRAMS_LIST)
        print(f"Okay! I chose: {choice}")

    return choice

def generate_code(i_program_request):
    user_request = (f"Create a python program that adheres to the following: {i_program_request}. "
            "Do not write any explanations, just show me the code itself.\n Also, please include" 
                 " running unit tests with asserts that check the logic of the" 
                    "program. Make sure to also check interesting edge cases. Important - There should be at least\n" 
                        "10 different unit tests. Important - please add a prograss bar to the assertion tests" 
                            " and indicate if any failed or all passed. Add comments for important actions and computations.")
    instruction = ("You are a python program writer that adheres to the requests he gets."
            " Output only RAW CODE in response to a request. Good Example:\n"
                "'user': 'create a program that prints hello world'\n" 
                "'system': 'print('hello world')'\n"
                "Bad Examples:\n"
                "'user': 'I want binary search'\n" 
                "'system': '#Example function, x * x'\n"
                "'user': 'I want at least 10 tests'\n" 
                "'system': * creates 7 tests * \n"
                    "You can add python comments when appropriate however, do not include title such as '''python'''"
                        " in beggining of the answer, nor triple quotes at the end."
                        "Do not include a so called example function, unnecessary imports, or anything that is not the direct, raw answer to the request."
                        "VERY IMPORTANT - if including unit tests, use the assert keyword in the tests.")
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # Setting initial instruction.
        {"role": "system", "content": instruction },
        # First user request.
        {"role": "user", "content": user_request}
    ]

    )
    respone = completion.choices[0].message.content
    if respone is None:
        respone = ""
    return respone


# Save response to a file.
def save_code_to_file(i_generated_code, i_file_path="generatedCode.py"):
    with open(i_file_path, "w") as file:
        file.write(i_generated_code)

# Try to run the generated code, and return any errors.
def run_generated_code(i_file_path="generatedCode.py"):
    try:
        run_result = subprocess.run(["python", i_file_path], capture_output=True, text=True, check=True)
        print("Output: ", run_result.stdout)
        print("Code creation completed successfully!")
        os.startfile(i_file_path)
    except subprocess.CalledProcessError as e:
        return e.stderr
    return None


def main():
    program_request = get_program_request()
    for attempt in range(5):
        generated_code = generate_code(program_request)
        if generated_code == "":
            print("Code generation failed. trying again.")
            continue
        save_code_to_file(generated_code)
        error = run_generated_code()
        if error is None:
            break
        else:
            print(f"Attempt {attempt} run into an error running generated code! Error:{error}. Trying again")
            program_request += (f" this is the code {generated_code}. I encountered "
                f"the following error: {error}. Please fix the code.")
    if error is not None:
        print("FINAL - Code generation failed.")

if __name__ == "__main__":
    main()


