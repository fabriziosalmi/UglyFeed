import { defineConfig } from "vitepress"

export default defineConfig({
  title: "UglyFeed",
  description: "Retrieve, aggregate, filter, evaluate, rewrite and serve RSS feeds using Large Language Models.",
  base: "/UglyFeed/",
  cleanUrls: true,
  lastUpdated: true,
  ignoreDeadLinks: true,

  sitemap: {
    hostname: "https://fabriziosalmi.github.io/UglyFeed/",
  },

  head: [
    ["link", { rel: "icon", type: "image/svg+xml", href: "/UglyFeed/favicon.svg" }],
    ["link", { rel: "apple-touch-icon", href: "/UglyFeed/favicon.svg" }],
    ["link", { rel: "canonical", href: "https://fabriziosalmi.github.io/UglyFeed/" }],
    ["meta", { name: "theme-color", content: "#10b981" }],
    ["meta", { name: "color-scheme", content: "dark light" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:title", content: "UglyFeed — AI-Powered RSS Feed Orchestrator" }],
    ["meta", { property: "og:description", content: "Retrieve, aggregate, filter, evaluate, rewrite and serve RSS feeds using Large Language Models." }],
    ["meta", { property: "og:url", content: "https://fabriziosalmi.github.io/UglyFeed/" }],
    ["meta", { property: "og:image", content: "https://fabriziosalmi.github.io/UglyFeed/favicon.svg" }],
    ["meta", { name: "twitter:card", content: "summary" }],
    ["meta", { name: "twitter:title", content: "UglyFeed — AI-Powered RSS Feed Orchestrator" }],
    ["meta", { name: "twitter:description", content: "Retrieve, aggregate, filter, evaluate, rewrite and serve RSS feeds using Large Language Models." }],
    ["meta", { name: "twitter:image", content: "https://fabriziosalmi.github.io/UglyFeed/favicon.svg" }],
    ["meta", { name: "robots", content: "index, follow, max-image-preview:large" }],
    [
      "script",
      { type: "application/ld+json" },
      JSON.stringify({
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "SoftwareApplication",
            "@id": "https://fabriziosalmi.github.io/UglyFeed/#software",
            name: "UglyFeed",
            operatingSystem: "Cross-platform",
            applicationCategory: "DeveloperApplication",
            description: "Retrieve, aggregate, filter, evaluate, rewrite and serve RSS feeds using Large Language Models.",
            url: "https://fabriziosalmi.github.io/UglyFeed/",
            license: "https://opensource.org/licenses/MIT",
            codeRepository: "https://github.com/fabriziosalmi/UglyFeed",
            author: {
              "@type": "Person",
              name: "Fabrizio Salmi",
              url: "https://github.com/fabriziosalmi",
            },
          },
          {
            "@type": "WebSite",
            "@id": "https://fabriziosalmi.github.io/UglyFeed/#website",
            url: "https://fabriziosalmi.github.io/UglyFeed/",
            name: "UglyFeed Documentation",
            description: "Retrieve, aggregate, filter, evaluate, rewrite and serve RSS feeds using Large Language Models.",
            publisher: {
              "@type": "Person",
              name: "Fabrizio Salmi",
              url: "https://github.com/fabriziosalmi",
            },
            inLanguage: "en-US",
          },
        ],
      }),
    ],
  ],

  themeConfig: {
    siteTitle: "UglyFeed",

    search: {
      provider: "local",
    },

    nav: [
      { text: "Guide", link: "/guide/introduction", activeMatch: "/guide/" },
      { text: "Modules", link: "/main.py", activeMatch: "/(main|llm_|rss_|similarity_|json)" },
      { text: "AI Setup", link: "/free-gemini-setup", activeMatch: "/(free-gemini|gemini-)" },
      { text: "Metrics", link: "/metrics", activeMatch: "/(metrics|process_multiple|evaluate)" },
      { text: "FAQ", link: "/faq" },
      { text: "GitHub", link: "https://github.com/fabriziosalmi/UglyFeed" },
    ],

    sidebar: [
      {
        text: "Getting Started",
        collapsed: false,
        items: [
          { text: "Introduction", link: "/guide/introduction" },
          { text: "Installation & Quickstart", link: "/guide/installation" },
          { text: "Docker & Compose", link: "/docker" },
          { text: "Troubleshooting Guide", link: "/troubleshooting" },
          { text: "Frequently Asked Questions", link: "/faq" },
        ],
      },
      {
        text: "AI & LLM Integration",
        collapsed: false,
        items: [
          { text: "Free Gemini Setup", link: "/free-gemini-setup" },
          { text: "Gemini Deep Dive", link: "/gemini-integration" },
          { text: "Feed Sources Management", link: "/sources" },
          { text: "Prompt Tuning & Parameters", link: "/tuning" },
        ],
      },
      {
        text: "Core Modules & Architecture",
        collapsed: false,
        items: [
          { text: "main.py (Orchestrator)", link: "/main.py" },
          { text: "llm_processor.py (Inference)", link: "/llm_processor.py" },
          { text: "rss_reader.py (Feed Ingestion)", link: "/rss_reader.py" },
          { text: "similarity_checker.py (Deduplication)", link: "/similarity_checker.py" },
          { text: "json_manager.py (State & Cache)", link: "/json_manager.py" },
          { text: "json2rss.py (XML Publisher)", link: "/json2rss.py" },
        ],
      },
      {
        text: "Evaluation & Benchmarks",
        collapsed: false,
        items: [
          { text: "Metrics Overview", link: "/metrics" },
          { text: "Batch Metrics Evaluation", link: "/process_multiple_metrics.py" },
          { text: "Evaluate Against Reference", link: "/evaluate_against_reference.py" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/fabriziosalmi/UglyFeed" },
    ],

    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © Fabrizio Salmi",
    },
  },
})
