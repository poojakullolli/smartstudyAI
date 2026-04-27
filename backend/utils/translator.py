from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

def translate_text(text: str, target_lang: str):
    """
    Translates text using deep-translator (no API key required).
    Falls back to original text on failure.
    """
    try:
        if not text or target_lang == "en":
            return text
        
        # Mapping Karnataka to 'kn' and others to their ISO codes if needed
        # GoogleTranslator uses ISO 639-1 codes
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        logger.error(f"Deep Translation failed: {str(e)}")
        return text
