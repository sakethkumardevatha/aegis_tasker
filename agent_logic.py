import os
from groq import Groq

def classify_task_with_ai(task_description):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    You are an AI Engineering Assistant. Categorize the following task into exactly ONE of these categories: 
    'DSA', 'ML Theory', 'ML Math', 'Project', or 'Tools'.
    
    Task: {task_description}
    
    Return ONLY the category name.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"