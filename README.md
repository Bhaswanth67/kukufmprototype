# 🎧 Kuku FM Daily Audio Briefing Prototype

This is a Streamlit-based prototype for a personalized audio content platform inspired by Kuku FM. It provides users with daily episode recommendations across genres and generates custom stories with audio playback.

---

## 🌟 Features

### 📌 Daily Briefing
- Select preferred **genres** (Thriller, Comedy, Drama, Romance).
- Option to add a **surprise pick** for more discovery.
- Recommendations are presented with **summaries and audio playback** using `gTTS`.

### 🧠 AI Story Generator
- Enter up to **3 custom keywords** or get random ones.
- Set a desired word count (100–5000 words).
- The story is generated using **Google's Gemini 2.0 Flash model**, chunked into coherent parts.
- Output includes both **readable text** and an **audio narration**.

### 🔊 Audio Features
- Uses **Google Text-to-Speech (gTTS)** to convert summaries and stories to audio.
- Instant **audio playback** within the app.

### ⚙️ Sidebar Features
- **Language selection** (currently English; other languages coming soon).
- Placeholder for **past briefings** and **user feedback submission**.

---

## 🛠️ Tech Stack

| Component           | Technology                        |
|--------------------|-----------------------------------|
| Frontend           | Streamlit                         |
| AI Model           | Gemini 2.0 Flash (Google Generative AI) |
| Audio Generation   | gTTS (Google Text-to-Speech)      |
| Environment Config | `python-dotenv`                   |
| Randomization      | Python `random` module            |
| Temporary Storage  | Python `tempfile` module          |

---

## 📂 Project Structure

```
kuku_fm_audio_prototype/
├── app.py            # Main Streamlit app
├── .env              # API key storage (GEMINI_API_KEY)
├── requirements.txt  # Dependencies
```

---

## ✅ How It Works

### 1. **User selects genres**
- Recommendations are filtered from a mock dataset.
- Optional surprise pick adds variety.

### 2. **Text-to-Speech conversion**
- Episode summaries and story content are turned into `.mp3` files.
- Files are stored temporarily and played in-browser.

### 3. **Story Generation Flow**
- AI generates the story in parts until the target word count is reached.
- Each part is appended to build a final coherent narrative.

### 4. **Audio Playback**
- The final story is synthesized to audio using `gTTS` and played for the user.

---

## 🔒 Environment Setup

1. Create a `.env` file:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 📦 `requirements.txt`
```
streamlit
gTTS
google-generativeai
python-dotenv
```

---

## 🎯 Future Enhancements

- 🧬 **Personalized Recommendations**: ML-powered content suggestions.
- 🌐 **Multilingual Support**: Add Hindi, Tamil, and more TTS options.
- ⏱️ **Custom Briefings**: Let users choose length or voice style.
- 📥 **Listen Later**: Save episodes to a personal playlist.
- 📤 **Social Sharing**: Share briefings via WhatsApp, Twitter, etc.
- 📈 **Trending Now**: Show hot and editor’s pick episodes.
- ⭐ **User Feedback**: Ratings and comments for each episode.
