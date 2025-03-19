import asyncio
import json
import os
import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path to access other modules
parent_dir = str(Path(__file__).parent.parent)
print(f"Parent directory: {parent_dir}")
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
# print(f"sys.path: {sys.path}")

# Fix imports with proper module paths
from agents.schemas import VocabularyRequest
from agents.vocab_gen import VocabularyGenerator
from agents.web_search import WebSearchAgent
from database.models import SongBase, VocabularyBase
from database import DatabaseStore, init_db

# Initialize database
init_db()
db = DatabaseStore()

# Initialize agents
web_search = WebSearchAgent()
vocab_gen = VocabularyGenerator()

def save_to_database(song_result, vocab_items):
    """Save song and vocabulary to database"""
    # Save song
    song_to_save = SongBase(
        title=song_result.title,
        lyrics=song_result.lyrics,
        language=song_result.language,
        artist=song_result.artist,
        album=song_result.album,
        release_date=song_result.release_date
    )
    song_id = db.add_song(song_to_save)
    
    # Save vocabulary items
    for item in vocab_items:
        # Create a VocabularyBase object (the model already has a validator to handle the list)
        vocab_to_save = VocabularyBase(
            song_id=song_id,
            word=item.word,
            explanation=item.explanation,
            example_sentences=item.example_sentences  # This will be converted to string by the validator
        )
        db.add_vocabulary(vocab_to_save)
    
    return song_id

def export_to_json(song_result, vocab_items, filename):
    """Export song and vocabulary to JSON file"""
    export_data = {
        "song": {
            "title": song_result.title,
            "lyrics": song_result.lyrics,
            "language": song_result.language,
            "artist": song_result.artist,
            "album": song_result.album,
            "release_date": song_result.release_date if song_result.release_date else None
        },
        "vocabulary": [
            {
                "word": item.word,
                "explanation": item.explanation,
                "example_sentences": item.example_sentences
            } for item in vocab_items
        ]
    }
    
    with open(f"data/json_exports/{filename}", 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return filename

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Song Vocabulary Builder",
        page_icon="🎵",
        layout="wide"
    )

    st.title("🎵 Song Vocabulary Builder")
    st.write("Learn vocabulary from your favorite songs in foreign languages!")
    
    # Create sidebar with instructions
    with st.sidebar:
        st.header("How to use")
        st.write("""
        1. Enter a song title
        2. Select your language 
        3. Select the song's language
        4. Click 'Search Song'
        5. Review lyrics and vocabulary
        6. Save to database or export as needed
        """)
        
        st.header("About")
        st.write("""
        This application helps language learners extract useful vocabulary 
        from songs in their target language. Powered by OpenAI agents and Streamlit.
        """)

    # Input form
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            song_title = st.text_input("Song Title", placeholder="Enter song title...")
        
        with col2:
            user_language = st.selectbox(
                "Your Language",
                options=["English", "Spanish", "French", "German", "Japanese", "Chinese", "Portuguese"],
                index=0
            )
        
        with col3:
            foreign_language = st.selectbox(
                "Song Language",
                options=["Jamaican Patois", "Spanish", "French", "German", "Japanese", "Portuguese", "Korean", "Italian"],
                index=0
            )
        
        num_words = st.slider("Number of vocabulary items", min_value=5, max_value=30, value=10)
        
        search_button = st.form_submit_button("Search Song", use_container_width=True)

    # Session state to store results
    if "song_result" not in st.session_state:
        st.session_state.song_result = None
        
    if "vocab_items" not in st.session_state:
        st.session_state.vocab_items = None

    # Process search when button is clicked
    if search_button and song_title:
        with st.spinner("📡 Searching for song..."):
            # Use asyncio to handle the async call
            song_result = asyncio.run(web_search.search_song(
                title=song_title,
                user_language=user_language,
                foreign_language=foreign_language
            ))
            
            if song_result:
                st.session_state.song_result = song_result
                
                # Display song details
                st.subheader("Song Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Title:** {song_result.title}")
                    st.write(f"**Artist:** {song_result.artist}")
                with col2:
                    st.write(f"**Album:** {song_result.album or 'N/A'}")
                    st.write(f"**Language:** {song_result.language}")
                
                # Display lyrics
                st.subheader("Lyrics")
                st.text_area("", value=song_result.lyrics, height=300, disabled=True)
                
                # Generate vocabulary
                with st.spinner("🔍 Generating vocabulary..."):
                    vocab_request = VocabularyRequest(
                        lyrics=song_result.lyrics,
                        source_language=foreign_language,
                        target_language=user_language,
                        num_words=num_words
                    )
                    vocab_items = asyncio.run(vocab_gen.generate_vocabulary(vocab_request))
                    st.session_state.vocab_items = vocab_items
                
                # Display vocabulary
                st.subheader("Vocabulary")
                for item in vocab_items:
                    with st.expander(f"📚 **{item.word}**"):
                        st.write(f"**Explanation:** {item.explanation}")
                        st.write("**Example Sentences:**")
                        for sentence in item.example_sentences:
                            st.write(f"- {sentence}")
                
                # Save/Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save to Database", use_container_width=True):
                        with st.spinner("Saving to database..."):
                            song_id = save_to_database(song_result, vocab_items)
                            st.success(f"Saved to database! Song ID: {song_id}")
                
                with col2:
                    # Export to JSON button
                    if st.button("📋 Export to JSON", use_container_width=True):
                        filename = f"{song_title.replace(' ', '_').lower()}_vocab.json"
                        filepath = export_to_json(song_result, vocab_items, filename)
                        
                        with open(filename, "r") as f:
                            json_data = f.read()
                        
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=filename,
                            mime="application/json",
                            use_container_width=True
                        )
                        st.success(f"JSON file created: {filename}")
            else:
                st.error("😕 Could not find the song. Please try a different title or language.")

    # Show previously loaded results if they exist
    elif st.session_state.song_result and st.session_state.vocab_items:
        song_result = st.session_state.song_result
        vocab_items = st.session_state.vocab_items
        
        # Display song details
        st.subheader("Song Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Title:** {song_result.title}")
            st.write(f"**Artist:** {song_result.artist}")
        with col2:
            st.write(f"**Album:** {song_result.album or 'N/A'}")
            st.write(f"**Language:** {song_result.language}")
        
        # Display lyrics
        st.subheader("Lyrics")
        st.text_area("", value=song_result.lyrics, height=300, disabled=True)
        
        # Display vocabulary
        st.subheader("Vocabulary")
        for item in vocab_items:
            with st.expander(f"📚 **{item.word}**"):
                st.write(f"**Explanation:** {item.explanation}")
                st.write("**Example Sentences:**")
                for sentence in item.example_sentences:
                    st.write(f"- {sentence}")
        
        # Save/Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save to Database", use_container_width=True):
                with st.spinner("Saving to database..."):
                    song_id = save_to_database(song_result, vocab_items)
                    st.success(f"Saved to database! Song ID: {song_id}")
        
        with col2:
            # Export to JSON button
            if st.button("📋 Export to JSON", use_container_width=True):
                filename = f"{song_result.title.replace(' ', '_').lower()}_vocab.json"
                filepath = export_to_json(song_result, vocab_items, filename)
                
                with open(f"data/json_exports/{filename}", "r") as f:
                    json_data = f.read()
                
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
                st.success(f"JSON file created: {filename}")

if __name__ == "__main__":
    main() 