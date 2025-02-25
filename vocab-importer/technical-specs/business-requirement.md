# Vocab Importer

##  Business Goal: 
The prototype of the language learning app is built, but we need to quickly populate the application with word and word groups so students can begin testing the system.

There is currently no interface for manually adding words or words groups and the process would be too tedious. 

You have been asked to:
- create an internal facing tool to generate vocab 
- Be able to export the generated vocab to json for later import
- Be able  to import to import json files

## Technical Restrictions
Since this is an internal facing tool the fractional CTO wants you to use an app prototyping framework of your choice:
- Gradio
- Streamlit
- FastHTML
- Some other framework

You need to use an LLM in order to generate the target words and word groups.
You can use either an:
- Managed/Serverless LLM API
- Local LLM serving the model via OPEA
