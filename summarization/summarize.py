import os, json, datetime
from summarization.safety_filter import violates_safety
from openai import OpenAI

RAW_DIR = "queue/incoming_raw/"
OUT_DIR = "queue/summaries/"
PROMPT_PATH = "summarization/prompt_templates/default.txt"
SAFETY_PROMPT_PATH = "summarization/prompt_templates/employer_neutral.txt"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt():
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def load_safety_prompt():
    with open(SAFETY_PROMPT_PATH, "r") as f:
        return f.read()

def summarize_article(article_path):
    with open(article_path, "r") as f:
        data = json.load(f)

    raw = load_prompt() + "\n" + data.get("summary_raw", "")

    # PRIMARY SUMMARY PASS
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": raw}]
    )

    text = response.choices[0].message.content

    # SAFETY PASS
    if violates_safety(text):
        safety_prompt = load_safety_prompt() + "\n" + text
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": safety_prompt}]
        )
        text = response.choices[0].message.content

    # WRITE OUTPUT
    out_name = os.path.basename(article_path).replace(".json", ".md")
    out_path = os.path.join(OUT_DIR, out_name)

    with open(out_path, "w") as f:
        f.write(text)

    print(f"[✓] Summarized → {out_path}")

def run_all():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".json"):
            summarize_article(os.path.join(RAW_DIR, file))

if __name__ == "__main__":
    run_all()
