# 🆓 Free Gemini Models Quick Reference

## 🎯 Recommended Setup (100% Free!)

### 1. Get Your Free API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your key

### 2. Quick Configuration
```yaml
# In config.yaml
api_config:
  selected_api: "Gemini"
  gemini_api_key: "YOUR_API_KEY_HERE"
  gemini_model: "gemini-2.0-flash"  # ⭐ BEST FREE MODEL
```

### 3. Available FREE Models

| Model | Best For | Context | Speed |
|-------|----------|---------|-------|
| **`gemini-2.0-flash`** ⭐ | **General use (RECOMMENDED)** | 1M tokens | Fast |
| `gemini-2.0-flash-lite` | High-volume processing | Standard | Fastest |
| `gemini-1.5-flash` | Proven reliability | 1M tokens | Fast |
| `gemini-1.5-flash-8b` | Simple tasks | 1M tokens | Very Fast |
| `gemma-3` | Open source fans | Standard | Fast |
| `gemma-3n` | Edge/mobile devices | Standard | Very Fast |

### 4. One-Command Setup
```bash
# Start with the best free model
python main.py --api gemini --api_key "YOUR_KEY" --model "gemini-2.0-flash"
```

### 5. GitHub Actions (Free Automation)
Copy either workflow to `.github/workflows/`:
- `UglyFeed-GitHub-Action-Gemini-gemini-2.0-flash.yml` (recommended)
- `UglyFeed-GitHub-Action-Gemini-gemma-3.yml` (100% open source)

Add your API key as GitHub secret: `GEMINI_API_KEY`

---

## 🏆 Why Choose Free Gemini?

✅ **No credit card required**  
✅ **Generous rate limits**  
✅ **Latest AI technology**  
✅ **Perfect for RSS processing**  
✅ **1M+ token context window**  
✅ **Automatic rate limiting**  
✅ **Easy integration**  

---

## 🚀 Quick Start Command
```bash
# Clone and run with free Gemini
git clone https://github.com/fabriziosalmi/UglyFeed.git
cd UglyFeed
pip install -r requirements.txt
python main.py --api gemini --api_key "YOUR_KEY" --model "gemini-2.0-flash"
```

**That's it! You're now using cutting-edge AI for FREE! 🎉**
