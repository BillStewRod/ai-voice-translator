# app.py - Flask backend with AI translation integration
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from datetime import datetime
import openai
import requests
import json

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_TRANSLATE_API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY')

# Initialize OpenAI client if API key is provided
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    """Serve the main HTML page"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Main translation endpoint"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'es')
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Try different translation methods in order of preference
        translation = None
        method_used = None
        
        # Method 1: OpenAI GPT (most accurate for context)
        if OPENAI_API_KEY and not translation:
            try:
                translation = translate_with_openai(text, source_lang, target_lang)
                method_used = 'OpenAI GPT'
            except Exception as e:
                print(f"OpenAI translation failed: {e}")
        
        # Method 2: Google Translate API (fast and reliable)
        if GOOGLE_TRANSLATE_API_KEY and not translation:
            try:
                translation = translate_with_google(text, source_lang, target_lang)
                method_used = 'Google Translate'
            except Exception as e:
                print(f"Google Translate failed: {e}")
        
        # Method 3: Fallback to LibreTranslate (free, self-hosted option)
        if not translation:
            try:
                translation = translate_with_libre(text, source_lang, target_lang)
                method_used = 'LibreTranslate'
            except Exception as e:
                print(f"LibreTranslate failed: {e}")
        
        # Method 4: Simple rule-based fallback
        if not translation:
            translation = simple_translate(text, source_lang, target_lang)
            method_used = 'Simple Fallback'
        
        return jsonify({
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'method': method_used,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def translate_with_openai(text, source_lang, target_lang):
    """Translate using OpenAI GPT API"""
    lang_names = {'es': 'Spanish', 'en': 'English'}
    
    prompt = f"""Translate the following {lang_names[source_lang]} text to {lang_names[target_lang]}. 
    Provide only the translation, no explanations or additional text.
    
    Text to translate: {text}
    
    Translation:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional translator. Provide accurate, natural translations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def translate_with_google(text, source_lang, target_lang):
    """Translate using Google Translate API"""
    url = "https://translation.googleapis.com/language/translate/v2"
    
    params = {
        'key': GOOGLE_TRANSLATE_API_KEY,
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    
    response = requests.post(url, data=params)
    response.raise_for_status()
    
    result = response.json()
    return result['data']['translations'][0]['translatedText']

def translate_with_libre(text, source_lang, target_lang):
    """Translate using LibreTranslate (free, open-source)"""
    # You can run your own LibreTranslate instance or use a public one
    url = "https://libretranslate.com/translate"
    
    payload = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    return result['translatedText']

def simple_translate(text, source_lang, target_lang):
    """Simple rule-based translation fallback"""
    translations = {
        'es-en': {
            'hola': 'hello',
            'buenos días': 'good morning',
            'buenas tardes': 'good afternoon',
            'buenas noches': 'good night',
            'gracias': 'thank you',
            'por favor': 'please',
            'adiós': 'goodbye',
            'sí': 'yes',
            'no': 'no',
            '¿cómo estás?': 'how are you?',
            'muy bien': 'very well',
            'lo siento': 'sorry',
            'disculpe': 'excuse me',
            'de nada': "you're welcome",
            'con permiso': 'excuse me',
            'buen día': 'good day'
        },
        'en-es': {
            'hello': 'hola',
            'good morning': 'buenos días',
            'good afternoon': 'buenas tardes',
            'good night': 'buenas noches',
            'thank you': 'gracias',
            'please': 'por favor',
            'goodbye': 'adiós',
            'yes': 'sí',
            'no': 'no',
            'how are you?': '¿cómo estás?',
            'very well': 'muy bien',
            'sorry': 'lo siento',
            'excuse me': 'disculpe',
            "you're welcome": 'de nada',
            'good day': 'buen día'
        }
    }
    
    key = f"{source_lang}-{target_lang}"
    text_lower = text.lower().strip()
    
    if key in translations and text_lower in translations[key]:
        return translations[key][text_lower]
    
    # If no direct translation found, return with indicator
    return f"[Translation needed: {text}]"

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'openai': bool(OPENAI_API_KEY),
            'google_translate': bool(GOOGLE_TRANSLATE_API_KEY)
        }
    })

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    return jsonify({
        'languages': [
            {'code': 'es', 'name': 'Spanish', 'flag': '🇪🇸'},
            {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
            {'code': 'fr', 'name': 'French', 'flag': '🇫🇷'},
            {'code': 'de', 'name': 'German', 'flag': '🇩🇪'},
            {'code': 'it', 'name': 'Italian', 'flag': '🇮🇹'},
            {'code': 'pt', 'name': 'Portuguese', 'flag': '🇵🇹'},
            {'code': 'zh', 'name': 'Chinese', 'flag': '🇨🇳'},
            {'code': 'ja', 'name': 'Japanese', 'flag': '🇯🇵'},
            {'code': 'ko', 'name': 'Korean', 'flag': '🇰🇷'},
            {'code': 'ar', 'name': 'Arabic', 'flag': '🇸🇦'}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)