# Vocabulary Importer Tool

A Streamlit-based tool for generating Jamaican Patois vocabulary using various LLM providers, exporting to JSON, and importing into the language learning application.

## Setup Instructions

### Environment Setup

1. Create a virtual environment:
```bash
# Navigate to the vocab-importer directory
cd vocab-importer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
# Install required packages
pip install streamlit python-dotenv pandas
pip install openai anthropic groq boto3
```

3. Configure API keys:
Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GROQ_API_KEY=your_groq_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

### Running the Application

```bash
streamlit run app.py
```

## Features

- Generate Jamaican Patois vocabulary based on themes/categories
- Choose from multiple LLM providers (OpenAI, Anthropic, Groq, AWS Bedrock)
- Export vocabulary to JSON format
- Import JSON files into the language learning application
- Provide feedback on generated vocabulary

## Project Structure

```
vocab-importer/
├── app.py                 # Main entry point
├── requirements.txt       # Dependencies
├── .env                   # API keys (gitignored)
├── .gitignore
├── README.md
├── llm/                   # LLM integration modules
│   ├── __init__.py
│   ├── openai.py
│   ├── anthropic.py
│   ├── groq.py
│   └── bedrock.py
├── data/                  # Data handling modules
│   ├── __init__.py
│   ├── schema.py          # Data validation
│   ├── export.py          # Export functionality
│   └── import.py          # Import functionality
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── helpers.py
└── feedback/              # Feedback handling
    ├── __init__.py
    └── store.py
``` 