import os
import json
import random
from textwrap import dedent
from groq import Groq
from openai import OpenAI

def generate_new_questions():
    """
    Uses Groq to generate a new set of questions for a buzzfeed style survey.
    
    Returns:
    - A JSON object containing 4 new questions.
    """
    # client = Groq()
    client = OpenAI()
    prompt = dedent("""Create an original buzzfeed-style survey in json format. 5 questions. No talk. Just do. A correct response would have the same json structure as the following example...

    {
      "questions": [
        {
          "question": str,
          "options": [
            str1,
            str2,
            str3,
            str4
          ]
        },
        {
          "question": str,
          "options": [
            str1,
            str2,
            str3,
            str4
          ]
        },
        etc.
      ]
    }

   
    ok let's get started.Your response starts with...

    {"questions": [

    """)

    for attempt in range(3):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you only respond with valid json on a single line with no additional characters or chatter or comments. Your responses start with {\"questions\": [\","
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-4-turbo-preview",
                temperature=0.8,
                max_tokens=2000,
            )
            new_questions_json = json.loads(chat_completion.choices[0].message.content)
            with open('./static/js/quiz_questions.json', 'w') as file:
                json.dump(new_questions_json, file, indent=4)
            # print(new_questions_json)
            break  # Break the loop if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt == 2:  # If last attempt also fails
                print("Failed to generate new questions after 3 attempts.")

if __name__ == "__main__":
    generate_new_questions()
