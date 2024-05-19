- similarity_checker.py
- llm_processor.py

## similarity_checker.py

This script provides a method for automatically grouping similar articles within a dataset. It leverages NLP techniques to analyze the textual content of the articles, preprocess them for consistency, and calculate their similarity. The grouping process allows you to cluster articles based on their content, aiding in organization, analysis, or recommendation systems.

Similarity stuff is specifically configured for Italian language, You can change it to any ntlk supported language of course.

Usage:

- Input Data: Ensure your article data is in a list of dictionaries format, with each dictionary containing 'title' and 'content' keys.
- Similarity Threshold: Adjust the similarity_threshold parameter (default: 0.5) to control how strict the grouping is. Higher values result in more similar articles being grouped together.
- Run the Script: Execute the script, and it will return the grouped articles.

**Components**

1. **Imports:** The code brings in necessary libraries and modules for text processing, language models, similarity calculation, progress tracking, and data structures.

2. **Language Model Setup (spaCy):** It initializes a spaCy language model specifically trained for Italian news. This model is used for text preprocessing and understanding linguistic features. If it's not present, it'll be automatically downloaded.

3. **NLP Tool Initialization:**
   - **Lemmatizer:** This tool reduces words to their base or dictionary form (e.g., "running" becomes "run").
   - **Stopwords:** This is a list of common words (e.g., "the", "and") that are often removed from text before analysis, as they might not carry significant meaning.

4. **`preprocess_text` Function:**
   - Cleans the text by removing HTML tags, converting to lowercase, and removing punctuation.
   - Lemmatizes the words to ensure consistency.
   - Removes Italian stopwords to focus on the more important words.

5. **`group_similar_articles` Function:**
   - This is the core of the script. It takes a list of articles (each containing a title and content) and a similarity threshold as input.
   - It processes the articles, calculates their similarity using TF-IDF vectors and cosine similarity, and then groups them based on the threshold.
   - It uses an iterative depth-first search algorithm to efficiently find groups of similar articles.
   - Optionally, it can return the groups either as a simple list or as a dictionary, where each group is associated with an ID.

**How It Works**

1. **Preprocessing:** The text of each article (title and content combined) is preprocessed using the `preprocess_text` function to standardize and simplify the text.

2. **TF-IDF Representation:**  TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic that reflects how important a word is to a document in a collection or corpus. The code converts the preprocessed articles into a TF-IDF matrix, representing each article as a vector of numbers.

3. **Cosine Similarity:**  Cosine similarity is a measure of similarity between two non-zero vectors. The code calculates the cosine similarity between each pair of article vectors. Higher cosine similarity values indicate greater similarity between the articles.

4. **Grouping:** The script then uses an iterative depth-first search algorithm to group articles based on the similarity threshold. If the similarity between two articles is above the threshold, they are grouped together.


## llm_processor.py

This script is designed to take multiple news sources about a single event, combine their information, and generate a comprehensive, well-formatted news article using an LLM API. The script reads input from JSON files, processes them, and produces rewritten articles in the same format. It is ideal for automating news aggregation and consolidation tasks.

**Prerequisites:**
- **LLM API:** Ensure you have an LLM API running locally (or modify the `API_URL` accordingly).
- **JSON Files:**  Place your JSON files containing the multiple news sources in the `OUTPUT_FOLDER`.

**Usage:**
1. Run the script. It will automatically process all JSON files in the `OUTPUT_FOLDER`.
2. The rewritten articles will be saved in the `REWRITTEN_FOLDER`.

**Components**

1. **Imports:** The code imports libraries for handling JSON, making HTTP requests, logging, working with file paths, managing dates and times, and retrying failed requests.

2. **Constants:** The script defines several constants:
   - `API_URL`: The address of the local LLM API.
   - `OUTPUT_FOLDER`: The folder where the original JSON files are located.
   - `REWRITTEN_FOLDER`: The folder where the rewritten JSON files will be saved.
   - `RETRIES`: The number of times to retry failed HTTP requests.
   - `BACKOFF_FACTOR`: Controls the delay between retries.
   - `HEADERS`: Headers for the HTTP requests to the API.
   - `COMBINED_CONTENT_PREFIX`: Instructions for the LLM to combine and format the news content from the multiple sources.

3. **Logging Setup:** Basic logging is configured to record events during the script's execution.

4. **`requests_retry_session` Function:** This function creates a requests session that automatically retries failed HTTP requests, which can be helpful when dealing with unreliable network connections or APIs.

5. **`call_llm_api` Function:** This function sends the combined news content to the LLM API. It crafts a JSON payload with the content and model information, makes the POST request, and parses the response to retrieve the rewritten content. If the request fails, it logs an error.

6. **`ensure_proper_punctuation` Function:** This function ensures that the text generated by the LLM has proper punctuation by adding periods to the end of sentences if they're missing.

7. **`process_json_file` Function:** This is the main workhorse of the script:
   - It reads a JSON file containing multiple news sources.
   - It combines the content from these sources, adding a prefix with instructions for the LLM.
   - It calls the `call_llm_api` function to get the rewritten content from the LLM.
   - It cleans up the returned content by removing formatting and irrelevant information.
   - It ensures proper punctuation and adds the current date and time.
   - It extracts links from the original JSON data.
   - It creates a new JSON object with the rewritten content and other details, and saves it to a file in the `REWRITTEN_FOLDER`.

8. **`main` Function:**
   - It creates the `REWRITTEN_FOLDER` if it doesn't exist.
   - It finds all JSON files in the `OUTPUT_FOLDER`.
   - It iterates through these files, calling `process_json_file` for each one.

**How It Works**

1. **Find JSON Files:** The script starts by locating all JSON files in the `OUTPUT_FOLDER`.
2. **Process Each File:** It processes each JSON file one by one.
3. **Read & Combine Content:** It reads the multiple news sources from the JSON file and combines their content into a single string.
4. **Send to LLM:** It sends this combined content to the LLM API, along with instructions on how to rewrite it.
5. **Clean & Save:** It receives the rewritten content from the LLM, cleans it up, adds metadata (like the date and links), and saves it as a new JSON file in the `REWRITTEN_FOLDER`.
