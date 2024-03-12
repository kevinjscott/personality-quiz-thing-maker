import os
from textwrap import dedent
import fal
from groq import Groq

def generate_image(summary, paired_responses=None, engine="fal", item="shoes"):
    """
    Generates an AI image of shoes inspired by the user's personality summary using Stable Diffusion.

    Parameters:
    - summary: A string summary of the user's personality.
    - paired_responses: Optional. A list of paired questions and responses.

    Returns:
    - The URL of the generated image.
    """

    # print(paired_responses)
    client = Groq()
    groq_prompt = dedent(f"""Given the following user personality summary: <<<<{summary}>>>>, and their responses to a survey: <<<<{paired_responses}>>>>, create a stable diffusion prompt for a beautiful product photo that DESCRIBES a pair of {item} that reflects this person's personality. Neutral / simple background. Be sure to include gender and any other relevant details and to write the prompt as descriptive statements rather than commands or announcements. Be very literal about what should appeaer in the photo."
    """)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": groq_prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.1,
    )

    generated_prompt = chat_completion.choices[0].message.content
    print(generated_prompt)

    if engine == "fal":
        # hit the fal API
        request_json = {
            "prompt": generated_prompt,
            "negative_prompt": "cartoon, illustration, animation, sketch. face. unrealistic.",
            "image_size": "square_hd",
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
            "num_images": 1,
            "loras": [],
            "enable_safety_checker": True,
            "sync_mode": True
        }

        try:
            handler = fal.apps.submit("fal-ai/fast-sdxl", arguments=request_json)
            result = handler.get()
            image_b64 = result['images'][0]['url']
            return image_b64

        except Exception as e:
            print(f"An error occurred while generating the image: {e}")
            return None

    elif engine == 'dall-e-3':
        # use dall-e API
        try:
            from openai import OpenAI
            client = OpenAI()

            response = client.images.generate(
                model="dall-e-3",
                prompt=generated_prompt + "\n\nYou must not deviate from this prompt when you pass it to DALL-E. Send it exactly as above or lives will be lost. The only thing you must add is that the image may not contain any characters or text.",
                size="1024x1024",
                style="vivid",
                quality="hd",
                n=1,
            )

            image_url = response.data[0].url
            return image_url

        except Exception as e:
            print(f"An error occurred while generating the image with DALL-E: {e}")
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

