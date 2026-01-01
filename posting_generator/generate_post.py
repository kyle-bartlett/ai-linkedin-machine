import os
from openai import OpenAI

SUMMARIES_DIR = "queue/summaries/"
POSTS_DIR = "queue/posts/"
PROMPT = "Convert the following article summary into an engaging LinkedIn post. Make it professional, insightful, and include a call to action like 'What are your thoughts?' or 'Share your experiences!'. Keep it under 200 words."

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(summary_path):
    with open(summary_path, "r") as f:
        summary = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT + "\n\n" + summary}]
    )

    post = response.choices[0].message.content

    # Save post
    post_name = os.path.basename(summary_path).replace(".md", "_post.txt")
    post_path = os.path.join(POSTS_DIR, post_name)

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(post_path, "w") as f:
        f.write(post)

    print(f"[✓] Generated post → {post_path}")
    return post_path

def run_all():
    for file in os.listdir(SUMMARIES_DIR):
        if file.endswith(".md"):
            generate_post(os.path.join(SUMMARIES_DIR, file))

if __name__ == "__main__":
    run_all()