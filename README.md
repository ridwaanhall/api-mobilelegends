# MLBB Hero Analytics API and Website

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/6f380e9e-ea7b-4326-8ec2-df979927fe68)

This project provides an API for fetching various analytics and data related to heroes in the game Mobile Legends: Bang Bang (MLBB). The API includes endpoints for hero rankings, positions, details, skill combinations, ratings, relationships, counter information, and compatibility.

![Hero Rank Web](images/hero-rank.png)

## Summary of API Docs, APIs, and Website.

```txt
https://api-mobilelegends.vercel.app/api/"       # for testing an api
https://mlbb-api-docs.vercel.app/"               # for read the documentations easy-to-understand
https://api-mobilelegends.vercel.app/hero-rank/" # for website demo of APIs
```

## Table of Contents

- Endpoints
  - [Hero Rank](#hero-rank)
  - [Hero Position](#hero-position)
  - [Hero Detail](#hero-detail)
  - [Hero Detail Stats](#hero-detail-stats)
  - [Hero Skill Combo](#hero-skill-combo)
  - [Hero Rate](#hero-rate)
  - [Hero Relation](#hero-relation)
  - [Hero Counter](#hero-counter)
  - [Hero Compatibility](#hero-compatibility)
- Setup
- Usage
- License

## Endpoints

The base URL for all endpoints is `https://api-mobilelegends.vercel.app`.

```text
https://api-mobilelegends.vercel.app
```

### Hero Rank

**Endpoint:** `GET /hero-rank/`

**Description:** Fetch hero rankings based on various parameters such as days, rank, page size, page index, and sorting options.

**Query Parameters:**

- `days` (optional): Number of days for which the data is to be fetched. Possible values: `1`, `3`, `7`, `15`, `30`. Default: `1`.
- `rank` (optional): Rank category for filtering the data. Possible values: `all`, `epic`, `legend`, `mythic`, `honor`, `glory`. Default: `all`.
- `size` (optional): Number of records per page. Default: `20`.
- `index` (optional): Page index for pagination. Default: `1`.
- `sort_field` (optional): Field by which the data should be sorted. Possible values: `pick_rate`, `ban_rate`, `win_rate`. Default: `win_rate`.
- `sort_order` (optional): Order of sorting. Possible values: `asc`, `desc`. Default: `desc`.

**Example Request:**

```text
GET /hero-rank/?days=7&rank=mythic&size=10&index=2&sort_field=pick_rate&sort_order=asc
```

### Hero Position

**Endpoint:** `GET /hero-position/`

**Description:** Fetch hero positions based on various parameters such as role, lane, page size, and page index.

**Query Parameters:**

- `role` (optional): Role category for filtering the data. Possible values: `all`, `tank`, `fighter`, `ass`, `mage`, `mm`, `supp`. Default: `all`.
- `lane` (optional): Lane category for filtering the data. Possible values: `all`, `exp`, `mid`, `roam`, `jungle`, `gold`. Default: `all`.
- `size` (optional): Number of records per page. Default: `21`.
- `index` (optional): Page index for pagination. Default: `1`.

**Example Request:**

```text
GET /hero-position/?role=tank&lane=mid&size=10&index=2
```

### Hero Detail

**Endpoint:** `GET /hero-detail/<int:hero_id>/`

**Description:** Display details of a specific hero identified by `hero_id`.

**Path Parameters:**

- `hero_id`: The ID of the hero whose details are to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-detail/123/
```

### Hero Detail Stats

**Endpoint:** `GET /hero-detail-stats/<int:main_heroid>/`

**Description:** Display detailed statistics of a specific hero identified by `main_heroid`.

**Path Parameters:**

- `main_heroid`: The ID of the main hero whose detailed statistics are to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-detail-stats/123/
```

### Hero Skill Combo

**Endpoint:** `GET /hero-skill-combo/<int:hero_id>/`

**Description:** Display skill combinations of a specific hero identified by `hero_id`.

**Path Parameters:**

- `hero_id`: The ID of the hero whose skill combinations are to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-skill-combo/123/
```

### Hero Rate

**Endpoint:** `GET /hero-rate/<int:main_heroid>/`

**Description:** Rate a specific hero identified by `main_heroid`.

**Path Parameters:**

- `main_heroid`: The ID of the main hero whose rating is to be fetched. Type: `integer`. Required: `true`.

**Query Parameters:**

- `past-days` (optional): Number of past days for which the data is to be fetched. Possible values: `7`, `15`, `30`. Default: `7`.

**Example Request:**

```text
GET /hero-rate/123/?past-days=15
```

### Hero Relation

**Endpoint:** `GET /hero-relation/<int:hero_id>/`

**Description:** Display relationships of a specific hero identified by `hero_id`.

**Path Parameters:**

- `hero_id`: The ID of the hero whose relationships are to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-relation/123/
```

### Hero Counter

**Endpoint:** `GET /hero-counter/<int:main_heroid>/`

**Description:** Display counter information of a specific hero identified by `main_heroid`.

**Path Parameters:**

- `main_heroid`: The ID of the main hero whose counter information is to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-counter/123/
```

### Hero Compatibility

**Endpoint:** `GET /hero-compatibility/<int:main_heroid>/`

**Description:** Display compatibility information of a specific hero identified by `main_heroid`.

**Path Parameters:**

- `main_heroid`: The ID of the main hero whose compatibility information is to be fetched. Type: `integer`. Required: `true`.

**Example Request:**

```text
GET /hero-compatibility/123/
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mlbb-hero-analytics-api.git
   cd mlbb-hero-analytics-api
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Django settings:
   - Update the `MLBB_URL` in your `settings.py` file with the appropriate URL.

5. Run the Django development server:

   ```bash
   python manage.py runserver
   ```

## Usage

Use the provided endpoints to fetch various analytics and data related to heroes in MLBB. Refer to the Endpoints section for detailed information on each endpoint and how to use them.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
