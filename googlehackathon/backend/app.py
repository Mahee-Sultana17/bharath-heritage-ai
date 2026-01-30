from flask import Flask, render_template, request, jsonify
from groq import Groq
import requests
import urllib.parse
import time
import re

app = Flask(__name__)

# ================== API KEY ==================
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ================== DATA ==================
PLACES = {
    "taj-mahal": {"name": "Taj Mahal", "lat": 27.1751, "lng": 78.0421, "img": "taj.jpg"},
    "hampi": {"name": "Hampi", "lat": 15.3350, "lng": 76.4600, "img": "hampi.jpg"},
    "konark": {"name": "Konark Sun Temple", "lat": 19.8876, "lng": 86.0945, "img": "konark.jpg"},
    "ajanta": {"name": "Ajanta Caves", "lat": 20.5519, "lng": 75.7033, "img": "ajanta.jpg"},
    "varanasi": {"name": "Varanasi Ghats", "lat": 25.3176, "lng": 82.9739, "img": "varanasi.jpg"},
    "meenakshi": {"name": "Meenakshi Temple", "lat": 9.9195, "lng": 78.1193, "img": "meenakshi.jpg"},
    "redfort": {"name": "Red Fort", "lat": 28.6562, "lng": 77.2410, "img": "redfort.jpg"},
    "statue": {"name": "Statue of Unity", "lat": 21.8380, "lng": 73.7191, "img": "statue.jpg"},
    "charminar": {"name": "Charminar", "lat": 17.3616, "lng": 78.4747, "img": "charminar.jpg"},
    "mysore": {"name": "Mysore Palace", "lat": 12.3051, "lng": 76.6551, "img": "mysore.jpg"},
    "khajuraho": {"name": "Khajuraho Temples", "lat": 24.8318, "lng": 79.9199, "img": "khajuraho.jpg"},
    "sanchi": {"name": "Sanchi Stupa", "lat": 23.4793, "lng": 77.7399, "img": "sanchi.jpg"},
}

ARTS = {
    "kathakali": {"name": "Kathakali", "img": "kathakali.jpg"},
    "bharatanatyam": {"name": "Bharatanatyam", "img": "bharatanatyam.jpg"},
    "yakshagana": {"name": "Yakshagana", "img": "yakshagana.jpg"},
    "kathak": {"name": "Kathak", "img": "kathak.jpg"},
    "madhubani": {"name": "Madhubani Painting", "img": "madhubani.jpg"},
    "chhau": {"name": "Chhau Dance", "img": "chhau.jpg"},
    "odissi": {"name": "Odissi Dance", "img": "odissi.jpg"},
    "kalaripayattu": {"name": "Kalaripayattu", "img": "kalaripayattu.jpg"},
}

FESTIVALS = {
    "diwali": {"name": "Diwali", "img": "diwali.jpg"},
    "pongal": {"name": "Pongal", "img": "pongal.jpg"},
    "navratri": {"name": "Navratri", "img": "navratri.jpg"},
    "holi": {"name": "Holi", "img": "holi.jpg"},
    "onam": {"name": "Onam", "img": "onam.jpg"},
    "durga": {"name": "Durga Puja", "img": "durga.jpg"},
    "ganesh": {"name": "Ganesh Chaturthi", "img": "ganesh.jpg"},
    "ramzan": {"name": "Ramzan (Eid-ul-Fitr)", "img": "ramzan.jpg"},
}

# ================== WIKI TITLE FIX ==================
WIKI_TITLE_FIX = {
    "Varanasi Ghats": "Ghats in Varanasi",
    "Khajuraho Temples": "Khajuraho Group of Monuments",
    "Chhau Dance": "Chhau dance",
    "Odissi Dance": "Odissi",
    "Pongal": "Pongal (festival)",
    "Ramzan (Eid-ul-Fitr)": "Eid al-Fitr",
}

# ================== MARKDOWN CLEANER ==================
def clean_markdown(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"^\s*[-*]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()

# ================== ROUTES ==================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/category/<cat>")
def category(cat):
    if cat == "places":
        data = PLACES
    elif cat == "arts":
        data = ARTS
    else:
        data = FESTIVALS
    return render_template("category.html", category=cat, items=data)

@app.route("/detail/<cat>/<key>")
def detail(cat, key):
    if cat == "places":
        item = PLACES[key]
    elif cat == "arts":
        item = ARTS[key]
    else:
        item = FESTIVALS[key]
    return render_template("detail.html", category=cat, key=key, item=item)

# ================== AI GENERATION ==================
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    name = data["name"]
    category = data["category"]
    language = data["language"]

    if language == "English":
        lang_instruction = "Write in English."
    elif language == "Hindi":
        lang_instruction = "Write ONLY in Hindi using Devanagari script."
    elif language == "Kannada":
        lang_instruction = "Write ONLY in Kannada script."
    elif language == "Telugu":
        lang_instruction = "Write ONLY in Telugu script."
    elif language == "Marathi":
        lang_instruction = "Write ONLY in Marathi using Devanagari script."
    else:
        lang_instruction = "Write in English."

    prompt = f"""
You are an expert Indian heritage historian.

Write a VERY LONG, DETAILED, PROFESSIONAL museum-style article about:

{name}
Category: {category}

CRITICAL RULES:
- {lang_instruction}
- Do NOT use markdown
- Do NOT use symbols
- Do NOT use bullets
- Do NOT mention AI
- Write MINIMUM 600-800 words
- Write clean natural paragraphs
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )

    raw_text = completion.choices[0].message.content.strip()
    text = clean_markdown(raw_text)

    return jsonify({"text": text})

# ================== WIKI IMAGES ==================
@app.route("/wiki_images")
def wiki_images():
    title = request.args.get("title")
    images = []

    try:
        wiki_title = WIKI_TITLE_FIX.get(title, title)
        safe_title = wiki_title.replace(" ", "_")

        headers = {"User-Agent": "Mozilla/5.0"}

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe_title}"
        r = requests.get(summary_url, headers=headers, timeout=10)
        data = r.json()

        if "originalimage" in data:
            images.append(data["originalimage"]["source"])
        elif "thumbnail" in data:
            images.append(data["thumbnail"]["source"])

        page_url = f"https://en.wikipedia.org/wiki/{safe_title}"
        html = requests.get(page_url, headers=headers, timeout=10).text

        matches = re.findall(r'src="(https://upload.wikimedia.org/[^"]+)"', html)

        for m in matches:
            if any(ext in m.lower() for ext in [".jpg", ".jpeg", ".png"]):
                if m not in images:
                    images.append(m)

    except Exception as e:
        print("Wiki error:", e)

    return jsonify(images[:8])

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
