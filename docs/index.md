---
layout: home
title: UglyFeed — AI-Powered RSS Feed Orchestrator
titleTemplate: false

hero:
  name: "UglyFeed"
  text: "Orchestrate, Filter & Rewrite RSS Feeds with Large Language Models"
  tagline: "Automated multi-source RSS feed aggregation, semantic deduplication, and AI rewriting using Google Gemini, OpenAI, Groq, and Ollama."
  image:
    src: /UglyFeed-diagram.png
    alt: UglyFeed Architecture Diagram
  actions:
    - theme: brand
      text: Quickstart Guide
      link: /guide/introduction
    - theme: alt
      text: Free Gemini Setup
      link: /free-gemini-setup
    - theme: alt
      text: GitHub (318 ⭐)
      link: https://github.com/fabriziosalmi/UglyFeed

features:
  - icon: 🤖
    title: Multi-Model LLM Engine
    details: Seamlessly integrate Google Gemini (including free tiers), OpenAI GPT-4o, Groq Llama 3, and local Ollama instances.
  - icon: ⚡
    title: Semantic Deduplication
    details: Vector similarity algorithms ensure your aggregated feeds contain zero duplicate or redundant stories across news sources.
  - icon: 📦
    title: Zero-Cost GitHub Actions CDN
    details: Schedule daily runs via GitHub Actions that automatically commit your clean, rewritten feeds to any public Git repository.
  - icon: 🎯
    title: Quality & Readability Metrics
    details: Built-in evaluation framework measuring hallucination safeguards, readability scoring, and reference dataset alignment.
  - icon: 🐳
    title: Docker & Web UI
    details: Run locally with Streamlit Web GUI or deploy with Docker & Docker Compose on Portainer, VPS, or Kubernetes.
  - icon: 🛡️
    title: Standards & Security
    details: RFC 9116 security.txt declaration, llms.txt context file, and Schema.org structured data.
---

<div class="vp-doc" style="max-width: 960px; margin: 40px auto 0 auto; padding: 0 24px;">

## 🚀 Quick Navigation

| Topic | Description | Link |
|---|---|---|
| **Getting Started** | Overview, architecture, and installation options | [Introduction →](/guide/introduction) |
| **Docker Deployment** | Standalone container and Compose stack | [Docker Guide →](/docker) |
| **Google Gemini Setup** | Free API key configuration & tips | [Free Gemini Setup →](/free-gemini-setup) |
| **Core Architecture** | Detailed documentation for all Python modules | [Modules →](/main.py) |
| **Evaluation Metrics** | Benchmarking and similarity evaluation tools | [Metrics System →](/metrics) |
| **Troubleshooting** | Solutions for empty feeds, title errors, and rate limits | [Troubleshooting →](/troubleshooting) |

</div>
