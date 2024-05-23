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
