# Tuning

**Tune it for your own needs**
- 🎛️ Customize user prompt, check the [prompts](https://github.com/fabriziosalmi/UglyFeed/tree/main/prompts) folder for inspiration. You can also check the [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts)
- 🎛️ Force specific languages to use for generation just by using specific prompts
- 📈 Evaluate generated content against several [metrics](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/metrics.md) (an aggregated score is provided too) by running `python evaluate_against_reference.py` to evaluate comparison metrics of generated files against the reference files or `python process_multiple_metrics.py` to evaluate only the generated content files against different metrics
- 🕒 Setup a cronjob to have fresh content automatically updated on your RSS reader by executing all files in the order specified

**Tune it by using 3rd party tools**
- 🔁 Create RSS from any content by using [RSSHub](https://github.com/DIYgod/RSSHub) and rewrite its feeds by using [UglyFeed](https://github.com/fabriziosalmi/UglyFeed)
- 🎛️ Customize system prompt [by using OpenWebUI](https://github.com/open-webui/open-webui) on top of Ollama or [by using Ollama itself](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- 🌎 You can reach your local generated feed securely via Internet by using solutions like ngrok, cloudflared, wireguard, tailscale and so on

**How to improve RSS source content before to be processed by UglyFeed**
- [Create RSS from any source via RSSHub](https://github.com/fabriziosalmi/UglyFeed/blob/main/docs/sources.md)

