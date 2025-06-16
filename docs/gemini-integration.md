# Google Gemini Int### 3. Supported Models (Free Tier Available!)

#### Free Tier Models (No cost!)
- **`gemini-2.0-flash`** ⭐ **RECOMMENDED** - Latest and most balanced model with excellent performance
- **`gemini-2.0-flash-lite`** - Smaller, faster model for high-volume processing
- **`gemini-1.5-flash`** - Proven fast model with 1M token context window
- **`gemini-1.5-flash-8b`** - Smallest model for simple tasks
- **`gemma-3`** - Open source model, completely free
- **`gemma-3n`** - Efficient model for edge devices

#### Paid Tier Models
- `gemini-2.5-flash-preview` - Preview model with reasoning capabilities
- `gemini-2.5-pro-preview` - Highest intelligence model
- `gemini-1.5-pro` - High intelligence with 2M token context

> **💡 Tip**: Start with `gemini-2.0-flash` - it's completely free and offers excellent performance!tion for UglyFeed

## Overview
Google Gemini AI support has been successfully added to UglyFeed, providing access to Google's advanced language models for content processing and rewriting.

## Features Added

### 1. Gemini API Client
- **Full Gemini API integration** with proper error handling and retry logic
- **Content truncation** to handle token limits
- **Rate limiting support** with automatic retry
- **Proper response parsing** for Gemini's unique response format

### 2. Configuration Support
- **GUI Integration**: Added Gemini as an option in the Streamlit interface
- **Config file support**: Example configuration in `config.yaml`
- **Environment variable support**: Can be configured via environment variables
- **CLI support**: Command-line interface supports Gemini parameters

## Configuration

### Via config.yaml
```yaml
api_config:
  selected_api: "Gemini"
  gemini_api_url: "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
  gemini_api_key: "your_gemini_api_key"
  gemini_model: "gemini-2.0-flash"  # Free tier model!
```

### Via Environment Variables
```bash
export API_TYPE="gemini"
export API_KEY="your_gemini_api_key"
export API_MODEL="gemini-2.0-flash"
export API_URL="https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
```

### Via Command Line
```bash
python llm_processor.py --api gemini \
                       --api_key "your_gemini_api_key" \
                       --model "gemini-2.0-flash" \
                       --api_url "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
```

## Getting Started

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in UglyFeed

### 2. Configure UglyFeed
Choose one of the configuration methods above and add your API key.

### 3. Run UglyFeed
- **GUI**: Select "Gemini" from the API dropdown in the Streamlit interface
- **CLI**: Use the command-line parameters shown above
- **Automated**: Use the provided GitHub Action workflow

## GitHub Actions Integration
A ready-to-use GitHub Actions workflow is available at:
`docs/UglyFeed-GitHub-Action-Gemini-gemini-2.0-flash.yml`

This workflow uses the **free tier** `gemini-2.0-flash` model.

To use it:
1. Add your Gemini API key as a GitHub secret named `GEMINI_API_KEY`
2. Copy the workflow to `.github/workflows/` in your repository
3. The workflow will run every 4 hours automatically using the free tier

## Technical Details

### API Implementation
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- **Authentication**: API key passed as query parameter
- **Request Format**: JSON with `contents` array
- **Response Format**: JSON with `candidates` array containing generated content

### Error Handling
- **Rate limiting**: Automatic retry with exponential backoff
- **API errors**: Comprehensive error logging with response details
- **Network issues**: Robust retry mechanism with session management
- **Content validation**: Proper response parsing with fallback handling

### Token Management
- **Content truncation**: Automatically truncates content to fit within token limits
- **Token estimation**: Rough estimation for content length management
- **Configurable limits**: Adjustable maximum token limits via configuration

## Troubleshooting

### Common Issues
1. **"API key not provided"**: Ensure your API key is properly set in configuration
2. **"Model not found"**: Verify the model name is correct (e.g., "gemini-1.5-flash")
3. **"Rate limit exceeded"**: The system will automatically retry, or wait a few minutes

### Validation
The system includes comprehensive validation:
- API key presence check
- Model name validation
- URL format verification
- Response structure validation

## Migration from Other APIs
Switching from other APIs to Gemini is seamless:
1. Change `selected_api` to "Gemini" in config.yaml
2. Add Gemini-specific configuration parameters
3. Remove or comment out previous API configuration
4. Restart UglyFeed

## Performance Notes
- **gemini-2.0-flash**: ⭐ **FREE & RECOMMENDED** - Best balance of speed and quality
- **gemini-2.0-flash-lite**: **FREE** - Fastest response times, good for high-volume processing  
- **gemini-1.5-flash**: **FREE** - Proven performance with 1M token context
- **gemini-1.5-flash-8b**: **FREE** - Most efficient for simple tasks
- **gemma-3/gemma-3n**: **COMPLETELY FREE** - Open source models
- Rate limits: Gemini free tier has generous limits with automatic handling

## Cost Benefits
🎉 **All recommended models are completely FREE!**
- No credit card required for free tier
- Generous rate limits for development and small-scale production
- Perfect for RSS feed processing and content rewriting
- Data used to improve Google products (standard for free tier)

## Security
- API keys are never logged or exposed in output
- HTTPS-only communication with Google's servers
- Proper error handling prevents sensitive data leakage
