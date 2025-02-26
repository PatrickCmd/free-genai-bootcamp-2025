import streamlit as st
import os
import json
from dotenv import load_dotenv
from llm import generate_vocabulary, check_api_status
from utils.helpers import extract_json_from_text, slugify
from data.schema import validate_words
from data.export import export_words, export_group, export_word_groups

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Vocabulary Importer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing generated vocabulary
if 'generated_words' not in st.session_state:
    st.session_state.generated_words = []
if 'theme' not in st.session_state:
    st.session_state.theme = ""
if 'provider' not in st.session_state:
    st.session_state.provider = ""
if 'model' not in st.session_state:
    st.session_state.model = ""

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
                options=["claude-3-5-sonnet-20240620", "claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-7-sonnet-latest"],
                index=1
            )
        elif llm_provider == "Groq":
            model = st.selectbox(
                "Model",
                options=["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "qwen-2.5-32b"],
                index=0
            )
        elif llm_provider == "AWS Bedrock":
            # Try to get accessible models
            try:
                from llm.bedrock import test_model_access, get_client, FALLBACK_MODELS
                
                client = get_client()
                
                # Test models to see which ones are accessible
                accessible_models = ["amazon.nova-micro-v1:0"]
                
                # Test Claude models
                claude_models = [
                    "anthropic.claude-3-5-haiku-20241022-v1:0",
                    "anthropic.claude-3-haiku-20240307-v1:0",
                    "anthropic.claude-3-sonnet-20240229-v1:0"
                ]
                
                for model_id in claude_models:
                    if test_model_access(client, model_id):
                        accessible_models.append(model_id)
                
                # Add fallback models
                for model_id in FALLBACK_MODELS:
                    if test_model_access(client, model_id):
                        accessible_models.append(model_id)
                
                model = st.selectbox(
                    "Model",
                    options=accessible_models,
                    index=0
                )
            except Exception:
                # Fallback to default options if there's an error
                model = st.selectbox(
                    "Model",
                    options=["amazon.nova-micro-v1:0"],
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
                try:
                    # Call the LLM to generate vocabulary
                    response = generate_vocabulary(
                        theme=theme,
                        count=word_count,
                        provider=llm_provider,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    # Extract JSON from the response
                    try:
                        json_data = extract_json_from_text(response)
                        
                        # Handle different response formats
                        if isinstance(json_data, dict) and "words" in json_data:
                            words = json_data["words"]
                        elif isinstance(json_data, dict) and "items" in json_data:
                            words = json_data["items"]
                        elif isinstance(json_data, list):
                            words = json_data
                        else:
                            # If we can't find a valid structure, show the raw response
                            st.error("Unexpected response format. Please try again.")
                            st.text_area("Raw Response", response, height=200)
                            words = []
                        
                        # Only proceed with validation if we have words
                        if words:
                            # Validate the words
                            try:
                                validated_words = validate_words(words)
                                
                                # Store in session state
                                st.session_state.generated_words = [word.model_dump() for word in validated_words]
                                st.session_state.theme = theme
                                st.session_state.provider = llm_provider
                                st.session_state.model = model
                                
                                st.success(f"Successfully generated {len(validated_words)} vocabulary items!")
                            except Exception as e:
                                st.error(f"Validation error: {str(e)}")
                                st.text_area("Raw Data", json.dumps(words, indent=2), height=200)
                    
                    except Exception as e:
                        st.error(f"Error processing response: {str(e)}")
                        st.text_area("Raw Response", response, height=200)
                
                except Exception as e:
                    st.error(f"Error generating vocabulary: {str(e)}")
    
    # Display generated vocabulary
    if st.session_state.generated_words:
        st.subheader("Generated Vocabulary")
        st.write(f"Theme: {st.session_state.theme}")
        st.write(f"Generated using: {st.session_state.provider} - {st.session_state.model}")
        
        # Display in a table
        words_df = []
        for word in st.session_state.generated_words:
            usage = word.get('parts', {}).get('usage', '')
            words_df.append({
                "Jamaican Patois": word.get('jamaican_patois', ''),
                "English": word.get('english', ''),
                "Type": word.get('parts', {}).get('type', ''),
                "Usage Notes": usage if usage else ''
            })
        
        st.dataframe(words_df, use_container_width=True)
        
        # Add collapsible raw JSON view
        with st.expander("View Raw JSON"):
            st.json(st.session_state.generated_words)
        
        # Export options
        st.subheader("Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Words"):
                try:
                    # Ensure all words have the required fields
                    for word in st.session_state.generated_words:
                        if 'id' not in word:
                            word['id'] = None
                    
                    filepath = export_words(
                        st.session_state.generated_words, 
                        theme=st.session_state.theme
                    )
                    with open(filepath, 'r') as f:
                        words_json = f.read()
                    st.download_button(
                        "Download Words JSON",
                        data=words_json,
                        file_name=os.path.basename(filepath),
                        mime="application/json"
                    )
                    st.success(f"Words exported to {filepath}")
                except Exception as e:
                    st.error(f"Error exporting words: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
        
        with col2:
            if st.button("Export Group"):
                try:
                    filepath = export_group(st.session_state.theme)
                    with open(filepath, 'r') as f:
                        group_json = f.read()
                    st.download_button(
                        "Download Group JSON",
                        data=group_json,
                        file_name=os.path.basename(filepath),
                        mime="application/json"
                    )
                    st.success(f"Group exported to {filepath}")
                except Exception as e:
                    st.error(f"Error exporting group: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
        
        with col3:
            if st.button("Export All"):
                try:
                    # Export words
                    # Ensure all words have the required fields
                    for word in st.session_state.generated_words:
                        if 'id' not in word:
                            word['id'] = None
                    
                    words_filepath = export_words(
                        st.session_state.generated_words,
                        theme=st.session_state.theme
                    )
                    
                    # Export group
                    group_filepath = export_group(st.session_state.theme)
                    
                    # Read the exported files to get IDs
                    with open(words_filepath, 'r') as f:
                        words_data = json.load(f)
                    with open(group_filepath, 'r') as f:
                        group_data = json.load(f)
                    
                    # Extract IDs
                    word_ids = [word.get('id') for word in words_data if word.get('id') is not None]
                    group_id = group_data[0].get('id', 1) if group_data and len(group_data) > 0 else 1
                    
                    # Export word-group associations
                    associations_filepath = export_word_groups(
                        word_ids, 
                        group_id,
                        theme=st.session_state.theme
                    )
                    
                    # Create a zip file with all exports
                    import zipfile
                    from datetime import datetime
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    theme_slug = slugify(st.session_state.theme) if st.session_state.theme else "export"
                    zip_filepath = f"exports/{theme_slug}_{timestamp}.zip"
                    
                    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                        zipf.write(words_filepath, os.path.basename(words_filepath))
                        zipf.write(group_filepath, os.path.basename(group_filepath))
                        zipf.write(associations_filepath, os.path.basename(associations_filepath))
                    
                    # Provide download button for the zip file
                    with open(zip_filepath, 'rb') as f:
                        zip_data = f.read()
                    
                    st.download_button(
                        "Download All (ZIP)",
                        data=zip_data,
                        file_name=os.path.basename(zip_filepath),
                        mime="application/zip"
                    )
                    
                    st.success(f"All data exported to {zip_filepath}")
                except Exception as e:
                    st.error(f"Error exporting data: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())

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