import os
from openai import OpenAI
from dotenv import load_dotenv
from context_information import manpower_available, layout_of_mall, fire_alarm_stations, fire_management_SOP

# Load environment variables from .env file
load_dotenv()

# Create the OpenAI client using your API key from the environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Write a function that takes in the latest fire situation and context from the user and generates a new solution
def generate_solution() -> str:
    """
    :return: The new solution generated based on the updated fire situation and user context
    :rtype: str
    """

    # Get the latest fire situation from fire_context.txt if it exists
    if os.path.exists("fire_context.txt"):
        with open("fire_context.txt", "r") as f:
            # Read whole file content
            image_context = f.read().strip()
            print("Fire context:", image_context)
    else:
        image_context = "No additional context provided about the fire situation."

    # Get the latest context from user_context.txt if it exists
    if os.path.exists("user_context.txt"):
        with open("user_context.txt", "r") as f:
            user_context = f.read().strip()
            print("User context:", user_context)
    else:
        user_context = "No additional context provided by the user."

    # Use the OpenAI API to generate a new solution based on the updated fire situation and user context
    prompt = f"""
            You are the head of security at the shopping mall. 
            
            You have been alerted to a potential fire through the CCTV system. 
            
            You are to come up with detailed actionable steps using each security guard's name to manage the situation with the security team with reference to the fire response and management SOP, context of the fire, and the manpower available, using the following format below as a guide, do not include any headers, introduction or conclusion, if there are any steps that are not applicable or has been completed, please indicate so:

            # Fire Response and Management Plan

            There are <insert number of security guards present> security guards and <insert number of security managers present> security manager on duty today.
            The security guards are as follows: <names of security guards, separated by commas>.
            The security manager is <name of security manager>.

            <Insert summary of the fire situation based on the context provided>
            <Insert summary of the user context provided>

            In response to the fire detected at <insert location of fire> on <insert date and time fire started>, here is a step-by-step plan for managing the situation based on the given SOP, fire context, and available manpower:

            ## Phase 1: Immediate Detection & Initial Response (0–1 Minute)
            <insert steps based on the SOP, contextualized to the situation>

            ## Phase 2: Emergency Communication & Service Contact (1–2 Minutes)
            <insert steps based on the SOP, contextualized to the situation>

            ## Phase 3: Evacuation Coordination (2–5 Minutes)
            <insert steps based on the SOP, contextualized to the situation>

            ## Phase 4: On-Site Fire Suppression (If Safe and Trained) (0–10 Minutes)
            <insert steps based on the SOP, contextualized to the situation>

            ## Phase 5: Ongoing Communication & Coordination (Throughout Incident)
            <insert steps based on the SOP, contextualized to the situation>

            ## Phase 6: Securing the Premises & Post-Incident Procedures (After 10 Minutes)
            <insert steps based on the SOP, contextualized to the situation>

            
            Here are the details you need to consider:
            The context of the fire is as follows: {image_context}
            The manpower available is as follows: {manpower_available}
            The context provided by the user is as follows: {user_context}
            The layout of the mall is as follows: {layout_of_mall}
            The fire alarm stations are as follows: {fire_alarm_stations}
            The fire management SOP is as follows: {fire_management_SOP}
            """
            
    messages = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    response_content = completion.choices[0].message.content
    print("New solution generated based on the updated fire situation and user context:", response_content)

    return response_content