```
bash-3.2$ ./demo.sh
Please enter up to 100 RSS feeds, either separated by spaces or one per line. Enter an empty line to finish:
http://www.agi.it/cronaca/rss
http://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml
http://www.ansa.it/sito/notizie/mondo/mondo_rss.xml
http://www.ilgiornale.it/taxonomy/term/40820/feed
http://www.repubblica.it/rss/cronaca/rss2.0.xml
http://www.repubblica.it/rss/esteri/rss2.0.xml
https://ilmanifesto.it/feed/
https://tg24.sky.it/rss/tg24_cronaca.xml
https://www.adnkronos.com/RSS_Cronaca.xml
https://www.ansa.it/europa/notizie/rss.xml
https://www.ansa.it/sito/ansait_rss.xml
https://www.ilfattoquotidiano.it/feed/
https://www.ilfoglio.it/cronaca/rss.xml
https://www.ilgiorno.it/rss
https://www.ilmattino.it/rss/
https://www.ilmessaggero.it/rss/cronaca.xml
https://www.ilrestodelcarlino.it/rss
https://www.ilsecoloxix.it/rss/cmlink/secolo-xix-primopiano-1.3408
https://www.ilsole24ore.com/rss/italia--attualita.xml
https://www.lanazione.it/rss
https://www.lastampa.it/rss.xml
https://www.lastampa.it/rss/cronache.xml
https://www.tg24.info/feed/
https://www.tgcom24.mediaset.it/rss/cronaca.xml
https://xml2.corriereobjects.it/rss/cronache.xml

Select model API:
1) Ollama
2) OpenAI
Enter the number corresponding to your choice: 1
Specify OLLAMA_URL for Ollama API (default: http://localhost:11434/api/chat): : http://192.168.100.41:11434/api/chat
Select LLM_MODEL:
1) phi3
2) llama3
Enter the number corresponding to your choice: 1
Starting the process with API: Ollama and Model: phi3...
Starting RSS feed processing...
Fetching and parsing RSS feeds...
Fetching and parsing RSS feeds: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 25/25 [00:07<00:00,  3.21it/s]
Total articles fetched and parsed: 1023
Grouping articles based on similarity (threshold=0.5)...
Grouping articles: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1023/1023 [00:00<00:00, 7398.14it/s]
Total groups formed: 972
Saving grouped articles to JSON files...
Saving groups:   0%|                                                                                                                                      | 0/972 [00:00<?, ?it/s]2024-05-23 22:55:54,418 - INFO - Saved output/20240523_2255-giovanni_tutte_toti-Q2-S0.35.json with 2 items and similarity score 0.35
2024-05-23 22:55:54,419 - INFO - Saved output/20240523_2255-caso_falso_testamento-Q2-S0.57.json with 2 items and similarity score 0.57
2024-05-23 22:55:54,420 - INFO - Saved output/20240523_2255-ilaria_salis_uscita-Q2-S1.00.json with 2 items and similarity score 1.00
2024-05-23 22:55:54,422 - INFO - Saved output/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json with 4 items and similarity score 0.48
2024-05-23 22:55:54,423 - INFO - Saved output/20240523_2255-droga_ordinata_carcere-Q3-S0.59.json with 3 items and similarity score 0.59
2024-05-23 22:55:54,424 - INFO - Saved output/20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json with 2 items and similarity score 0.85
Saving groups: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 972/972 [00:00<00:00, 126823.35it/s]
RSS feed processing complete. 6 different articles are now grouped.
Details of groups saved: [3, 3, 3, 4, 3, 3]
(Took 8.84 seconds)
Summarizing output files:
20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json: 22 lines
20240523_2255-caso_falso_testamento-Q2-S0.57.json: 12 lines
20240523_2255-ilaria_salis_uscita-Q2-S1.00.json: 12 lines
20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json: 12 lines
20240523_2255-droga_ordinata_carcere-Q3-S0.59.json: 17 lines
20240523_2255-giovanni_tutte_toti-Q2-S0.35.json: 12 lines
Total output files: 6
2024-05-23 22:55:55,117 - INFO - Processing file: output/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json
2024-05-23 22:55:55,118 - INFO - Processing output/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json - combined content prepared.
2024-05-23 22:57:06,578 - INFO - Rewritten file saved to rewritten/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48_rewritten.json
2024-05-23 22:57:06,578 - INFO - Processing file: output/20240523_2255-caso_falso_testamento-Q2-S0.57.json
2024-05-23 22:57:06,578 - INFO - Processing output/20240523_2255-caso_falso_testamento-Q2-S0.57.json - combined content prepared.
2024-05-23 22:58:03,309 - INFO - Rewritten file saved to rewritten/20240523_2255-caso_falso_testamento-Q2-S0.57_rewritten.json
2024-05-23 22:58:03,309 - INFO - Processing file: output/20240523_2255-ilaria_salis_uscita-Q2-S1.00.json
2024-05-23 22:58:03,309 - INFO - Processing output/20240523_2255-ilaria_salis_uscita-Q2-S1.00.json - combined content prepared.
2024-05-23 22:59:07,924 - INFO - Rewritten file saved to rewritten/20240523_2255-ilaria_salis_uscita-Q2-S1.00_rewritten.json
2024-05-23 22:59:07,925 - INFO - Processing file: output/20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json
2024-05-23 22:59:07,925 - INFO - Processing output/20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json - combined content prepared.
2024-05-23 22:59:29,428 - INFO - Rewritten file saved to rewritten/20240523_2255-taiwan__aerei_guerra-Q2-S0.85_rewritten.json
2024-05-23 22:59:29,428 - INFO - Processing file: output/20240523_2255-droga_ordinata_carcere-Q3-S0.59.json
2024-05-23 22:59:29,429 - INFO - Processing output/20240523_2255-droga_ordinata_carcere-Q3-S0.59.json - combined content prepared.
2024-05-23 23:00:11,625 - INFO - Rewritten file saved to rewritten/20240523_2255-droga_ordinata_carcere-Q3-S0.59_rewritten.json
2024-05-23 23:00:11,625 - INFO - Processing file: output/20240523_2255-giovanni_tutte_toti-Q2-S0.35.json
2024-05-23 23:00:11,626 - INFO - Processing output/20240523_2255-giovanni_tutte_toti-Q2-S0.35.json - combined content prepared.
2024-05-23 23:00:54,115 - INFO - Rewritten file saved to rewritten/20240523_2255-giovanni_tutte_toti-Q2-S0.35_rewritten.json
RSS feed successfully created at uglyfeeds/uglyfeed.xml
Serving uglyfeed.xml at: http://192.168.100.6:8000/uglyfeed.xml
```

Viewing single item on FluentReader

![demo](https://raw.githubusercontent.com/fabriziosalmi/UglyFeed/main/docs/demo.png)


#### Evaluations

Evaluate metrics of generated files against reference files:

```
python evaluate_against_reference.py

Evaluating: 20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json
Evaluating: 20240523_2255-ilaria_salis_uscita-Q2-S1.00.json
Evaluating: 20240523_2255-caso_falso_testamento-Q2-S0.57.json
Evaluating: 20240523_2255-giovanni_tutte_toti-Q2-S0.35.json
Evaluating: 20240523_2255-droga_ordinata_carcere-Q3-S0.59.json
Evaluating: 20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json
Results saved to reports/evaluation_results.json and reports/evaluation_results.html

cat reports/evaluation_results.json
[
    {
        "Output File": "output/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48.json",
        "BLEU-1": 0.7142857142857143,
        "Jaccard Similarity": 0.35714285714285715,
        "ROUGE-L": 0.10526315789473684,
        "TF-IDF Cosine Similarity": 0.7109488811714723,
        "METEOR": 0.23280791531738962,
        "Edit Distance": 0.5263157894736842,
        "BoW Cosine Similarity": 0.7820408830054595,
        "WER": 0.8461538461538461,
        "CIDEr": 16.993741140980674,
        "Hamming Distance": 11,
        "F1 Score": 0.5263157894736842,
        "Overlap Coefficient": 0.7142857142857143,
        "Dice Coefficient": 0.5263157894736842,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 8,
        "Readability Score": 3.32,
        "Sentence BLEU": 0.43734770368552467,
        "SMOG Index": 15.200000000000001,
        "ARI Score": 27.6,
        "NIST Score": 0.7523186607677644,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 1.0,
        "Lexical Density": 0.846195652173913,
        "Gunning Fog Index": 15.2,
        "Coleman Liau Index": 26.92,
        "Automated Readability Index": 27.6,
        "Aggregated Score": 67.01110374910445
    },
    {
        "Output File": "output/20240523_2255-ilaria_salis_uscita-Q2-S1.00.json",
        "BLEU-1": 0.6,
        "Jaccard Similarity": 0.42857142857142855,
        "ROUGE-L": 0.18181818181818182,
        "TF-IDF Cosine Similarity": 0.3775326992215303,
        "METEOR": 0.3510657938905673,
        "Edit Distance": 0.5454545454545454,
        "BoW Cosine Similarity": 0.5096059227876986,
        "WER": 5.868421052631579,
        "CIDEr": 4.3481811614475,
        "Hamming Distance": 5,
        "F1 Score": 0.6,
        "Overlap Coefficient": 0.6,
        "Dice Coefficient": 0.6,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 4,
        "Readability Score": 4.155,
        "Sentence BLEU": 0.5222329678670935,
        "SMOG Index": 9.25,
        "ARI Score": 36.65,
        "NIST Score": 1.1743067164455423,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 1.0,
        "Lexical Density": 0.8225393028024607,
        "Gunning Fog Index": 16.43,
        "Coleman Liau Index": 34.29,
        "Automated Readability Index": 36.65,
        "Aggregated Score": 24.00263241155164
    },
    {
        "Output File": "output/20240523_2255-caso_falso_testamento-Q2-S0.57.json",
        "BLEU-1": 0.6,
        "Jaccard Similarity": 0.375,
        "ROUGE-L": 0.18181818181818182,
        "TF-IDF Cosine Similarity": 0.6303678553882509,
        "METEOR": 0.460815503003003,
        "Edit Distance": 0.5454545454545454,
        "BoW Cosine Similarity": 0.7341342997555474,
        "WER": 4.071428571428571,
        "CIDEr": 11.855214367454591,
        "Hamming Distance": 5,
        "F1 Score": 0.5454545454545454,
        "Overlap Coefficient": 0.6,
        "Dice Coefficient": 0.5454545454545454,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 4,
        "Readability Score": -25.48,
        "Sentence BLEU": 0.4386913376508308,
        "SMOG Index": 16.35,
        "ARI Score": 37.45,
        "NIST Score": 1.3481522047781656,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 1.0,
        "Lexical Density": 0.7953964194373402,
        "Gunning Fog Index": 17.09,
        "Coleman Liau Index": 36.975,
        "Automated Readability Index": 37.45,
        "Aggregated Score": 43.15426135405814
    },
    {
        "Output File": "output/20240523_2255-giovanni_tutte_toti-Q2-S0.35.json",
        "BLEU-1": 0.6,
        "Jaccard Similarity": 0.375,
        "ROUGE-L": 0.18181818181818182,
        "TF-IDF Cosine Similarity": 0.48351711078390575,
        "METEOR": 0.39043069684627296,
        "Edit Distance": 0.5454545454545454,
        "BoW Cosine Similarity": 0.5992369152819312,
        "WER": 4.0227272727272725,
        "CIDEr": 6.776268813386874,
        "Hamming Distance": 5,
        "F1 Score": 0.5454545454545454,
        "Overlap Coefficient": 0.6,
        "Dice Coefficient": 0.5454545454545454,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 4,
        "Readability Score": -32.905,
        "Sentence BLEU": 0.4594336333128949,
        "SMOG Index": 9.05,
        "ARI Score": 35.8,
        "NIST Score": 1.3481522047781656,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 1.0,
        "Lexical Density": 0.8179223744292237,
        "Gunning Fog Index": 20.065,
        "Coleman Liau Index": 34.11,
        "Automated Readability Index": 35.8,
        "Aggregated Score": 39.16886129110789
    },
    {
        "Output File": "output/20240523_2255-droga_ordinata_carcere-Q3-S0.59.json",
        "BLEU-1": 0.6666666666666666,
        "Jaccard Similarity": 0.36363636363636365,
        "ROUGE-L": 0.13333333333333333,
        "TF-IDF Cosine Similarity": 0.4900922884035068,
        "METEOR": 0.36998191681735987,
        "Edit Distance": 0.5333333333333333,
        "BoW Cosine Similarity": 0.610736534441601,
        "WER": 1.964705882352941,
        "CIDEr": 8.942340347421618,
        "Hamming Distance": 8,
        "F1 Score": 0.5333333333333333,
        "Overlap Coefficient": 0.6666666666666666,
        "Dice Coefficient": 0.5333333333333333,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 6,
        "Readability Score": -3.7499999999999996,
        "Sentence BLEU": 0.46775793659417675,
        "SMOG Index": 17.3,
        "ARI Score": 31.799999999999997,
        "NIST Score": 1.0566416671474372,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 1.0,
        "Lexical Density": 0.8370388349514564,
        "Gunning Fog Index": 17.1,
        "Coleman Liau Index": 29.7,
        "Automated Readability Index": 31.799999999999997,
        "Aggregated Score": 54.42465001642002
    },
    {
        "Output File": "output/20240523_2255-taiwan__aerei_guerra-Q2-S0.85.json",
        "BLEU-1": 0.6,
        "Jaccard Similarity": 0.42857142857142855,
        "ROUGE-L": 0.18181818181818182,
        "TF-IDF Cosine Similarity": 0.611599486750694,
        "METEOR": 0.44633478391356535,
        "Edit Distance": 0.5454545454545454,
        "BoW Cosine Similarity": 0.7351060940956757,
        "WER": 2.4864864864864864,
        "CIDEr": 4.436442501126439,
        "Hamming Distance": 5,
        "F1 Score": 0.6,
        "Overlap Coefficient": 0.6,
        "Dice Coefficient": 0.6,
        "Longest Common Subsequence": 1,
        "Levenshtein Distance": 4,
        "Readability Score": -33.485,
        "Sentence BLEU": 0.36889397323344053,
        "SMOG Index": 8.9,
        "ARI Score": 41.3,
        "NIST Score": 1.1743067164455423,
        "LSA Similarity": 1.0,
        "Sentiment Analysis": 0.19999999999999996,
        "Lexical Density": 0.7430103745384209,
        "Gunning Fog Index": 17.915,
        "Coleman Liau Index": 41.1,
        "Automated Readability Index": 41.3,
        "Aggregated Score": 50.95148537851307
    }
]
```

Evaluate metrics of generated files 

```
cat rewritten/20240523_2255-crosetto_ambulanza_ministro-Q4-S0.48_rewritten_metrics_merged.json
{
    "Noun and Verb Metrics": {
        "Concrete Noun Ratio": 0.0,
        "Abstract Noun Ratio": 0.023809523809523808
    },
    "Aggregated Noun and Verb Score": 2.380952380952381,
    "Cohesion Concreteness": {
        "Cohesion Score": 1.0,
        "Concreteness Score": 0.0,
        "Imageability Score": 0.0,
        "Age of Acquisition Score": 0.0,
        "Text Familiarity Index": 0.2608695652173913
    },
    "Aggregated Cohesion Concreteness Score": 25.217391304347824,
    "Punctuation and Function Word Metrics": {
        "Punctuation Frequency": {
            ",": 6,
            ".": 6
        },
        "Ellipsis Frequency": 0.0,
        "Conjunction Usage Frequency": 0.0125,
        "Preposition Usage Frequency": 0.11875
    },
    "Aggregated Punctuation and Function Word Score": 29.127846790890267,
    "Information and Density Metrics": {
        "Information Density": 0.4251497005988024,
        "Referential Density": 0.029940119760479042,
        "Cohesive Harmony Index": 0.041916167664670656
    },
    "Aggregated Information and Density Score": 28.605645851154833,
    "Text Cohesion and Information Density Metrics": {
        "Coh-Metrix Scores": 0.5,
        "Cohesion Score": 3.6,
        "Cohesive Harmony Index": 0.8333333333333334,
        "Referential Density": 0.2754491017964072,
        "Information Density": 0.6894409937888198
    },
    "Aggregated Text Cohesion and Information Density Score": 65.96446857837121,
    "Text Structural Metrics": {
        "Subordination Index": 0.3333333333333333,
        "Coordination Index": 0.3333333333333333,
        "Discourse Marker Frequency": 0.0
    },
    "Aggregated Text Structural Score": 46.666666666666664,
    "Text Statistical Metrics": {
        "Jaro-Winkler Distance": 0.4946944673823287,
        "Honore\u2019s Statistic": 1068.4576453123846,
        "Sichel\u2019s Measure": 0.1111111111111111,
        "Brunet\u2019s Measure": 10.421629307974406,
        "Yule\u2019s Characteristic K": 86.71875,
        "MTLD (Measure of Textual Lexical Diversity)": 133.28986501944635,
        "HD-D (Hypergeometric Distribution D)": 0.8598234825917903,
        "Variability Index": 0.675
    },
    "Aggregated Text Statistical Score": 53.699780302967184,
    "Lexical and Syntactic Metrics": {
        "Named Entity Recognition (NER) Coverage": 0.0,
        "Dependency Tree Depth": 8,
        "Syntactic Variability": 1.0,
        "Lexical Density": 0.51875,
        "Passive Voice Percentage": 0.0,
        "Longest Increasing Subsequence": 20
    },
    "Aggregated Lexical and Syntactic Score": 29.9851625,
    "Text Frequency Metrics": {
        "Stopword Ratio": 0.031055900621118012,
        "Hapax Legomena Ratio": 0.5279503105590062,
        "Hapax Dislegomena Ratio": 0.09937888198757763,
        "Mean Sentence Length": 26.833333333333332,
        "Mean Word Length": 5.527950310559007,
        "Syllable per Word": 1.7763975155279503,
        "Clause per Sentence": 2.0
    },
    "Aggregated Frequency Score": 3.6796066252588,
    "Aggregated Cohesion Information Density Score": 65.96446857837121,
    "Overall Average Aggregated Score": 36.61953970527904
}
```
