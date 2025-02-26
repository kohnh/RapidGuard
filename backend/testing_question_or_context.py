from question_or_context import is_question_or_context

chat_thread = [
    {"role": "system", "content": "You are an AI assistant helping with dealing with a fire incident at a shopping mall."},
    {"role": "user", "content": "What should I do if the fire is blocking the main entrance?"},
    {"role": "assistant", "content": "If the fire is blocking the main entrance, you should direct people to the nearest emergency exit."},
    {"role": "user", "content": "One of the security personnel is sick today."},
]

chat_thread_2 = [
    {"role": "system", "content": "You are an AI assistant helping with dealing with a fire incident at a shopping mall."},
    {"role": "user", "content": "What should I do if the fire is blocking the main entrance?"},
    {"role": "assistant", "content": "If the fire is blocking the main entrance, you should direct people to the nearest emergency exit."},
    {"role": "user", "content": "Where is the fire located?"},
]

chat_thread_3 = [
    {"role": "system", "content": "You are an AI assistant helping with dealing with a fire incident at a shopping mall."},
    {"role": "user", "content": "What should I do if the fire is blocking the main entrance?"},
    {"role": "assistant", "content": "If the fire is blocking the main entrance, you should direct people to the nearest emergency exit."},
    {"role": "user", "content": "The fire has spread to the food court area."},
]

assert(is_question_or_context(chat_thread) == "context")
assert(is_question_or_context(chat_thread_2) == "question")
assert(is_question_or_context(chat_thread_3) == "context")

