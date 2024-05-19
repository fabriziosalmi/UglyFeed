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
