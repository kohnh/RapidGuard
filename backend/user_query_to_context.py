import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Write a function that takes a chat thread and adds additional context about the fire situation, for instance, a change in the manpower, malfunction of certain equipment, etc, to user_context.txt
def get_context_from_user_query(chat_thread : list) -> None:
    """
    :param user_query: The chat thread that we need to extract additional context from, based on the last user query
    :type user_query: list
    :return: None (The additional context is written to user_context.txt)
    """
    # Use the OpenAI API to generate the additional context based on the user query
    prompt = f"""
             The user is the head of the security guard department who is responsible for monitoring the CCTV cameras in a shopping mall.
             A fire has broken out in the shopping mall and the a solution has been generated using the AI assistant.

             The user has provided additional context about the fire situation.

             Extract the additional context from the user's latest message and return it, without any additional information, headers or introduction.

             Here is the whole chat thread for your reference:
             {chat_thread}
              """
    messages = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response_content = completion.choices[0].message.content
    print("Additional context extracted from the user query:", response_content)

    # Create or update the user_context.txt file with the additional context
    if not os.path.exists("user_context.txt"):
        with open("user_context.txt", "w") as f:
            f.write(response_content + "\n")

    else:
        with open("user_context.txt", "a") as f:
            f.write(response_content + "\n")

