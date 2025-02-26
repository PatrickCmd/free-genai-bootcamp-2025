import streamlit as st
import os
import json
from dotenv import load_dotenv
from llm import generate_vocabulary, check_api_status
from utils.helpers import extract_json_from_text, slugify
from data.schema import validate_words
from data.export import export_words, export_group, export_word_groups
from data.importer import import_words, import_groups, import_word_groups, get_preview_data
from api.client import check_api_connection, sync_words, sync_groups, sync_word_groups, get_all_groups, get_words_by_group
from feedback.store import store_feedback, get_feedback, get_feedback_stats, export_feedback
import uuid
from datetime import datetime

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

# Initialize session state for feedback
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False
if 'previous_generations' not in st.session_state:
    st.session_state.previous_generations = []

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
                                
                                # Add to previous generations
                                generation = {
                                    'timestamp': datetime.now().isoformat(),
                                    'theme': theme,
                                    'provider': llm_provider,
                                    'model': model,
                                    'words': [word.model_dump() for word in validated_words]
                                }
                                st.session_state.previous_generations.insert(0, generation)
                                # Keep only the last 5 generations
                                if len(st.session_state.previous_generations) > 5:
                                    st.session_state.previous_generations = st.session_state.previous_generations[:5]
                                
                                # Reset feedback submitted flag
                                st.session_state.feedback_submitted = False
                                
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
        if words_file:
            words_content = words_file.read().decode("utf-8")
            words_preview, words_count, words_error = get_preview_data(words_content, 'words')
            
            if words_error:
                st.error(f"Error parsing words file: {words_error}")
            else:
                st.success(f"Found {words_count} words in file")
    
    with col2:
        groups_file = st.file_uploader("Upload Groups JSON", type=["json"], key="groups_upload")
        if groups_file:
            groups_content = groups_file.read().decode("utf-8")
            groups_preview, groups_count, groups_error = get_preview_data(groups_content, 'groups')
            
            if groups_error:
                st.error(f"Error parsing groups file: {groups_error}")
            else:
                st.success(f"Found {groups_count} groups in file")
    
    with col3:
        associations_file = st.file_uploader("Upload Word-Group Associations JSON", type=["json"], key="associations_upload")
        if associations_file:
            associations_content = associations_file.read().decode("utf-8")
            associations_preview, associations_count, associations_error = get_preview_data(associations_content, 'word_groups')
            
            if associations_error:
                st.error(f"Error parsing associations file: {associations_error}")
            else:
                st.success(f"Found {associations_count} associations in file")
    
    # Preview section
    if words_file or groups_file or associations_file:
        st.subheader("Preview")
        
        preview_tabs = []
        if words_file:
            preview_tabs.append("Words")
        if groups_file:
            preview_tabs.append("Groups")
        if associations_file:
            preview_tabs.append("Associations")
        
        if preview_tabs:
            preview_tab = st.radio("Select preview", preview_tabs)
            
            if preview_tab == "Words" and words_file:
                st.write("Words Preview:")
                if words_preview:
                    st.dataframe(words_preview)
            
            if preview_tab == "Groups" and groups_file:
                st.write("Groups Preview:")
                if groups_preview:
                    st.dataframe(groups_preview)
            
            if preview_tab == "Associations" and associations_file:
                st.write("Associations Preview:")
                if associations_preview:
                    st.dataframe(associations_preview)
        
        # Import options
        st.subheader("Import Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            import_to_db = st.checkbox("Import to Local Database", value=True)
        
        with col2:
            sync_with_api = st.checkbox("Sync with Backend API", value=check_api_connection())
            if sync_with_api and not check_api_connection():
                st.warning("Backend API is not connected. Sync will be skipped.")
        
        if st.button("Import Data", type="primary"):
            import_results = []
            sync_results = []
            
            # Import to local database
            if import_to_db:
                if words_file:
                    imported_count, errors = import_words(words_content)
                    if errors:
                        import_results.append(f"⚠️ Imported {imported_count} words with errors: {errors}")
                    else:
                        import_results.append(f"✅ Successfully imported {imported_count} words")
                
                if groups_file:
                    imported_count, errors = import_groups(groups_content)
                    if errors:
                        import_results.append(f"⚠️ Imported {imported_count} groups with errors: {errors}")
                    else:
                        import_results.append(f"✅ Successfully imported {imported_count} groups")
                
                if associations_file:
                    imported_count, errors = import_word_groups(associations_content)
                    if errors:
                        import_results.append(f"⚠️ Imported {imported_count} associations with errors: {errors}")
                    else:
                        import_results.append(f"✅ Successfully imported {imported_count} associations")
            
            # Sync with backend API
            if sync_with_api and check_api_connection():
                if words_file:
                    success, message = sync_words(json.loads(words_content))
                    if success:
                        sync_results.append(f"✅ {message}")
                    else:
                        sync_results.append(f"❌ {message}")
                
                if groups_file:
                    success, message = sync_groups(json.loads(groups_content))
                    if success:
                        sync_results.append(f"✅ {message}")
                    else:
                        sync_results.append(f"❌ {message}")
                
                if associations_file:
                    success, message = sync_word_groups(json.loads(associations_content))
                    if success:
                        sync_results.append(f"✅ {message}")
                    else:
                        sync_results.append(f"❌ {message}")
            
            # Display results
            if import_results:
                st.subheader("Import Results")
                for result in import_results:
                    st.write(result)
            
            if sync_results:
                st.subheader("Sync Results")
                for result in sync_results:
                    st.write(result)

with tab3:
    st.header("Feedback")
    
    # Tabs for feedback and statistics
    feedback_tab, stats_tab = st.tabs(["Submit Feedback", "Feedback Statistics"])
    
    with feedback_tab:
        st.subheader("Rate Generated Vocabulary")
        
        # Check if there are any generations to rate
        if not st.session_state.previous_generations:
            st.warning("No vocabulary has been generated yet. Generate vocabulary in the Generate tab first.")
        else:
            # Selection for which generation to rate
            generation_options = [f"{g['theme']} ({g['provider']} - {g['model']}, {g['timestamp'][:16].replace('T', ' ')})" for g in st.session_state.previous_generations]
            selected_generation_idx = st.selectbox(
                "Select Generation to Rate", 
                options=range(len(generation_options)),
                format_func=lambda i: generation_options[i]
            )
            
            selected_generation = st.session_state.previous_generations[selected_generation_idx]
            
            # Display selected generation
            st.write(f"Theme: {selected_generation['theme']}")
            st.write(f"Provider: {selected_generation['provider']}")
            st.write(f"Model: {selected_generation['model']}")
            
            # Display a sample of the words
            st.write("Sample words:")
            sample_words = selected_generation['words'][:3]  # Show first 3 words
            for word in sample_words:
                st.write(f"- {word['jamaican_patois']} ({word['english']})")
            
            # Rating
            rating = st.slider("Rating (1-5)", min_value=1, max_value=5, value=3)
            
            # Comments
            comments = st.text_area("Comments (Optional)", placeholder="Enter any feedback or suggestions here...")
            
            # Submit button
            if st.button("Submit Feedback", type="primary"):
                if rating:
                    # Store feedback
                    feedback_id = store_feedback(
                        session_id=st.session_state.session_id,
                        theme=selected_generation['theme'],
                        provider=selected_generation['provider'],
                        model=selected_generation['model'],
                        rating=rating,
                        comments=comments
                    )
                    
                    st.session_state.feedback_submitted = True
                    st.success(f"Thank you for your feedback! (ID: {feedback_id})")
                else:
                    st.error("Please provide a rating before submitting.")
    
    with stats_tab:
        st.subheader("Feedback Statistics")
        
        # Get feedback statistics
        stats = get_feedback_stats()
        
        if stats['avg_rating'] == 0:
            st.info("No feedback has been submitted yet.")
        else:
            # Overall statistics
            st.write(f"Average Rating: {stats['avg_rating']:.2f}/5.0")
            
            # Rating distribution
            st.write("Rating Distribution:")
            rating_data = []
            for i in range(1, 6):
                rating_data.append({
                    'Rating': str(i),
                    'Count': stats['rating_distribution'].get(i, 0)
                })
            
            st.bar_chart(
                data=rating_data,
                x='Rating',
                y='Count'
            )
            
            # Provider statistics
            st.write("Provider Performance:")
            provider_data = []
            for provider, data in stats['provider_stats'].items():
                provider_data.append({
                    'Provider': provider,
                    'Average Rating': data['avg_rating'],
                    'Count': data['count']
                })
            
            st.dataframe(provider_data)
            
            # Model statistics
            st.write("Model Performance:")
            model_data = []
            for model, data in stats['model_stats'].items():
                model_data.append({
                    'Model': model,
                    'Average Rating': data['avg_rating'],
                    'Count': data['count']
                })
            
            st.dataframe(model_data)
            
            # Theme statistics
            st.write("Popular Themes:")
            theme_data = []
            for theme, data in stats['theme_stats'].items():
                theme_data.append({
                    'Theme': theme,
                    'Average Rating': data['avg_rating'],
                    'Count': data['count']
                })
            
            st.dataframe(theme_data)
            
            # Export feedback
            if st.button("Export Feedback Data"):
                filepath = export_feedback()
                with open(filepath, 'r') as f:
                    feedback_json = f.read()
                st.download_button(
                    "Download Feedback JSON",
                    data=feedback_json,
                    file_name=os.path.basename(filepath),
                    mime="application/json"
                )
                st.success(f"Feedback exported to {filepath}")

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

    st.subheader("Backend API Status")
    api_connected = check_api_connection()
    if api_connected:
        st.success("Backend API: Connected")
    else:
        st.error("Backend API: Not connected") 