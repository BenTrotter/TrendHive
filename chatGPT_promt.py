
from openai import OpenAI
import os


MY_API_KEY = os.getenv("CHAT_GPT_API_KEY")


def get_prompt():
    topic = input("\n\nPlease enter your topic: ")
    prompt = (
        f"I want you to act as a YouTube content creator, creating Youtube shorts on a broad range of "
        f"topics relating to the latest trends. I will send you a keyword that will be a "
        f"recently searched trend on YouTube. I want you to find out why this is trending on the "
        f"web (so that your information is up to date) and then find out about the trend. Use what "
        f"you find about the trend to write a script for a 50 second video. The video should be "
        f"informative, entertaining, and catch people's attention by spiking curiosity. Please start "
        f"with a clickbait title for this video, and then provide the script. Your output should "
        f"be a title introduced with 'Title: (YOUR TITLE)', then script introduced with 'Script: (YOUR SCRIPT)', "
        f"and then a video description, introduced with 'Description: (DESCRIPTION)'. Please stick to this structure."
        f"Do not add sources, do not add special characters, do not ask for comments below "
        f"and do not introduce or end of the channel as the script is for Youtube Shorts Your topic today is: {topic}"
    )
    print("\n\nTHIS IS THE PROMPT\n\n" + prompt + "\n\n")
    return prompt


def call_chat_gpt(prompt):
    client = OpenAI(api_key = MY_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are youtube content creator"},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("\nTHIS IS WHAT CHATGPT CAME UP WITH:\n\n" + completion.choices[0].message.content + "\n\n")
    return completion.choices[0].message.content


def extract_title(text):
    title_prefix = "Title: "
    if title_prefix in text:
        start_pos = text.find(title_prefix) + len(title_prefix)
        rest_of_text = text[start_pos:]
        end_pos = rest_of_text.find('\n')
        if end_pos == -1:
            end_pos = len(rest_of_text)
        title = rest_of_text[:end_pos].strip()
        return title
    else:
        return "Title not found, please rename"
    

def extract_and_remove_description(input_string):
    description_start = input_string.find("Description:")
    if description_start == -1:
        return input_string, ""
    description_content = input_string[description_start + len("Description:"):].strip()
    updated_string = input_string[:description_start].strip()
    return updated_string, description_content


def get_title_prompt_description():
    prompt = get_prompt()
    generated_prompt = call_chat_gpt(prompt)
    title = extract_title(generated_prompt)
    generated_prompt, description = extract_and_remove_description(generated_prompt)
    return title, generated_prompt, description


if __name__ == "__main__":
    get_title_prompt_description()