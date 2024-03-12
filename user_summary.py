import os
from groq import Groq

def summarize_user_responses(question_answer_pairs):
    """
    Uses Groq to generate an assertive summary of the user's personality based on quiz responses.
    
    Parameters:
    - question_answer_pairs: A JSON string containing pairs of questions and the user's selected answers.
    
    Returns:
    - An assertive string summary of the user's personality.
    """
    # Initialize Groq client with your API key
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Prepare the prompt for Groq
    prompt = f"Given the following user responses to a personality quiz: {question_answer_pairs}, " \
             "generate 5-sentences: a creative and assertive summary of the user's personality. Be clever and provocative. Just give the summary text without being chatty or restating the user's answers. Use 2nd person voice. Start with: 'You are a ...'"

    # Perform a chat completion to generate a summary
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=1.0,
    )

    # Return the generated summary
    return chat_completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    # Example question and answer pairs in JSON format
    example_question_answer_pairs = '[{"question": "What\'s your go-to activity on a free afternoon?", "answer": "Reading a book at a cozy cafe"}, {"question": "Choose a color palette that speaks to you.", "answer": "Pastels: Light Pink, Baby Blue, Lavender"}]'
    summary = summarize_user_responses(example_question_answer_pairs)
    print(summary)

