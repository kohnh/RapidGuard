import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Write a function that takes a chat thread and decides if the last message is a question or a context update
def is_question_or_context(chat_thread : list) -> str:
    """
    :param chat_thread: The chat thread that we need to determine if the last message is a question or a context update
    :type chat_thread: list
    :return: The type of the last message - 'question' or 'context'
    :rtype: str
    """
    # Use the OpenAI API to classify the last message in the chat thread as a question or a context update
    prompt = f"""
             The user is the head of the security guard department who is responsible for monitoring the CCTV cameras in a shopping mall.
             A fire has broken out in the shopping mall and the a solution has been generated using the AI assistant.

             The user has sent a message. Determine if the last message in the chat thread is a question or a context update.
             A question is a query seeking information, while a context update is additional information provided by the user, for instance, a change in the situation such as a security personnel is sick, a new development such as the fire blocking an emergency exit, etc.

             Determine if the last message in the chat thread is a question or a context update.

             If the last message is a question, return 'question'.
             If the last message is a context update, return 'context'.
             Do not include any additional information, headers or introduction.

             Here is the whole chat thread for your reference:
             {chat_thread}
              """
    messages = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response_content = completion.choices[0].message.content

    print("Type of the last message in the chat thread:", response_content)

    return response_content
