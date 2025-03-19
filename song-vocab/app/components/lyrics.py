# song-vocab/app/components/lyrics.py
import streamlit as st

def render_lyrics(song_result):
    """Render the lyrics display component"""
    st.subheader("Song Details")
    st.write(f"**Title:** {song_result.title}")
    st.write(f"**Artist:** {song_result.artist}")
    st.write(f"**Album:** {song_result.album or 'N/A'}")
    st.write(f"**Language:** {song_result.language}")
    
    st.subheader("Lyrics")
    st.text_area("", value=song_result.lyrics, height=300, disabled=True)