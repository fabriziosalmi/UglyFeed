# Metrics

## Evaluation of the generated content

| **Metric Group**                          | **Metric**                          | **Range**           | **Interpretation**                                                                 |
|-------------------------------------------|-------------------------------------|---------------------|-----------------------------------------------------------------------------------|
| **Noun and Verb Metrics**                 | Concrete Noun Ratio                 | 0 to 1              | Higher values indicate a greater use of concrete nouns, making the text more tangible. |
|                                           | Abstract Noun Ratio                 | 0 to 1              | Higher values indicate a greater use of abstract nouns, making the text more conceptual. |
| **Cohesion Concreteness**                 | Cohesion Score                      | 0 to 1              | Higher scores indicate better logical flow and connectivity of ideas.                 |
|                                           | Concreteness Score                  | 0 to 1              | Higher scores indicate that the text refers more to tangible objects and concepts.     |
|                                           | Imageability Score                  | 0 to 1              | Higher scores indicate that the text easily evokes mental images.                      |
|                                           | Age of Acquisition Score            | 0 to 1              | Lower scores indicate words are typically learned at a younger age, making the text more accessible. |
|                                           | Text Familiarity Index              | 0 to 1              | Higher scores indicate the text uses more common and familiar words.                  |
| **Punctuation and Function Word Metrics** | Punctuation Frequency               | 0 to ∞              | Counts the number of specific punctuation marks, indicating sentence structure and pacing. |
|                                           | Ellipsis Frequency                  | 0 to ∞              | Counts the use of ellipses in the text.                                               |
|                                           | Conjunction Usage Frequency         | 0 to 1              | Higher values indicate more frequent use of conjunctions, showing the complexity of sentence structures. |
|                                           | Preposition Usage Frequency         | 0 to 1              | Higher values indicate more frequent use of prepositions, showing detailed descriptions and relationships. |
| **Information and Density Metrics**       | Information Density                 | 0 to 1              | Higher scores indicate a higher amount of information packed into the text.            |
|                                           | Referential Density                 | 0 to 1              | Higher scores indicate more frequent references to entities or concepts within the text. |
|                                           | Cohesive Harmony Index              | 0 to 1              | Higher scores indicate better alignment and harmony of cohesive devices in the text.     |
| **Text Cohesion and Information Density Metrics** | Coh-Metrix Scores                  | 0 to 1              | Scores from the Coh-Metrix tool indicating overall text cohesion.                      |
|                                           | Cohesion Score                      | 0 to 1              | Higher scores indicate better logical flow and connectivity of ideas.                 |
|                                           | Cohesive Harmony Index              | 0 to 1              | Higher scores indicate better alignment and harmony of cohesive devices in the text.     |
|                                           | Referential Density                 | 0 to 1              | Higher scores indicate more frequent references to entities or concepts within the text. |
|                                           | Information Density                 | 0 to 1              | Higher scores indicate a higher amount of information packed into the text.            |
| **Text Structural Metrics**               | Subordination Index                 | 0 to 1              | Higher values indicate more complex sentence structures with subordinate clauses.      |
|                                           | Coordination Index                  | 0 to 1              | Higher values indicate more frequent use of coordinating conjunctions, showing parallel structures. |
|                                           | Discourse Marker Frequency          | 0 to 1              | Higher values indicate more frequent use of discourse markers, which guide the reader through the text. |
| **Text Statistical Metrics**              | Jaro-Winkler Distance               | 0 to 1              | Measures text similarity; higher values indicate greater similarity.                   |
|                                           | Honore’s Statistic                  | 0 to ∞              | Measures vocabulary richness; higher values indicate richer vocabulary.               |
|                                           | Sichel’s Measure                    | 0 to 1              | Measures vocabulary diversity; higher values indicate more diverse vocabulary.         |
|                                           | Brunet’s Measure                    | 0 to ∞              | Measures vocabulary richness; higher values indicate richer vocabulary.               |
|                                           | Yule’s Characteristic K             | 0 to ∞              | Measures vocabulary richness; higher values indicate richer vocabulary.               |
|                                           | MTLD (Measure of Textual Lexical Diversity) | 0 to ∞      | Measures lexical diversity; higher values indicate greater lexical diversity.         |
|                                           | HD-D (Hypergeometric Distribution D) | 0 to 1             | Measures lexical diversity; higher values indicate greater lexical diversity.         |
|                                           | Variability Index                   | 0 to 1              | Measures text variability; higher values indicate more variability.                    |
| **Lexical and Syntactic Metrics**         | Named Entity Recognition (NER) Coverage | 0 to 1          | Higher values indicate more entities (e.g., names, places) are recognized in the text. |
|                                           | Dependency Tree Depth               | 0 to ∞              | Measures syntactic complexity; higher values indicate more complex syntax.             |
|                                           | Syntactic Variability               | 0 to 1              | Higher values indicate greater variety in syntactic structures.                        |
|                                           | Lexical Density                     | 0 to 1              | Higher values indicate a higher proportion of content words (nouns, verbs, adjectives, adverbs). |
|                                           | Passive Voice Percentage            | 0 to 1              | Higher values indicate more frequent use of passive voice.                             |
|                                           | Longest Increasing Subsequence      | 0 to ∞              | Measures the length of the longest syntactic subsequence; higher values indicate more complex structures. |
| **Text Frequency Metrics**                | Stopword Ratio                      | 0 to 1              | Higher values indicate a higher proportion of stopwords (common words like "the", "is"). |
|                                           | Hapax Legomena Ratio                | 0 to 1              | Measures the proportion of words that appear only once in the text; higher values indicate more unique words. |
|                                           | Hapax Dislegomena Ratio             | 0 to 1              | Measures the proportion of words that appear exactly twice; higher values indicate more varied vocabulary. |
|                                           | Mean Sentence Length                | 0 to ∞              | Average length of sentences in the text; higher values indicate longer sentences.      |
|                                           | Mean Word Length                    | 0 to ∞              | Average length of words in the text; higher values indicate longer words.              |
|                                           | Syllable per Word                   | 0 to ∞              | Average number of syllables per word; higher values indicate more complex words.       |
|                                           | Clause per Sentence                 | 0 to ∞              | Average number of clauses per sentence; higher values indicate more complex sentence structures. |

## Evaluation of the generated content against the reference

| **Metric**                   | **Range**           | **Interpretation**                                                                                 |
|------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|
| **BLEU-1**                   | 0 to 1              | Measures n-gram precision, with 1 being a perfect match to the reference text.                      |
| **Jaccard Similarity**       | 0 to 1              | Measures the similarity between two sets, with 1 being identical sets.                               |
| **ROUGE-L**                  | 0 to 1              | Measures the longest common subsequence, indicating how well the order of words is preserved.        |
| **TF-IDF Cosine Similarity** | 0 to 1              | Measures the cosine similarity between two texts based on TF-IDF vectors, with 1 being identical.    |
| **METEOR**                   | 0 to 1              | Measures precision, recall, and synonymy, with 1 being a perfect match to the reference text.        |
| **Edit Distance**            | 0 to ∞              | Measures the number of edits needed to transform one text into another, with 0 being identical texts.|
| **BoW Cosine Similarity**    | 0 to 1              | Measures the cosine similarity between two texts based on Bag-of-Words vectors, with 1 being identical.|
| **WER**                      | 0 to 1              | Measures the word error rate, with 0 being a perfect match to the reference text.                    |
| **CIDEr**                    | 0 to ∞              | Measures consensus in image description generation, higher scores indicate better quality.           |
| **Hamming Distance**         | 0 to ∞              | Measures the number of positions at which the corresponding symbols differ, with 0 being identical texts.|
| **F1 Score**                 | 0 to 1              | Measures the balance between precision and recall, with 1 being perfect precision and recall.        |
| **Overlap Coefficient**      | 0 to 1              | Measures the overlap between two sets, with 1 being identical sets.                                  |
| **Dice Coefficient**         | 0 to 1              | Measures the similarity between two sets, with 1 being identical sets.                               |
| **Longest Common Subsequence**| 0 to ∞              | Measures the length of the longest subsequence common to both texts, higher values indicate more similarity.|
| **Levenshtein Distance**     | 0 to ∞              | Measures the minimum number of single-character edits needed to change one text into the other, with 0 being identical texts.|
| **Readability Score**        | 0 to ∞              | Measures how easy a text is to read, higher scores indicate more difficult texts.                     |
| **Sentence BLEU**            | 0 to 1              | Measures n-gram precision for individual sentences, with 1 being a perfect match.                    |
| **SMOG Index**               | 0 to ∞              | Measures the years of education needed to understand a text, higher scores indicate more difficult texts.|
| **ARI Score**                | 0 to ∞              | Automated Readability Index, higher scores indicate more difficult texts.                             |
| **NIST Score**               | 0 to ∞              | Measures precision while giving more weight to informative n-grams, higher scores indicate better quality.|
| **LSA Similarity**           | 0 to 1              | Measures the similarity between two texts using Latent Semantic Analysis, with 1 being identical.     |
| **Sentiment Analysis**       | -1 to 1             | Measures the sentiment of the text, with -1 being very negative, 0 being neutral, and 1 being very positive.|
| **Lexical Density**          | 0 to 1              | Measures the proportion of content words in a text, with higher values indicating more information-rich texts.|
| **Gunning Fog Index**        | 0 to ∞              | Measures the years of formal education needed to understand a text, higher scores indicate more difficult texts.|
| **Coleman Liau Index**       | 0 to ∞              | Measures the years of education needed to understand a text, higher scores indicate more difficult texts.|
| **Automated Readability Index** | 0 to ∞           | Measures the readability of a text, higher scores indicate more difficult texts.                      |




