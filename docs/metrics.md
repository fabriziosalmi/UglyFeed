### Metrics with Native 0 to 1 Range

| Metric                       | Interpretation                                                   | Description                                                          |
|------------------------------|------------------------------------------------------------------|----------------------------------------------------------------------|
| **BLEU-1**                   | Higher is better; 1 means perfect overlap with reference text.    | Measures the precision of n-grams (unigrams) between candidate and reference text. |
| **Jaccard Similarity**       | Higher is better; 1 means sets are identical.                     | Measures the similarity between two sets by comparing their intersection and union. |
| **ROUGE-L**                  | Higher is better; 1 means perfect match in longest common subsequences. | Measures the longest common subsequence between candidate and reference text. |
| **TF-IDF Cosine Similarity** | Higher is better; 1 means vectors are identical.                  | Measures the cosine similarity between TF-IDF vectors of two texts.  |
| **METEOR**                   | Higher is better; closer to 1 indicates better alignment with reference. | Evaluates translation quality based on precision, recall, and synonym matching. |
| **BoW Cosine Similarity**    | Higher is better; 1 means vectors are identical.                  | Measures the cosine similarity between Bag-of-Words vectors of two texts. |
| **F1 Score**                 | Higher is better; 1 means perfect precision and recall.           | Harmonic mean of precision and recall, used in classification tasks. |
| **Overlap Coefficient**      | Higher is better; 1 means complete overlap.                       | Measures the overlap between two sets, focusing on the smaller set.  |
| **Dice Coefficient**         | Higher is better; 1 indicates complete overlap.                   | Measures the similarity between two sets based on their intersection and total size. |
| **Longest Common Subsequence** (Normalized)| Higher is better; 1 means sequences are identical. | Measures the length of the longest subsequence present in both sequences. |
| **Type-Token Ratio**         | Higher is better; measures lexical diversity.                     | Ratio of unique words (types) to total words (tokens) in a text.     |
| **Lexical Diversity**        | Higher is better; measures variety in vocabulary.                 | Indicates the diversity of the vocabulary used in a text.            |

### Other Metrics

| Metric                       | Typical Range           | Interpretation                                                   | Description                                                          |
|------------------------------|-------------------------|------------------------------------------------------------------|----------------------------------------------------------------------|
| **Edit Distance**            | 0 to length of string   | Lower is better; 0 means no edits needed.                         | Measures the minimum number of edits needed to transform one string into another. |
| **WER (Word Error Rate)**    | 0 to infinity           | Lower is better; 0 means no errors.                               | Measures the rate of errors in a transcription compared to a reference. |
| **CIDEr**                    | Usually 0 to 10+        | Higher is better; specific to image captioning tasks.             | Evaluates the consensus between candidate and reference captions using TF-IDF weighting. |
| **Hamming Distance**         | 0 to length of string   | Lower is better; 0 means strings are identical.                   | Measures the number of differing characters between two strings of equal length. |
| **Levenshtein Distance**     | 0 to length of string   | Lower is better; 0 means strings are identical.                   | Measures the minimum number of single-character edits needed to change one string into another. |
| **Average Token Length**     | No fixed range          | Provides insight into the complexity of the tokens.               | Average length of tokens (words) in a text.                          |
| **Gunning Fog Index**        | Usually 0 to 20+        | Lower is better; measures readability.                            | Estimates the years of formal education needed to understand a text on the first reading. |
| **Automated Readability Index** | Usually 0 to 20+      | Lower is better; measures readability.                            | Estimates the years of education required to understand a text.      |
| **Syntactic Complexity**     | No fixed range          | Higher often indicates more complex syntax.                       | Measures the complexity of syntactic structures in a text.           |
| **Readability Consensus**    | No fixed range          | Measures overall readability based on multiple metrics.           | Aggregates multiple readability scores into a single consensus score. |
| **Entropy**                  | No fixed range          | Measures unpredictability or complexity.                          | Quantifies the randomness or disorder within a set of data.          |

These tables provide a comprehensive overview of each metric, including their typical ranges, interpretations, and descriptions.
