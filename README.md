# MLBB Hero Analytics API and Website

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68)

## 🚨 URGENT: Service at Risk - Your Support Needed! 🚨

### ⚠️ **DISCONTINUATION NOTICE: July 10, 2025** ⚠️

**This free API service is at risk of being shut down!** 📉

Due to overwhelming traffic costs and zero financial backing, this popular MLBB analytics service will be **permanently discontinued on July 10, 2025** unless we receive community support.

### 💝 **Help Keep This Service Alive - We Need $50/Month, But You Can Start with Just $1!**

**Monthly Target: $50 USD** to cover essential costs, but **every contribution matters** - even $1 helps us get closer to our goal!

Your contribution directly helps:

- 🔧 Maintain server infrastructure
- 📊 Handle increasing API traffic
- 🌐 Keep ridwaanhall.com operational
- 🚀 Develop new features for the community

### 🎯 **Take Action Now!**

[![Become a Sponsor](https://img.shields.io/badge/💖%20Become%20a%20Sponsor-FF69B4?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/ridwaanhall/)
[![Buy Me a Coffee](https://img.shields.io/badge/☕%20Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](coff.ee/ridwaanhall)

**Every dollar counts!** Together, we can ensure this valuable resource remains available for the entire MLBB community. 🤝✨

---
*Don't let this service disappear - your support makes the difference!* 🙏

## Description

This project provides a comprehensive Django-based API and web interface for fetching various analytics and data related to heroes in the game Mobile Legends: Bang Bang (MLBB). The system includes secure URL encryption, RESTful API endpoints, and a modern web interface for hero rankings, positions, details, skill combinations, ratings, relationships, counter information, and compatibility.

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
