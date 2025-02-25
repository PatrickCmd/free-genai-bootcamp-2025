import streamlit as st
import os
from dotenv import load_dotenv
from llm import check_api_status

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Vocabulary Importer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title
st.title("Jamaican Patois Vocabulary Importer")
st.markdown("Generate, export, and import Jamaican Patois vocabulary for the language learning application.")

# Create tabs for different functionality
tab1, tab2, tab3 = st.tabs(["Generate", "Import", "Feedback"])

with tab1:
    st.header("Generate Vocabulary")
    
    # Input section
    st.subheader("Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.text_input("Theme/Category", placeholder="e.g., Food, Travel, Greetings")
        word_count = st.slider("Number of words to generate", min_value=5, max_value=50, value=10)
    
    with col2:
        llm_provider = st.selectbox(
            "LLM Provider",
            options=["OpenAI", "Anthropic", "Groq", "AWS Bedrock"],
            index=0
        )
        
        # Dynamic model selection based on provider
        if llm_provider == "OpenAI":
            model = st.selectbox(
                "Model",
                options=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
                index=0
            )
        elif llm_provider == "Anthropic":
            model = st.selectbox(
                "Model",
                options=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                index=1
            )
        elif llm_provider == "Groq":
            model = st.selectbox(
                "Model",
                options=["llama-3-70b", "llama-3-8b", "mixtral-8x7b"],
                index=0
            )
        elif llm_provider == "AWS Bedrock":
            model = st.selectbox(
                "Model",
                options=["anthropic.claude-3-sonnet", "anthropic.claude-3-haiku", "cohere.command", "amazon.titan"],
                index=0
            )
    
    # Advanced parameters
    with st.expander("Advanced Parameters"):
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        max_tokens = st.slider("Max Tokens", min_value=100, max_value=4000, value=2000, step=100)
    
    # Generate button
    if st.button("Generate Vocabulary", type="primary"):
        if not theme:
            st.error("Please enter a theme/category")
        else:
            with st.spinner(f"Generating {word_count} vocabulary items using {llm_provider}..."):
                # Placeholder for actual generation
                st.info("This is a placeholder. Actual LLM integration will be implemented in the next phase.")
                
                # Placeholder data
                placeholder_data = [
                    {
                        "jamaican_patois": "Nyam",
                        "english": "Eat",
                        "parts": {
                            "type": "verb"
                        }
                    },
                    {
                        "jamaican_patois": "Wah Gwaan",
                        "english": "Hello/What's happening",
                        "parts": {
                            "type": "phrase"
                        }
                    }
                ]
                
                st.subheader("Generated Vocabulary")
                st.json(placeholder_data)
                
                # Export options
                st.subheader("Export Options")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "Export Words",
                        data="{}",
                        file_name="words.json",
                        mime="application/json"
                    )
                with col2:
                    st.download_button(
                        "Export Group",
                        data="{}",
                        file_name="group.json",
                        mime="application/json"
                    )
                with col3:
                    st.download_button(
                        "Export Associations",
                        data="{}",
                        file_name="word_groups.json",
                        mime="application/json"
                    )

with tab2:
    st.header("Import Vocabulary")
    
    # File upload section
    st.subheader("Upload JSON Files")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        words_file = st.file_uploader("Upload Words JSON", type=["json"], key="words_upload")
    
    with col2:
        groups_file = st.file_uploader("Upload Groups JSON", type=["json"], key="groups_upload")
    
    with col3:
        associations_file = st.file_uploader("Upload Word-Group Associations JSON", type=["json"], key="associations_upload")
    
    # Preview and import buttons
    if words_file or groups_file or associations_file:
        st.subheader("Preview")
        
        if words_file:
            st.write("Words Preview:")
            st.info("Preview functionality will be implemented in a later phase")
        
        if groups_file:
            st.write("Groups Preview:")
            st.info("Preview functionality will be implemented in a later phase")
        
        if associations_file:
            st.write("Associations Preview:")
            st.info("Preview functionality will be implemented in a later phase")
        
        if st.button("Import to Database", type="primary"):
            st.success("Import functionality will be implemented in a later phase")

with tab3:
    st.header("Feedback")
    
    # Feedback form
    st.subheader("Rate Generated Vocabulary")
    
    # Selection for which generation to rate
    st.selectbox("Select Generation to Rate", options=["Current Session", "Previous Session 1", "Previous Session 2"])
    
    # Rating
    rating = st.slider("Rating", min_value=1, max_value=5, value=3)
    
    # Comments
    comments = st.text_area("Comments (Optional)", placeholder="Enter any feedback or suggestions here...")
    
    # Submit button
    if st.button("Submit Feedback", type="primary"):
        if rating:
            st.success("Thank you for your feedback! This will help improve future generations.")
        else:
            st.error("Please provide a rating before submitting.")

# Sidebar with information
with st.sidebar:
    st.header("Information")
    st.info(
        "This tool allows you to generate Jamaican Patois vocabulary using various LLM providers, "
        "export the generated vocabulary to JSON format, and import it into the language learning application."
    )
    
    st.subheader("Instructions")
    st.markdown(
        """
        1. **Generate Tab**: Enter a theme/category and select an LLM provider to generate vocabulary.
        2. **Import Tab**: Upload JSON files to import into the database.
        3. **Feedback Tab**: Provide feedback on generated vocabulary.
        """
    )
    
    st.subheader("API Status")
    
    # Check environment variables for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Display API status based on environment variables
    if openai_key:
        st.success("OpenAI API: Configured")
    else:
        st.error("OpenAI API: Not configured")
        
    if anthropic_key:
        st.success("Anthropic API: Configured")
    else:
        st.error("Anthropic API: Not configured")
        
    if groq_key:
        st.success("Groq API: Configured")
    else:
        st.error("Groq API: Not configured")
        
    if aws_access_key and aws_secret_key:
        st.success("AWS Bedrock: Configured")
    else:
        st.error("AWS Bedrock: Not configured") 