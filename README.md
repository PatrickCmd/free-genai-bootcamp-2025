# GenAI Bootcamp 2025

GenAI Bootcamp 2025 is a series of weeks of learning Generative AI and prompts for learning Jamaican Patois. Guided by Andrew Brown from ExamPro Inc.
[GenAI Bootcamp 2025 YouTube Playlist](https://www.youtube.com/playlist?list=PLBfufR7vyJJ69c9MNlOKtO2w2KU5VzLJV)

## 1. Introduction
### 1.1. [Learn Jamaican Patois(Beginners) 20 Common questions and Answers - YouTube](https://www.youtube.com/watch?v=MGKIqxlkwPY)
### 1.2. [Jamaican Patois Language Guide - YouTube](https://www.youtube.com/watch?v=r9zOthNkVPU&list=PL4Jw2ofjp-ikoH31FAO2P_ZiuB_pdfE1j)

## 2. Sentence Constructor

### 2.1. [Sentence Constructor Journal](sentence-constructor/README.md)
### 2.2. [Sentence Constructor Prompt](sentence-constructor/chatgpt/prompt.md)
### 2.3. [Sentence Constructor Hypothesis](sentence-constructor/hypothesis/hypothesis.md)
### 2.4. [Sentence Constructor Technical](sentence-constructor/hypothesis/technical.md)

# Learning Journal

## 1. GenAI Architecting
*Reference: [genai-architecting](./genai-architecting/README.md)*

Exploring foundational concepts of GenAI architecture including:
- Conceptual architectures for GenAI applications
- RAG (Retrieval Augmented Generation) implementation patterns
- Prompt engineering techniques and best practices
- Effective knowledge retrieval systems design

This study laid the groundwork for later projects by establishing a solid understanding of GenAI conceptual models and architectural patterns. I explored how different components like vector databases, LLMs, and retrieval systems work together in production environments.

## 2. Sentence Constructor
*Reference: [sentence-constructor](./sentence-constructor/README.md)*

A focused project on prompt engineering for language learning:
- Created prompts for different LLMs (ChatGPT, Claude, Meta AI)
- Developed a hypothesis-driven approach to prompt engineering
- Implemented specialized prompts for Jamaican Patois sentence construction
- Compared performance across different models and prompt formats

This project helped me understand the nuances of prompt design and how different LLMs respond to similar instructions. The work with Jamaican Patois highlighted the importance of cultural context in language-oriented AI systems.

## 3. Lang Portal
*Reference: [lang-portal](./lang-portal/)*

A full-stack language learning platform with:
- Frontend web interface built with React and Tailwind CSS
- Backend API services for language learning content
- Integration with LLM services for dynamic content generation
- User experience focused on practical language acquisition

This project enhanced my understanding of how to build user-facing applications powered by GenAI, particularly focusing on the architectural separation between frontend and backend components in GenAI applications.

## 4. Vocab Importer
*Reference: [vocab-importer](./vocab-importer/README.md)*

An advanced vocabulary management system featuring:
- Automated vocabulary extraction from various sources
- LLM-powered definitions and example generation
- Export functionality for spaced repetition systems
- Data validation and structured knowledge representation

The Vocab Importer project demonstrated practical applications of GenAI for educational tooling, with particular emphasis on structured data processing and educational content generation.

## 5. OPEA Comps
*Reference: [opea-comps](./opea-comps/README.md)*

Exploration of the Open Enterprise AI (OPEA) architecture through several component implementations:

### 5.1. Megaservice
*Reference: [mega-service](./opea-comps/mega-service/README.md)*

- Orchestration layer for multiple AI capabilities
- Unified API for diverse AI services
- Request/response protocols for standardized communication
- Service composition patterns for complex AI workflows

### 5.2. ChatQnA
*Reference: [chatqna_opea](./opea-comps/chatqna_opea/README.md)*

- Terraform-based infrastructure provisioning on AWS
- Docker containerization for deployable AI services
- Integration with OpenAI models for conversation
- Enterprise-grade prompt templating techniques

### 5.3. DocSum
*Reference: [docsum_opea](./opea-comps/docsum_opea/README.md)*

- Document summarization pipeline implementation
- Infrastructure provisioning patterns matching ChatQnA
- Document processing workflows for knowledge extraction
- Output formatting for human readability

### 5.4. TTS Microservice
*Reference: [tts-microservice](./opea-comps/tts-microservice/README.md)*

- Speech synthesis capabilities using multiple models
- Audio generation service architecture
- REST API design for speech services
- AWS infrastructure optimization for audio processing
- Model comparison between SpeechT5 and GPTSoVITS

The OPEA components exploration provided hands-on experience with enterprise-grade AI service development, infrastructure provisioning, and containerization strategies. This work highlighted the importance of standardized communication protocols and deployment automation in GenAI applications.

## 6. AI Agentic Workflows

### 6.1. Song Vocab
*Reference: [song-vocab](./song-vocab/README.md)*

A comprehensive application demonstrating AI agentic workflows:

- **Database Layer:** SQLite3 with Pydantic models for data validation
- **Agent Layer:** OpenAI GPT-4o powering web search and vocabulary generation
- **Presentation Layer:** Streamlit for an interactive user interface

**Implementation Journey:**
1. **Database and Data Modeling:** Created schema and CRUD operations for songs and vocabulary
2. **OpenAI Agents Integration:** Implemented web search and vocabulary generation using responses API
3. **Streamlit UI Development:** Built an intuitive interface for searching songs and learning vocabulary

**Technical Highlights:**
- Web search integration using OpenAI's tools
- Structured output generation with JSON schema
- Asynchronous operations in a synchronous UI context
- Database integration for persistent storage

**Learning Outcomes:**
- Practical application of prompt engineering for specialized tasks
- Techniques for getting consistent structured data from LLMs
- Integration patterns for combining multiple AI capabilities
- Error handling strategies for AI-powered applications

This project represents the culmination of my GenAI Bootcamp journey, demonstrating how to combine multiple AI capabilities into a cohesive application with practical utility for language learners, particularly those studying Jamaican Patois.

## 7. AI Deployment and Security
*Reference: [deploy-ai](./deploy-ai/README.md)*

Exploring best practices for deploying and securing AI applications:
- Cloud deployment strategies for AI/ML models
- Security considerations for LLM-powered applications
- Cost optimization techniques for AI inference
- Monitoring and observability of AI systems
- Compliance and governance frameworks

**Key Learnings:**
- Implemented secure API endpoints with proper authentication
- Explored rate limiting and usage tracking for AI services
- Evaluated various deployment options (serverless, containers, VMs)
- Documented strategies for protecting prompt inputs and model outputs
- Researched techniques for preventing prompt injection attacks

This module provided critical insights into the operational aspects of AI applications beyond development. Understanding how to properly deploy, secure, and monitor LLM-based applications is essential for building production-ready systems that can be safely used by real users while managing costs effectively.


