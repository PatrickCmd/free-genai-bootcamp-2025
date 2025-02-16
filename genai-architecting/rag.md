# How RAG Works

RAG, or Retrieval-Augmented Generation, is a framework that combines retrieval-based and generation-based approaches to enhance the capabilities of language models. It consists of two main workflows: the Text Generation Workflow and the Data Ingestion Workflow.

## Text Generation Workflow

1. **User Input:**
   - The process begins with the user providing input, which could be a question or a prompt.

2. **Embeddings Model:**
   - The user input is processed by an embeddings model. This model converts the input into a numerical representation known as an embedding. Embeddings capture the semantic meaning of the input.

3. **Semantic Search:**
   - The embedding is used to perform a semantic search in a vector store. This search retrieves relevant documents or data that are semantically similar to the input.

4. **Context:**
   - The retrieved documents are used to create a context. This context is crucial for enhancing the understanding of the input and providing more accurate responses.

5. **Prompt Augmentation:**
   - The original user input is augmented with the retrieved context. This augmented prompt is then used to query a large language model.

6. **Large Language Model:**
   - The large language model processes the augmented prompt to generate a response. This model leverages the context to provide more informed and relevant answers.

7. **Response:**
   - Finally, the generated response is delivered to the user.

## Data Ingestion Workflow

1. **New Data:**
   - The workflow begins with the ingestion of new data, which could be documents, articles, or any other relevant information.

2. **Document Store:**
   - The new data is stored in a document store. This store acts as a repository for all the information that can be retrieved during the text generation process.

3. **Embeddings Model:**
   - The data in the document store is processed by an embeddings model to create embeddings for each document. These embeddings are stored in a vector store.

4. **Vector Store:**
   - The vector store holds the embeddings of all documents. It enables efficient semantic search by allowing quick retrieval of documents that are semantically similar to a given input.

By integrating these two workflows, RAG effectively combines the strengths of retrieval-based and generation-based models, resulting in more accurate and contextually relevant responses.