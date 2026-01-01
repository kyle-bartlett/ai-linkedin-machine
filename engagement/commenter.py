import os
import time
import random
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI

PERSONAS_CONFIG = "config/personas.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def load_personas():
    with open(PERSONAS_CONFIG, "r") as f:
        return json.load(f)["personas"]

def login(driver, persona):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(persona["email"])
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(persona["password"])
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(5)

def get_top_posts(driver, num_posts=5):
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(5)
    posts = driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")[:num_posts]
    post_data = []
    for post in posts:
        try:
            text_element = post.find_element(By.XPATH, ".//div[contains(@class, 'feed-shared-text')]")
            text = text_element.text
            post_id = post.get_attribute("data-urn").split(":")[-1] if post.get_attribute("data-urn") else str(random.randint(1000,9999))
            timestamp_element = post.find_element(By.XPATH, ".//time")
            timestamp = timestamp_element.get_attribute("datetime")
            post_data.append({"id": post_id, "text": text, "timestamp": timestamp})
        except:
            continue
    return post_data

def is_recent(timestamp, hours=24):
    if not timestamp:
        return False
    post_time = datetime.fromisoformat(timestamp[:-1])  # Remove Z
    return datetime.utcnow() - post_time < timedelta(hours=hours)

def generate_comment(post_text):
    prompt = f"Generate an engaging comment for this LinkedIn post that will likely draw replies. Make it insightful and question-based. Post: {post_text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def comment_on_post(driver, post_element, comment_text):
    try:
        comment_button = post_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Comment')]")
        comment_button.click()
        time.sleep(2)
        comment_box = post_element.find_element(By.XPATH, ".//div[@role='textbox']")
        comment_box.send_keys(comment_text)
        time.sleep(1)
        post_button = post_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Post comment')]")
        post_button.click()
        time.sleep(3)
    except Exception as e:
        print(f"Error commenting: {e}")

def run_commenter():
    personas = load_personas()
    for persona in personas:
        if "linkedin" in persona["behavior"]["platforms"]:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            login(driver, persona)
            top_posts = get_top_posts(driver)

            for post in top_posts:
                if is_recent(post["timestamp"]):
                    comment = generate_comment(post["text"])
                    # TODO: Implement actual commenting
                    print(f"Persona {persona['name']} would comment on post {post['id']}: {comment}")

            driver.quit()
            time.sleep(30)  # Delay between personas

if __name__ == "__main__":
    run_commenter()