import streamlit as st
from gtts import gTTS
import random
import tempfile
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configure the generative AI with the API key
genai.configure(api_key=GEMINI_API_KEY)

# Expanded mock content data (simulating Kuku FM's audio content)
content_data = [
    {"title": "Episode 1: Mystery Unveiled", "genre": "Thriller", "summary": "A thrilling tale of secrets and suspense."},
    {"title": "Episode 2: Suspenseful Journey", "genre": "Thriller", "summary": "Join the adventure filled with unexpected twists."},
    {"title": "Episode 3: Laugh Out Loud", "genre": "Comedy", "summary": "Get ready to laugh with this hilarious podcast."},
    {"title": "Episode 4: Hilarious Adventures", "genre": "Comedy", "summary": "Embark on a journey of fun and laughter."},
    {"title": "Episode 5: Emotional Rollercoaster", "genre": "Drama", "summary": "Experience a story that tugs at your heartstrings."},
    {"title": "Episode 6: Heartfelt Stories", "genre": "Drama", "summary": "Dive into narratives that resonate deeply."},
    {"title": "Episode 7: Love in the Air", "genre": "Romance", "summary": "A heartwarming story of love and connection."},
    {"title": "Episode 8: Romantic Getaway", "genre": "Romance", "summary": "Escape into a world of romance and passion."},
    {"title": "Episode 9: Thrilling Chase", "genre": "Thriller", "summary": "A high-stakes pursuit that will keep you on the edge."},
    {"title": "Episode 10: Comedy Night", "genre": "Comedy", "summary": "An evening of stand-up comedy to brighten your day."},
    {"title": "Episode 11: Dramatic Finale", "genre": "Drama", "summary": "The conclusion to an epic saga."},
    {"title": "Episode 12: Romantic Encounters", "genre": "Romance", "summary": "Tales of love that will make your heart flutter."},
    {"title": "Episode 13: The Unexpected Turn", "genre": "Thriller", "summary": "A story where nothing is as it seems."},
    {"title": "Episode 14: Jokes Galore", "genre": "Comedy", "summary": "A collection of jokes to keep you smiling."},
    {"title": "Episode 15: Tears and Triumphs", "genre": "Drama", "summary": "A journey through life's ups and downs."},
    {"title": "Episode 16: Love Letters", "genre": "Romance", "summary": "Intimate stories told through letters."},
]

# Function to generate audio using Google Text-to-Speech (gTTS)
def text_to_speech(text):
    """Convert text to an audio file using gTTS and return the file path."""
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        return tmpfile.name

# Function to start a chat with the Gemini model
def start_llm_chat(history=None):
    """Start a new chat session with the Gemini model."""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    chat = model.start_chat(history=history if history else [])
    return chat

# Function to send a message to the Gemini model
def send_llm_message(chat, prompt):
    """Send a message to the LLM and get the response stream."""
    response = chat.send_message(prompt, stream=True)
    return response

# Streamlit app layout and logic
st.title("Kuku FM Daily Audio Briefing Prototype")

# Sidebar: New features simulating future additions
st.sidebar.header("Settings")
language = st.sidebar.selectbox("Preferred Language", ["English", "Hindi-Feature adding soon", "Other-Feature adding soon"])
st.sidebar.write("More settings coming soon (e.g., briefing length, voice style).")

st.sidebar.header("Past Briefings")
st.sidebar.write("2023-10-01")
st.sidebar.write("2023-09-30")
st.sidebar.write("Click to view past briefings (feature coming soon).")

st.sidebar.header("Feedback")
feedback = st.sidebar.text_area("Leave your feedback here")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.write("Thank you for your feedback!")

# Main app: User inputs for briefing
genres = list(set(item['genre'] for item in content_data))  # Dynamic genres from content
selected_genres = st.multiselect("Select your favorite genres:", genres)
include_surprise = st.checkbox("Include a surprise recommendation from any genre")

# Button to trigger the briefing generation
if st.button("Generate My Briefing"):
    if selected_genres or include_surprise:
        # Filter content based on selected genres
        filtered_content = [item for item in content_data if item["genre"] in selected_genres]
        
        recommendations = []
        if filtered_content:
            recommendations = random.sample(filtered_content, min(3, len(filtered_content)))
        
        if include_surprise:
            surprise_rec = random.choice(content_data)
            while surprise_rec in recommendations:  # Avoid duplicates
                surprise_rec = random.choice(content_data)
            recommendations.append(surprise_rec)
        
        if recommendations:
            # Generate individual audio files for each summary
            audio_files = {}
            for rec in recommendations:
                summary_text = f"{rec['title']}: {rec['summary']}"
                audio_files[rec['title']] = text_to_speech(summary_text)
            
            # Generate full briefing text
            briefing_text = "Welcome to your daily audio briefing. Today, we recommend the following episodes: "
            for i, rec in enumerate(recommendations, 1):
                if include_surprise and rec == recommendations[-1]:
                    briefing_text += f"And here's a surprise recommendation: {rec['title']}: {rec['summary']} "
                else:
                    briefing_text += f"{i}. {rec['title']}: {rec['summary']} "
            briefing_text += "Enjoy your listening!"
            
            # Generate and display full briefing audio
            full_audio_file = text_to_speech(briefing_text)
            st.write("### Your Daily Briefing")
            st.audio(full_audio_file)
            
            # Display recommendations with emojis and interactive buttons
            st.write("### Your Recommendations:")
            genre_emojis = {
                "Thriller": "🔪",
                "Comedy": "😂",
                "Drama": "🎭",
                "Romance": "💖",
            }
            for i, rec in enumerate(recommendations):
                emoji = genre_emojis.get(rec['genre'], "🎙️")
                title_display = f"{emoji} **{rec['title']}**"
                if include_surprise and i == len(recommendations) - 1:
                    title_display += " (Surprise Pick)"
                st.write(title_display)
                st.write(rec['summary'])
                if st.button(f"Play Summary", key=f"play_{rec['title']}"):
                    st.audio(audio_files[rec['title']])
                if st.button(f"Play Full Episode", key=f"full_{rec['title']}"):
                    st.write(f"Simulating playback of {rec['title']}")
        else:
            st.write("No content available for selected options.")
    else:
        st.write("Please select at least one genre or check 'Include a surprise recommendation'.")

# New section: Generate Your Own Story
with st.expander("Generate Your Own Story"):
    st.write("Enter keywords to generate a custom story or click 'Get Random Keywords' for inspiration.")
    
    # List of words for random keyword generation
    word_list = [
        "adventure", "mystery", "love", "comedy", "drama", "thriller", "romance", "journey", "secrets", "laughter",
        "heartwarming", "suspense", "twists", "fun", "emotional", "stories", "connection", "passion", "chase", "stand-up",
        "finale", "encounters", "unexpected", "jokes", "triumphs", "letters"
    ]
    
    # Button to generate random keywords
    if st.button("Get Random Keywords"):
        random_keywords = random.sample(word_list, 3)
        st.session_state.keywords_input = ", ".join(random_keywords)
    
    # Input field for keywords
    keywords_input = st.text_input("Keywords (comma-separated, up to 3):", key="keywords_input")
    
    # Button to generate the story
    if st.button("Generate Story"):
        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
            if 1 <= len(keywords) <= 3:
                with st.spinner("Generating your story... This may take a few minutes."):
                    status_text = st.empty()
                    status_text.write("Starting story generation...")

                    chat = start_llm_chat()
                    story_parts = []
                    current_word_count = 0
                    target_word_count = 2500

                    # Initial prompt
                    initial_prompt = f"Create the beginning of a detailed, engaging story that includes the following keywords: {', '.join(keywords)}. Aim for about 500 words and ensure the story is suitable for audio narration."
                    response = send_llm_message(chat, initial_prompt)
                    part = ""
                    for chunk in response:
                        part += chunk.text
                    story_parts.append(part)
                    current_word_count += len(part.split())
                    status_text.write(f"Generated initial part: {current_word_count} words")

                    # Continue generating parts until close to target
                    while current_word_count < (target_word_count - 500):
                        continue_prompt = "Continue the story from where you left off, adding another 500 words. Keep it engaging, coherent, and aligned with the keywords."
                        response = send_llm_message(chat, continue_prompt)
                        part = ""
                        for chunk in response:
                            part += chunk.text
                        story_parts.append(part)
                        current_word_count += len(part.split())
                        status_text.write(f"Generated {len(story_parts)} parts: {current_word_count} words")

                    # Final part to conclude the story
                    final_prompt = f"Conclude the story from where you left off, ensuring it wraps up completely and includes the keywords {', '.join(keywords)}. Add enough content to reach a total of at least 2500 words when combined with previous parts (current word count is {current_word_count})."
                    response = send_llm_message(chat, final_prompt)
                    part = ""
                    for chunk in response:
                        part += chunk.text
                    story_parts.append(part)
                    current_word_count += len(part.split())
                    status_text.write(f"Story completed with {len(story_parts)} parts: {current_word_count} words")

                    full_story = " ".join(story_parts)
                    st.session_state['story'] = full_story
                    status_text.write("Story generation complete!")
                    st.write("### Your Custom Story")
                    st.write(full_story)
            else:
                st.write("Please enter 1 to 3 keywords.")
        else:
            st.write("Please enter some keywords.")
    
    # Button to listen to the story
    if 'story' in st.session_state:
        if st.button("Listen to Story"):
            st.write("Note: The story is at least 2500 words long, so the audio may take around 15-20 minutes to play.")
            with st.spinner("Generating audio for the story... This may take a while due to the story's length."):
                audio_file = text_to_speech(st.session_state['story'])
                st.audio(audio_file)

# Future additions section
st.write("""
---

### Future Additions for Kuku FM
This prototype can be enhanced to align with Kuku FM's goals of engaging users with personalized audio content. Here are potential improvements:

- **Real-Time Content Integration**: Connect to Kuku FM's library via an API to pull real podcasts, audiobooks, or episodes.
- **Advanced Personalization**: Use machine learning to recommend content based on listening history, preferences, or trending episodes.
- **Multilingual Support**: Offer briefings in multiple languages (e.g., Hindi, Tamil) using gTTS or other TTS engines.
- **Customizable Briefings**: Allow users to set briefing duration (short, medium, long) or choose specific narrators.
- **Listen Later Playlist**: Add a feature to save recommended episodes for future listening.
- **Social Sharing**: Enable users to share briefings or episodes via social media or messaging apps.
- **Interactive Feedback**: Collect ratings or comments on briefings to refine recommendations.
- **Trending Section**: Highlight popular or editor-picked episodes alongside personalized recommendations.
""")