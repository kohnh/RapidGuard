from user_query_to_context import get_context_from_user_query

get_context_from_user_query([
    {"role": "user", "content": "Where is the fire?"}, 
    {"role": "assistant", "content": "The fire has been detected on Level 1 (East Wing) of the shopping mall, near the escalator leading to Level 2, close to the 'Coffee Bean' cafe and 'Cosmetics Corner.'"},
    {"role": "user", "content": "Sarah is sick today."},
    {"role": "assistant", "content": "I have modified the solution to account for 1 less person."},
    {"role": "user", "content": "The fire has blocked off the main entrance to the shopping mall, I dont know what to do now. Help me."}
    ])