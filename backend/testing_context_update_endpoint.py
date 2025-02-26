import requests

# url_ask = "http://54.161.142.111:5000/context_update"
url_ask = "http://127.0.0.1:5000/context_update"

payload_context_update = {
    "conversation":[
    {"role": "assistant", "content": """
There are 5 security guards and 1 security manager on duty today. The security guards are as follows: John Tan, Mary Lim, Ali Hassan, Sarah Lee, and Peter Wong. The security manager is Rajesh Kumar.

There is a medium fire detected at Level 1 (West Wing): Central corridor area, beside the 'Grand Bookstore' and directory board on Wed Feb 26 12:46:57 2025. It is about 3 square meters in size. The fire is likely to be of kitchen or display-related nature, located at the Kixtois store window display. The fire appears to be contained within the display area, and there are people nearby in the store. The corridor is still accessible 
with people walking by. The fire has blocked off the main entrance to the shopping mall. Sarah is sick today.

In response to the fire detected at Kixtois store window display on Wed Feb 26 12:46:57 2025, here is a step-by-step plan for managing the situation based on the given SOP, fire context, and available manpower:

## Phase 1: Immediate Detection & Initial Response (0–1 Minute)

1. Detection & Alarm Activation:
   - Mary Lim, stationed at the west entrance, is closest to the fire and should activate the nearest fire alarm pull station located near 'Home 
Essentials.'
   - Mary Lim then immediately informs Rajesh Kumar via radio about the fire's confirmation.

2. Notification:
   - Rajesh Kumar, upon confirmation, alerts John Tan at the east entrance to prepare for evacuation procedures and Ali Hassan on the second floor to assist in crowd control given Sarah's absence.
   - Timing: To be completed within the first 1 minute.

## Phase 2: Emergency Communication & Service Contact (1–2 Minutes)

1. Call to Emergency Services:
   - Rajesh Kumar, as the Communication Officer, calls 911 providing the mall name, address, specific location of the fire, and situation details.

2. Public Alert:
   - Rajesh Kumar uses the PA system to announce: “Attention: Fire emergency at Level 1 West Wing, Kixtois display area. Evacuate immediately via the nearest safe exit. Do not use elevators.”

## Phase 3: Evacuation Coordination (2–5 Minutes)

1. Activation of Evacuation Teams:
   - With Sarah sick, Ali Hassan is assigned as the Evacuation Coordinator for the second floor, directing occupants away from the area and towards the east exit.
   - Mary Lim assists ground floor evacuation, ensuring clear directives for evacuation through the west entrance.

2. Route Clearance & Crowd Control:
   - John Tan directs people towards the east entrance and ensures no bottlenecks form, maintaining access is clear.
   - Peter Wong, on the third floor, confirms routes remain unobstructed, evacuating floors sequentially towards the east wing exits.

## Phase 4: On-Site Fire Suppression (If Safe and Trained) (0–10 Minutes)

1. Decision to Engage Fire:
   - With adequate training, John Tan and Mary Lim assess if the fire is safely addressable using extinguishers. Given its display-related nature, and blockage of main entrance, they prepare to act following PASS method.
   - Priority is to ensure their own safety first, ceasing attempts if fire spreads beyond control.

## Phase 5: Ongoing Communication & Coordination (Throughout Incident)

1. Regular Updates:
   - Ali Hassan, as the acting Floor Supervisor for the second floor, reports status every 2 minutes via radio to Rajesh Kumar.
   - Coordination continued between Peter Wong and John Tan to report evacuation statuses.

2. Liaison with Firefighters:
   - Rajesh Kumar prepares to meet arriving firefighters, providing them with schematics and relevant building access keys.

## Phase 6: Securing the Premises & Post-Incident Procedures (After 10 Minutes)

1. Securing the Mall:
   - Rajesh Kumar ensures no re-entry is allowed until declared safe, conducting exit locks and monitoring with Peter Wong.

2. Incident Documentation:
   - Rajesh Kumar, along with each security guard, submits incident report comprising alarm times, evacuation clearances, action taken, and any challenges.
   - With adequate training, John Tan and Mary Lim assess if the fire is safely addressable using extinguishers. Given its display-related nature, and blockage of main entrance, they prepare to act following PASS method.
   - Priority is to ensure their own safety first, ceasing attempts if fire spreads beyond control.
     """}
]
}

response_context_update = requests.post(url_ask, json=payload_context_update)
print("\nUpdate in context triggered new solution: \n")
print(response_context_update.json().get('conversation'))
