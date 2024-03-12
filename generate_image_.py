from textwrap import dedent
from openai import OpenAI

def generate_image(summary, paired_responses=None):
    """
    Generates an AI image of shoes inspired by the user's personality summary using DALL-E.

    Parameters:
    - summary: A string summary of the user's personality.
    - paired_responses: Optional. A list of paired questions and responses.

    Returns:
    - The URL of the generated image.
    """

    print (summary)
    print (paired_responses)
    # Generate an image prompt based on the user's personality summary
    prompt = dedent(f"""Create a photo of a pair of shoes against a neutral backdrop. The shoes should suit a person who has the following personality description: <<<<<{summary}>>>>>\n\nThe person recently answered a survey in this way: <<<<<{paired_responses}>>>>>.\n\nIt is CRITICAL that the prompt sent to DALL-E insists that DALL-E does not include any characters.""")

    print(prompt)

    try:
        from openai import OpenAI
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        print(response.data[0])
        return image_url

    except Exception as e:
        print(f"An error occurred while generating the image: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example summary
    example_summary = "Your personality is a mix of fashion-forward, earthy, peaceful, and classic."
    image_url = generate_image(example_summary)
    if image_url:
        print(f"Image generated successfully: {image_url}")
    else:
        print("Failed to generate image.")

