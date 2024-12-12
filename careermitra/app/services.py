import openai
from django.conf import settings

openai.api_key = ""
def get_openai_response(user_input, context=None):
    prompt = f"""
    You are a career counseling assistant. Answer the following questions related to career paths, educational streams, and career guidance.

    Context: {context if context else ""}
    
    Student says: {user_input}

    Respond as a counselor:
    """
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    
    return response.choices[0].text.strip()
