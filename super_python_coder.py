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
    "A program that calculates the factorial of a number using recursion.",
    "A program that sorts a list of integers using the quicksort algorithm."
]

def get_program_request():
    choice = input(("I’m Super Python Coder. Tell me, which program would you like me to code for you?\n"
         "If you don't have an idea, just press enter and"
          " I will choose a random program to code:"))
    if choice.strip() == "":
        choice = random.choice(PROGRAMS_LIST)

    return choice

def generate_code(i_program_request):
    user_request = (f"Create a python program that adheres to the following: {i_program_request}. "
            "Do not write any explanations, just show me the code itself.\n Also, please include" 
                 " running unit tests with asserts that check the logic of the" 
                    "program. Make sure to also check interesting edge cases. There should be at least\n" 
                        "10 different unit tests. important - please add a prograss bar to the assertion tests" 
                            " and indicate if any failed or all passed.")
    instruction = ("You are a python program writer that adheres to the requests he gets."
            " Output only RAW CODE in response to a request. Good Example:\n"
                "'user': 'create a program that prints hello world'\n" 
                "'system': 'print('hello world')'\n"
                "Bad Example:\n"
                "'user': 'I want binary search'\n" 
                "'system': '#Example function, x * x'\n"
                    "You can add python comments when appropriate however, do not include title such as '''python'''"
                        " in beggining of the answer, nor triple quotes at the end."
                        "Do not include a so called example function, unnecessary imports, or anything that is not the direct, raw answer to the request.")
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
        run_result = subprocess.run(["python", i_file_path], capture_output=True, text=True)
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
            program_request += (f" this is the code {generated_code}. I encountered "
                f"the following error: {error}. Please fix the code.")
    if error is not None:
        print("FINAL - Code generation failed.")

if __name__ == "__main__":
    main()


