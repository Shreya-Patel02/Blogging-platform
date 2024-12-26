from openai import OpenAI
client = OpenAI()
def generate_content(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=50
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def generate_tags(content):
    prompt = f"Generate relevant tags for the following content:\n\n{content}"
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=50
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating tags: {e}")
        return None
