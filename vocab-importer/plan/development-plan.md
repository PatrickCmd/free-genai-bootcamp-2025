# Development Plan: Vocabulary Importer

This document outlines a step-by-step plan for implementing the Vocabulary Importer tool based on the technical specifications.

## Phase 1: Environment Setup and Project Initialization

### Week 1: Setup and Basic Structure

#### Day 1-2: Environment Configuration
- [x] Set up Python virtual environment
- [x] Install Streamlit and basic dependencies
- [x] Configure API credentials for LLM providers
  - Create `.env` file for API keys
  - Set up environment variable loading
- [x] Initialize Git repository with `.gitignore` for sensitive files

#### Day 3-4: Basic Streamlit Application Structure
- [x] Create main application entry point (`app.py`)
- [x] Implement basic UI layout with placeholder sections:
  - Input section (theme entry, provider selection)
  - Results display area
  - Export/import controls
- [x] Set up basic navigation/tabs for different functionality
- [x] Test Streamlit server and hot reloading

#### Day 5: Project Organization
- [x] Create modular folder structure:
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
- [x] Create placeholder files and implement basic imports

## Phase 2: LLM Integration and Core Generation Logic

### Week 2: LLM Provider Integration

#### Day 1-2: OpenAI Integration
- [x] Implement OpenAI API client in `llm/openai.py`
- [x] Create model selection dropdown that populates based on provider
- [x] Implement temperature and other parameter controls
- [x] Test basic prompt delivery and response handling

#### Day 3-4: Additional LLM Providers
- [x] Implement Anthropic/Claude integration
- [x] Implement Groq integration
- [x] Implement AWS Bedrock integration
- [x] Create a unified interface for provider selection

#### Day 5: Prompt Engineering and Testing
- [x] Refine the prompt template for vocabulary generation
- [x] Implement prompt formatting with user inputs
- [x] Test across different providers and models
- [x] Create response handling for different provider formats

### Week 3: Data Handling and Processing

#### Day 1-2: Response Processing
- [x] Implement JSON extraction from LLM responses
- [x] Create validation for vocabulary item schema
- [x] Build processing pipeline for raw LLM output
- [x] Handle error cases and malformed responses

#### Day 3-4: Data Structure Implementation
- [x] Implement Words schema and validation
- [x] Implement Groups schema and validation
- [x] Implement Word-Group Associations logic
- [x] Create ID assignment for generated items

#### Day 5: Results Display
- [x] Design and implement tabular display of generated vocabulary
- [x] Add editing capabilities for user refinement
- [x] Implement sorting and filtering options
- [x] Create preview functionality

## Phase 3: Export/Import and Feedback Features

### Week 4: Export and Import Functionality

#### Day 1-2: Export Implementation
- [x] Create JSON export functionality for vocabulary items
- [x] Implement separate exports for words, groups, and associations
- [x] Add combined export option
- [x] Implement file naming and organization

#### Day 3-4: Import Implementation
- [x] Create file upload interface
- [x] Implement JSON parsing and validation
- [x] Build preview functionality for imported data
- [x] Handle validation errors and feedback

#### Day 5: Backend API Integration
- [x] Implement connection to language portal API
- [x] Create authentication mechanism
- [x] Build import-to-database functionality
- [x] Test end-to-end workflow

### Week 5: Feedback System and Refinement

#### Day 1-2: Feedback Collection
- [ ] Implement rating interface (1-5 stars)
- [ ] Create comment submission form
- [ ] Design feedback data storage
- [ ] Implement feedback submission

#### Day 3-4: Data Storage and Persistence
- [ ] Implement local storage for generated vocabulary
- [ ] Create session management for ongoing work
- [ ] Implement caching for LLM responses
- [ ] Build export history

#### Day 5: Performance Optimization
- [ ] Implement batch processing for large datasets
- [ ] Add progress indicators for long-running operations
- [ ] Optimize LLM request parameters
- [ ] Implement timeout handling and retries

## Phase 4: Testing, Documentation, and Deployment

### Week 6: Testing and Refinement

#### Day 1-2: Unit and Integration Testing
- [ ] Write tests for JSON processing functions
- [ ] Test LLM API integrations
- [ ] Implement error handling tests
- [ ] Create validation test suite

#### Day 3-4: User Acceptance Testing
- [ ] Conduct testing with language experts
- [ ] Gather feedback on vocabulary quality
- [ ] Test with various themes and categories
- [ ] Refine prompts based on output quality

#### Day 5: Final Refinements
- [ ] Address issues identified during testing
- [ ] Implement UI/UX improvements
- [ ] Optimize performance bottlenecks
- [ ] Ensure all error cases are handled

### Week 7: Documentation and Deployment

#### Day 1-2: User Documentation
- [ ] Create user guide with screenshots
- [ ] Document available LLM options
- [ ] Write export/import instructions
- [ ] Document feedback system

#### Day 3-4: Technical Documentation
- [ ] Document code structure and architecture
- [ ] Create API integration documentation
- [ ] Document environment setup process
- [ ] Create contribution guidelines

#### Day 5: Deployment
- [ ] Package application for distribution
- [ ] Create deployment instructions
- [ ] Test deployment in target environment
- [ ] Prepare handover documentation

## Next Steps and Future Enhancements

- Implement additional LLM providers as they become available
- Add more sophisticated prompt templates for different vocabulary types
- Enhance the UI with visualization of word relationships
- Implement automatic quality assessment of generated vocabulary
- Add support for bulk operations and batch processing
- Create a vocabulary recommendation system based on feedback 