# Tech Specs
## Business Goal
We want to create a program that will find lyrics off the internet for a target song in a specific langauge and produce vocabulary to be imported into our database using OpenAI Agents (web search, text generation, etc).


1. In the database we should have the following table:
- Song
- Vocabulary

With the following fields:

Song Table:
- Song Title
- Song Lyrics
- Song Language
- Song Artist
- Song Album
- Song Release Date

Vocabulary Table:
- Song ID (foreign key)
- Vocabulary
- Vocabulary Explanation
- Example Sentences

We shall sqlite3 database for now and pydantic for data validation. Write the sql scripts and code to create the database and the pydantic models.
Use usable python modules, packages and utility functions with an orgainised folder structure.

2. For openai agents, we shall use the following:
- Web search agent tool (See documentation here: https://platform.openai.com/docs/guides/tools-web-search?api-mode=responses) to search the internet for the target song lyrics in the target language.
- Function calling (See documentation here: https://platform.openai.com/docs/guides/function-calling?api-mode=responses) and Text generation agent tool to generate the vocabulary and its explanation.
- Function calling (See documentation here: https://platform.openai.com/docs/guides/function-calling?api-mode=responses) and Text generation agent tool to generate the example sentences.

Reference a sample implementation on how to use the web search agent tool [here](./test_web_search.py). Here use the web search agent tool to search the internet for the target song lyrics in the target language and return the song details as defined in the Song table. Use structured output using pydantic models here also in the json schema to return the data.

Then let's pass the song lyrics to another the function calling ([docs](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)) and text generation agent tools to generate the vocabulary and its explanation. Also use structured output using pydantic models here also in the json schema to return the data.

3. For the application ui we shall use streamlit. The use should be able to put the song title, user language and foreign language to get the song lyrics, vocabulary and example sentences. 
Display the song title, song lyrics, vocabulary and example sentences in the ui.
Have a button to save the data to the database from the generated structured json data into the appropriate tables and also export the data to a json file if required.

Organise the code in proper modules, packages and utilities in a good folder structure.

Document each step of the application in the README.


