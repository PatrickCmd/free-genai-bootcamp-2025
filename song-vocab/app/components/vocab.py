import streamlit as st

def render_vocabulary_list(vocab_items):
    """Render the vocabulary list component"""
    st.subheader("Vocabulary")
    
    if not vocab_items:
        st.info("No vocabulary items found.")
        return
    
    for item in vocab_items:
        with st.expander(f"📚 {item.word}"):
            st.write(f"**Explanation:** {item.explanation}")
            st.write("**Example Sentences:**")
            for sentence in item.example_sentences:
                st.write(f"- {sentence}")
