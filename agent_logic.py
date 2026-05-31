import os
from groq import Groq

def generate_rpg_side_quest(user_mood_or_topic):
    """The AI plays Game Master, creating contextual micro-missions to circumvent analytical burnout."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    You are the 'Aegis Core OS Game Master' directing an early-career engineer transitioning to GenAI and Backend Architectures.
    The player is expressing fatigue or wants a creative micro-mission related to: "{user_mood_or_topic}".
    
    Generate ONE specific, highly practical, engaging, but very simple 'Side Quest' that can be achieved in under 15 minutes. 
    It should not feel like an abstract homework problem. Make it look like a low-pressure scouting assignment.
    
    Examples:
    - "Investigate the GitHub Trending page for Python repositories, pick one library you've never heard of, and look up its main purpose."
    - "Open a text terminal on your machine, type `docker stats`, observe the default live performance numbers, and exit."
    
    Provide your output strictly in this plain format:
    Mundane Goal: [Short, understandable name of quest]
    Directive: [Clear instructions on what simple step to perform]
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=150
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Mundane Goal: Quick Clean\nDirective: API temporary offline. Go review your script lines for trailing blank variables."