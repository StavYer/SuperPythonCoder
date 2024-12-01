"""Module for interfacing with the OpenAI API."""
import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv('API_KEY')
client = OpenAI(api_key=API_KEY)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # Setting initial instruction.
        {"role": "system", "content": "You are a python program writer. \
            Output only code in response to a request. \
                Example - 'user': 'create a program that prints hello world', \
                     'system': 'print('hello world')'. \
                        You can add python comments when appropriate,\
                             however, do not include title such as '''python''' in beggining of the answer.\
                                just include raw python code and comments - if you want to make examples \
                                    make them in comment."},
        # First user request.
        {"role": "user", "content": "Create a python program that checks if a number is prime. \
             Do not write any explanations, just show me the code itself. Also, please include \
                 running unit tests with asserts that check the logic of the \
                    program. Make sure to also check interesting edge cases. There should be at least \
                        10 different unit tests. Also, add a prograss bar to the assertion tests \
                            and indicate if any failed or all passed."}
    ]

)

# Extract respone from gpt-4o-mini.
response = completion.choices[0].message.content

# Save response to a file.

with open("generatedCode.py", "w") as file:
    file.write(response)


# Run the generated code.

run_result = subprocess.run(["python", "generatedCode.py"], capture_output=True, text=True)

print("Output: ", run_result.stdout)

print("Error: ", run_result.stderr)

