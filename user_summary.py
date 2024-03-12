import os
from textwrap import dedent
from groq import Groq
from openai import OpenAI

def summarize_user_responses(question_answer_pairs):
    """
    Uses Groq to generate an assertive summary of the user's personality based on quiz responses.
    
    Parameters:
    - question_answer_pairs: A JSON string containing pairs of questions and the user's selected answers.
    
    Returns:
    - An assertive string summary of the user's personality.
    """
    # client = Groq()
    client = OpenAI()

    # prompt = dedent(f"""A user gave these secret responses to a personality quiz: <<<<<{question_answer_pairs}>>>>>. You may not refer or allude to the responses directly or indirectly.
    # Scrub all specifics / examples from the quiz and write a very short personality summary by making bold inferences. You should embellish to be clever and fun. Your response starts with with: 'You are ...'""")

    prompt = dedent(f"""A user gave these secret responses to a personality quiz: <<<<<{question_answer_pairs}>>>>>. You may not refer or allude to the responses directly or indirectly.
    Scrub all specifics / examples from the quiz and write a 7-sentence personality summary by making bold inferences. You should embellish to be clever and fun. Your response starts with with: 'You are ...'""")

    for attempt in range(3):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                # model="mixtral-8x7b-32768",
                model="gpt-4-turbo-preview",
                temperature=0.5,
            )
            # temp = chat_completion.choices[0].message.content

            # prompt = dedent(f"""The user is described by: <<<<<{temp}>>>>>. Without restating any of the specific examples or indirectly, write a 7-sentence paragraph about the user's personality and tendencies (like an MBTI summary). You make inferences without explicitly referencing the user's actions / statements / preferences. You should embellish a bit to be clever and fun. Your response starts with with: 'You are a ...'""")

            # chat_completion = client.chat.completions.create(
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": prompt,
            #         }
            #     ],
            #     # model="mixtral-8x7b-32768",
            #     model="gpt-4-turbo-preview",
            #     temperature=0.5,
            # )
            return chat_completion.choices[0].message.content





        except Exception as e:
            if attempt < 2:  # Only print error message if not on last attempt
                print(f"Attempt {attempt + 1} failed with error: {e}")
            temp = "Error generating completion. Please try again."


# Example usage
if __name__ == "__main__":
    # Example question and answer pairs in JSON format
    example_question_answer_pairs = '[{"question": "What\'s your go-to activity on a free afternoon?", "answer": "Reading a book at a cozy cafe"}, {"question": "Choose a color palette that speaks to you.", "answer": "Pastels: Light Pink, Baby Blue, Lavender"}]'
    summary = summarize_user_responses(example_question_answer_pairs)
    print(summary)

