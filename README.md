# MLBB Hero Analytics API and Website

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68)

## 🌟 Your Support Means the World! Start from 1 USD

Are you interested in the project I created and want to help keep it running? You can support me by becoming a sponsor! Your contributions will greatly assist in the development and maintenance of this project.

[![Sponsor Me](https://img.shields.io/badge/-Sponsor%20Me-blue?style=for-the-badge)](https://github.com/sponsors/ridwaanhall/)

Thank you for supporting my work! Together, we can create something amazing. 🚀

## Description

This project provides a comprehensive Django-based API and web interface for fetching various analytics and data related to heroes in the game Mobile Legends: Bang Bang (MLBB). The system includes secure URL encryption, RESTful API endpoints, and a modern web interface for hero rankings, positions, details, skill combinations, ratings, relationships, counter information, and compatibility.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ridwaanhall/api-mobilelegends.git
   cd api-mobilelegends
   ```

2. **Create and activate virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   Create a `.env` file in the root directory:

   ```env
   # Django Settings - REQUIRED!
   SECRET_KEY=your-very-long-secret-key-here-make-it-random-and-secure
   
   # Debug Mode (True for development, False for production)
   DEBUG=True
   
   # Production URL Configuration
   # For development (using your local API):
   PROD_URL=http://localhost:8000/api/
   
   # For production (using external API - default):
   # PROD_URL=https://mlbb-stats.ridwaanhall.com/api/
   
   # Database (Optional - uses SQLite by default)
   # DATABASE_URL=sqlite:///db.sqlite3
   ```

   **Important Notes:**
   - `SECRET_KEY` is **required** and has no default value
   - `DEBUG=True` enables development mode with unrestricted hosts
   - `DEBUG=False` enables production mode with restricted hosts
   - `PROD_URL` defaults to the external API if not specified

5. **Database Migration**

   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/`
   The web interface will be available at `http://localhost:8000/`

## ⚙️ Important Configuration

### 🌐 ALLOWED_HOSTS Configuration

The `ALLOWED_HOSTS` setting is automatically managed based on the `DEBUG` setting:

**Development Mode (`DEBUG=True`):**

- `ALLOWED_HOSTS = []` (allows all hosts - automatic Django behavior)
- Perfect for local development

**Production Mode (`DEBUG=False`):**

- `ALLOWED_HOSTS` is restricted to specific domains:

  ```python
  ALLOWED_HOSTS = [
      '.vercel.app',
      '.ridwaanhall.me', 
      '.ridwaanhall.com',
  ]
  ```

**To modify allowed hosts for your domain:**

1. Edit `MLBB/settings.py`
2. Update the `ALLOWED_HOSTS` list in the `else` block
3. Add your domain (e.g., `'your-domain.com'`, `'.your-domain.com'`)

### 🔗 PROD_URL Configuration

The `PROD_URL` setting determines where the web interface fetches API data from. It has a default value but can be overridden via environment variables:

**Default Behavior (External API):**

- Uses: `https://mlbb-stats.ridwaanhall.com/api/`
- No `.env` configuration needed

**For Self-Referencing (Local Development):**

```env
PROD_URL=http://localhost:8000/api/
```

**For Self-Referencing (Production):**

```env
PROD_URL=https://your-domain.com/api/
```

**For External API (Custom):**

```env
PROD_URL=https://external-api-server.com/api/
```

## 📚 API Documentation & Demo

### Live Demo URLs

```txt
https://mlbb-stats.ridwaanhall.com/                # Base URL
https://mlbb-stats-docs.ridwaanhall.com/           # API Documentation
https://mlbb-stats.ridwaanhall.com/api/            # API Testing Interface
https://mlbb-stats.ridwaanhall.com/hero-rank/      # Web Demo Interface
```

### API Docs with Explanations and Example Usage

[https://mlbb-stats-docs.ridwaanhall.com/](https://mlbb-stats-docs.ridwaanhall.com/)

![API Docs](images/api-docs.png)

### Testing an API [Visit API Testing Interface](https://mlbb-stats.ridwaanhall.com/api/)

### Demo Website [View Hero Rankings Demo](https://mlbb-stats.ridwaanhall.com/hero-rank/)

![Hero Rank Web](images/demo-website.png)

## 🔧 Available API Endpoints

The API provides comprehensive MLBB hero analytics through the following endpoints:

- **Hero Rank** - `/api/hero-rank/` - Get hero rankings by various criteria
- **Hero Position** - `/api/hero-position/` - Get hero position analytics
- **Hero Detail** - `/api/hero-detail/{hero_id}/` - Get detailed hero information
- **Hero Detail Stats** - `/api/hero-detail-stats/{hero_id}/` - Get hero statistics
- **Hero Skill Combo** - `/api/hero-skill-combo/{hero_id}/` - Get hero skill combinations
- **Hero Rate** - `/api/hero-rate/{hero_id}/` - Get hero win/pick rates
- **Hero Relation** - `/api/hero-relation/{hero_id}/` - Get hero relationships
- **Hero Counter** - `/api/hero-counter/{hero_id}/` - Get hero counter information
- **Hero Compatibility** - `/api/hero-compatibility/{hero_id}/` - Get hero compatibility data

## 🚀 Deployment

### Development Deployment

1. Follow the installation steps above
2. Set `DEBUG=True` in your `.env` file
3. Use `ALLOWED_HOSTS=localhost,127.0.0.1`
4. Use `PROD_URL=http://localhost:8000/api/`

### Production Deployment

1. **Security Settings**

   ```env
   DEBUG=False
   SECRET_KEY=your-secure-production-secret-key
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   PROD_URL=https://your-domain.com/api/
   ```

2. **Static Files**

   ```bash
   python manage.py collectstatic
   ```

3. **Web Server Configuration**
   - Configure your web server (Nginx, Apache) to serve static files
   - Set up HTTPS certificates
   - Configure reverse proxy to Django application

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🔒 Security Considerations

- **Environment Variables**: Use `.env` file for sensitive configuration
- **ALLOWED_HOSTS**: Properly configure allowed hosts for production
- **DEBUG**: Always set `DEBUG=False` in production
- **HTTPS**: Use HTTPS in production environments
- **Secret Key**: Use a strong, unique secret key for production

## 🐛 Troubleshooting

### Common Issues

1. **ImportError: No module named 'cryptography'**

   ```bash
   pip install cryptography
   ```

2. **KeyError: 'SECRET_KEY'**
   - The `SECRET_KEY` environment variable is required
   - Create a `.env` file with: `SECRET_KEY=your-secret-key-here`
   - Generate a secure key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

3. **DisallowedHost error**
   - Check if `DEBUG=True` in your `.env` for development
   - For production (`DEBUG=False`), add your domain to `ALLOWED_HOSTS` in `MLBB/settings.py`

4. **API endpoints not working**
   - Verify `PROD_URL` is correctly set in `.env` or using the default
   - Check if the Django server is running
   - Ensure the `/api/` path is accessible

5. **Static files not loading**

   ```bash
   python manage.py collectstatic
   ```

## 📞 Support & Discussion

If you have any questions or would like to discuss this project, please join the conversation in our [GitHub Discussions](https://github.com/ridwaanhall/api-mobilelegends/discussions). We value your feedback and are here to help!

## License

This project follows the **BSD 3-Clause License**. Please refer to [LICENSE](https://github.com/ridwaanhall/api-mobilelegends/blob/main/LICENSE) for details.

## Attribution

Special thanks to **Moonton** for developing **Mobile Legends: Bang Bang**. All rights to the game and its assets belong to **Moonton**.

## Source

For more information about **Mobile Legends: Bang Bang**, visit the official website: [Mobile Legends](https://www.mobilelegends.com).

## Disclaimer

This project is an independent redistribution of the **Mobile Legends: Bang Bang API** developed by **Moonton**. The purpose of this project is to make accessing the API easier through custom code and implementation.

By using this code, you **must** adhere to the following conditions:

1. **License Compliance** – Users must follow the **BSD 3-Clause License** terms, including proper attribution and distribution policies. See [LICENSE](https://github.com/ridwaanhall/api-mobilelegends/blob/main/LICENSE) for details.
2. **Attribution Requirement** – Users **must** mention both:
   - **Moonton** as the developer and publisher of **Mobile Legends: Bang Bang**.
   - **ridwaanhall** as the creator of this MLBB Stats.
3. **Visibility of Attribution** – The attribution to **Moonton** and **ridwaanhall** must be clearly visible in any public-facing project or website that utilizes this API.
4. **Independent Project** – This project is **not affiliated, endorsed, or officially supported** by **Moonton**. All rights to **Mobile Legends: Bang Bang** and its assets belong to **Moonton**.

Failure to comply with these terms may result in **restriction from using this code**.

For more information, please visit [Mobile Legends](https://www.mobilelegends.com/) and [ridwaanhall’s GitHub](https://github.com/ridwaanhall/api-mobilelegends).
