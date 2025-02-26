import os
from openai import OpenAI
from dotenv import load_dotenv
from context_information import manpower_available, layout_of_mall, fire_alarm_stations, fire_management_SOP

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Write a function that answers the user's question based on the chat thread
def answer_question(chat_thread : list) -> list:
    """
    :param chat_thread: The chat thread that we need to answer the user's question based on
    :type chat_thread: list
    :return: The updated chat thread with the answer to the user's question
    :rtype: list
    """
    # Use the OpenAI API to generate the answer to the user's question based on the chat thread
    prompt = f"""
            You are an AI assistant helping with dealing with a fire incident at a shopping mall.
            The user is a security officer seeking guidance on managing the situation and has been provided with a preliminary solution.
            The user is asking a follow-up question or seeking clarification on the provided solution.
            Please provide a detailed and informative response to assist the user effectively.

            This is a dynamic conversation, and you should adapt your responses based on the user's queries and the context of the conversation.

            Here is the whole chat thread for your reference: {chat_thread}
            The original manpower available is as follows: {manpower_available}
            The original layout of the mall is as follows: {layout_of_mall}
            The original fire alarm stations are as follows: {fire_alarm_stations}
            The fire management SOP is as follows: {fire_management_SOP}
              """
    messages = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response_content = completion.choices[0].message.content

    updated_conversation = chat_thread + [{"role": "assistant", "content": response_content}]
    # print("Answer to the user's question:", response_content)

    return updated_conversation