import json
import re
import os
import argparse
import yaml
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv
from logging_setup import setup_logging, get_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'(?<=[.,;!?])', ' ', text)
    logger.debug(f"Preprocessed text: {text}")
    return text

# Function to synthesize speech from text
def synthesize_speech(text, lang, speed_factor, output_path):
    preprocessed_text = preprocess_text(text)
    tts = gTTS(text=preprocessed_text, lang=lang, slow=False)
    temp_output_path = "temp_output.mp3"
    tts.save(temp_output_path)
    audio = AudioSegment.from_file(temp_output_path)
    faster_audio = audio.speedup(playback_speed=speed_factor)
    faster_audio.export(output_path, format="mp3")
    os.remove(temp_output_path)
    logger.info(f"Saved synthesized speech to {output_path}")

def process_json_files(tts_input, tts_output, tts_language, speed_factor, enable_tts):
    if not os.path.exists(tts_output):
        os.makedirs(tts_output)
        logger.debug(f"Created output directory: {tts_output}")
    for filename in os.listdir(tts_input):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(tts_input, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    text_to_synthesize = data["content"]
                    output_path = os.path.join(tts_output, filename.replace('.json', '.mp3'))
                    if enable_tts:
                        synthesize_speech(text_to_synthesize, tts_language, speed_factor, output_path)
                        logger.info(f"Processed {filename}, saved to {output_path}")
                    else:
                        logger.info(f"TTS disabled. Skipped processing {filename}")
            except Exception as e:
                logger.error(f"Failed to process {filename}: {e}")

def load_config():
    try:
        with open("config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
        logger.debug(f"Loaded configuration: {config}")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration file: {e}")
        raise

def main():
    config = load_config()

    parser = argparse.ArgumentParser(description='Process JSON files and generate TTS MP3 files.')
    parser.add_argument('--tts_input', default=os.getenv('TTS_INPUT', config['tts_input']))
    parser.add_argument('--tts_output', default=os.getenv('TTS_OUTPUT', config['tts_output']))
    parser.add_argument('--tts_language', default=os.getenv('TTS_LANGUAGE', config['tts_language']))
    parser.add_argument('--speed_factor', type=float, default=float(os.getenv('SPEED_FACTOR', config['speed_factor'])))
    parser.add_argument('--enable_tts', type=bool, default=(os.getenv('ENABLE_TTS', str(config['enable_tts'])).lower() == 'true'))

    args = parser.parse_args()

    logger.info("Starting JSON processing with the following settings:")
    logger.info(f"TTS Input Directory: {args.tts_input}")
    logger.info(f"TTS Output Directory: {args.tts_output}")
    logger.info(f"TTS Language: {args.tts_language}")
    logger.info(f"Speed Factor: {args.speed_factor}")
    logger.info(f"Enable TTS: {args.enable_tts}")

    process_json_files(
        tts_input=args.tts_input,
        tts_output=args.tts_output,
        tts_language=args.tts_language,
        speed_factor=args.speed_factor,
        enable_tts=args.enable_tts
    )

if __name__ == "__main__":
    main()
