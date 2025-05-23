# 🌐 AI Voice Translator

A sophisticated real-time translation app with voice input/output capabilities, powered by AI and designed for cloud deployment.

## Features

- 🎤 **Voice Input**: Speech-to-text in multiple languages
- 🔊 **Audio Output**: Text-to-speech with natural voices
- 🤖 **AI-Powered**: Multiple translation backends (OpenAI, Google Translate, LibreTranslate)
- ⚡ **Real-time**: Instant translation with live mode
- 🌍 **Multi-language**: Support for 10+ languages
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🐳 **Docker Ready**: Easy deployment with Docker and Docker Compose
- 🔒 **Secure**: HTTPS, security headers, and best practices

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-voice-translator.git
   cd ai-voice-translator
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - HTTP: `http://your-server-ip`
   - HTTPS: `https://your-domain.com` (after SSL setup)

## Configuration

### API Keys

The app supports multiple translation services:

- **OpenAI API**: Most accurate, context-aware translations
  ```bash
  OPENAI_API_KEY=your-openai-api-key
  ```

- **Google Translate API**: Fast and reliable
  ```bash
  GOOGLE_TRANSLATE_API_KEY=your-google-api-key
  ```

- **LibreTranslate**: Free, open-source option (no API key needed)

### SSL Setup

For production deployment:

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Place certificates in the `ssl/` directory
3. Update `nginx.conf` with your domain name

## API Endpoints

- `GET /` - Main application interface
- `POST /api/translate` - Translation endpoint
- `GET /api/health` - Health check
- `GET /api/languages` - Supported languages

## Deployment on Proxmox

1. **Create a new LXC container or VM**
   - Ubuntu 22.04 LTS recommended
   - Minimum 2GB RAM, 20GB storage

2. **Install Docker and Docker Compose**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Clone and deploy**
   ```bash
   git clone https://github.com/yourusername/ai-voice-translator.git
   cd ai-voice-translator
   docker-compose up -d
   ```

4. **Set up reverse proxy** (optional)
   - Configure your existing Nginx Proxy Manager
   - Or use the included Nginx configuration

## Browser Compatibility

- Chrome/Chromium 60+ (recommended for voice features)
- Firefox 55+
- Safari 11+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- 📖 Documentation: Check the wiki
- 🐛 Bug reports: Open an issue
- 💡 Feature requests: Open a discussion

---

**Made with ❤️ for seamless global communication**