# Sentence Constructor for Learning Jamaican Patois

This documentation outlines how the Sentence Constructor application utilizes AI-powered assistants, specifically OpenAI's ChatGPT (GPT-4o) and Meta AI, to aid students in learning Jamaican Patois. The application is designed to provide structured guidance and interactive learning experiences.

## Overview

The Sentence Constructor application leverages AI models to assist students in translating English sentences into Jamaican Patois. The AI models provide vocabulary, sentence structures, and clues to help students construct sentences, encouraging active engagement and learning.

## AI Assistants Used

### 1. OpenAI's ChatGPT (GPT-4o)

**Model:** GPT-4o is one of the latest and most advanced models in the GPT family. It is a multi-modal model capable of processing text, images, and audio, making it highly versatile for educational applications.

**Usage in Sentence Constructor:**
- **Role:** Jamaican Patois Language Teacher
- **Language Level:** Beginner
- **Teaching Instructions:** 
  - Students provide an English sentence.
  - The AI helps transcribe the sentence into Jamaican Patois using clues.
  - A vocabulary table is provided, including nouns, verbs, adverbs, and adjectives.
  - Sentence structures are suggested without particles, tenses, or conjugations.
  - Clues and considerations are offered to guide students in constructing sentences.

**Prompt Engineering:**
- The prompt is designed to encourage students to think critically and engage with the language.
- The AI does not provide direct answers but offers structured guidance through vocabulary tables and sentence structures.

**Example:**
- **Student Input:** "Did you see the raven this morning? They were looking at our garden."
- **AI Output:** Provides vocabulary, sentence structure, and clues to help the student construct the sentence in Patois.

### 2. Meta AI

**Model:** Meta AI uses the Llama 3 70B model, which is known for its robust language processing capabilities.

**Usage in Sentence Constructor:**
- **Role:** Jamaican Patois Language Teacher
- **Language Level:** Beginner
- **Teaching Instructions:**
  - Similar to ChatGPT, students provide an English sentence.
  - The AI assists in transcribing the sentence into Jamaican Patois using clues.
  - A vocabulary table is provided, focusing on verbs, adverbs, adjectives, and nouns.
  - Sentence structures are suggested without particles, tenses, or conjugations.

**Prompt Engineering:**
- The prompt is crafted to ensure students engage with the language by figuring out the correct particles and conjugations themselves.
- The AI provides clues and considerations to help students understand sentence construction in Patois.

**Example:**
- **Student Input:** "Bears are at the door, did you leave the garbage out?"
- **AI Output:** Offers vocabulary, sentence structure, and clues to guide the student in constructing the sentence in Patois.

## Future Investigations

In the future, we plan to explore the use of open-source models to further enhance the Sentence Constructor application. This will involve testing the prompt document with models such as Llama3.1 8B, Deepseek-R1, phi4, Mistral, Gemma, Qwen, and others. These models will be evaluated locally using platforms like Ollama and OpenWeb UI to determine their effectiveness in processing and understanding Jamaican Patois.

## Conclusion

The Sentence Constructor application effectively uses AI-powered assistants to enhance the learning experience for students studying Jamaican Patois. By providing structured guidance and interactive learning opportunities, the application helps students develop a deeper understanding of the language.

For more information on using these AI models, refer to the respective documentation for [OpenAI's GPT-4o](https://platform.openai.com/docs/models#gpt-4o) and [Meta AI's Llama 3 70B](https://huggingface.co/meta-llama/Meta-Llama-3-70B).
