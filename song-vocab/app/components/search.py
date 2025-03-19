# song-vocab/app/components/search.py
import streamlit as st

def render_search_form():
    """Render the search form component"""
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            song_title = st.text_input("Song Title", placeholder="Enter song title...")
        
        with col2:
            user_language = st.selectbox(
                "Your Language",
                options=["English", "Spanish", "French", "German"],
                index=0
            )
        
        with col3:
            foreign_language = st.selectbox(
                "Song Language",
                options=["Jamaican Patois", "Spanish", "French", "German", "Japanese"],
                index=0
            )
        
        search_button = st.form_submit_button("Search Song")
        
    return {
        "song_title": song_title,
        "user_language": user_language,
        "foreign_language": foreign_language,
        "search_clicked": search_button
    }