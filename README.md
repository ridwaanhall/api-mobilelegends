# Mobile Legends API

A professional FastAPI-based REST API for Mobile Legends Bang Bang hero data, statistics, and analytics.

## 🚀 Features

- **Hero Management**: Complete hero list, details, and statistics
- **Rank Analysis**: Hero performance across different ranks
- **Position Analysis**: Heroes filtered by role and lane
- **Statistics**: Win rates, pick rates, ban rates, and more
- **Relations**: Hero counters and compatibility
- **Win Rate Calculator**: Calculate required matches to achieve target win rate
- **Multi-language Support**: API responses in multiple languages
- **Comprehensive Documentation**: OpenAPI/Swagger and ReDoc

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Development](#️-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🔧 Installation

### Prerequisites

- Python 3.12+
- pip or conda

### Setup

1. Clone the repository:

```bash
git clone https://github.com/ridwaanhall/api-mobilelegends.git
cd api-mobilelegends
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Configure your environment variables in `.env` (see [Configuration](#configuration))

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# API Configuration
API_VERSION=2.0.0
IS_AVAILABLE=True
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here

# External Services
MLBB_URL=https://your-mlbb-api-url.com
PROD_URL=https://your-production-url.com

# Optional: Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_VERSION` | API version number | `2.0.0` | No |
| `IS_AVAILABLE` | Enable/disable API endpoints | `True` | No |
| `DEBUG` | Enable debug mode | `False` | No |
| `SECRET_KEY` | Secret key for encryption | - | Yes |
| `MLBB_URL` | MLBB API base URL | - | Yes |
| `PROD_URL` | Production URL | - | Yes (if not DEBUG) |

## 🚀 Usage

### Running Locally

Development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker build -t mlbb-api .
docker run -p 8000:8000 --env-file .env mlbb-api
```

## 📚 API Endpoints

### Base URLs

- **Production**: `https://mlbb-stats.ridwaanhall.com/api/`
- **Local Development**: `http://localhost:8000/api/`

### Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

### Available Endpoints

#### General

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint

#### Hero Endpoints

- `GET /api/hero-list/` - Get complete hero list
- `GET /api/hero-rank/` - Get hero rankings by win rate, pick rate, ban rate
- `GET /api/hero-position/` - Get heroes by role and lane
- `GET /api/hero-detail/{hero_id}` - Get detailed hero information
- `GET /api/hero-detail-stats/{main_heroid}` - Get hero statistics
- `GET /api/hero-skill-combo/{hero_id}` - Get hero skill combo information
- `GET /api/hero-rate/{main_heroid}` - Get hero rate over time
- `GET /api/hero-relation/{hero_id}` - Get hero relation information
- `GET /api/hero-counter/{main_heroid}` - Get hero counter information
- `GET /api/hero-compatibility/{main_heroid}` - Get hero compatibility

#### Utility Endpoints

- `GET /api/win-rate/` - Calculate required matches to reach target win rate

### Query Parameters

Most endpoints support these common parameters:

- `lang` - Language code (default: `en`)
- `size` - Page size for pagination (default: `20`)
- `index` - Page index (default: `1`)

## 🛠️ Development

### Project Structure

```txt
api-mobilelegends/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── heroes.py
│   │   │   │   ├── stats.py
│   │   │   │   └── utils.py
│   │   │   └── api.py
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   ├── security.py        # Security utilities
│   │   └── logging.py         # Logging setup
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── hero.py
│   │   ├── stats.py
│   │   └── response.py
│   ├── schemas/               # Request/Response schemas
│   │   ├── __init__.py
│   │   └── api.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── mlbb_service.py
│   │   └── calculation_service.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── crypto.py
│       └── http_client.py
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
├── docs/                      # Additional documentation
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── vercel.json
```

### Code Style

This project follows:

- PEP 8 style guide
- Type hints for all functions
- Docstrings for all modules, classes, and functions
- Maximum line length: 100 characters

### Linting and Formatting

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Check types
mypy app/

# Lint
flake8 app/ tests/
pylint app/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_heroes.py

# Run with verbose output
pytest -v
```

### Writing Tests

Tests are located in the `tests/` directory. Follow the same structure as the `app/` directory.

## 🚢 Deployment

### Vercel

This project is configured for Vercel deployment:

```bash
vercel deploy
```

### Docker

```bash
# Build image
docker build -t mlbb-api:latest .

# Run container
docker run -d -p 8000:8000 --env-file .env mlbb-api:latest
```

### Environment Variables

Ensure all required environment variables are set in your deployment platform.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Write clear, descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Follow the existing code style
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**ridwaanhall**

- GitHub: [@ridwaanhall](https://github.com/ridwaanhall)
- Website: [ridwaanhall.com](https://ridwaanhall.com)

## 💖 Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 💝 [Sponsoring the project](https://github.com/sponsors/ridwaanhall)
- 🐛 Reporting bugs
- 📝 Contributing to documentation

**Support Goal**: Help us reach $500 USD to enhance API performance and handle high request volumes.

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/ridwaanhall/api-mobilelegends/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ridwaanhall/api-mobilelegends/discussions)

## 🙏 Acknowledgments

- Mobile Legends Bang Bang for the game data
- FastAPI for the amazing framework
- All contributors and supporters

---

**Note**: This API is not officially affiliated with Mobile Legends Bang Bang or Moonton.
