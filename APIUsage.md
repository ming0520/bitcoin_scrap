# scrapperE\scrap\views.py Usage Documentation

## Overview

The `scrapperE\scrap\views.py` file is responsible for handling the request/response logic for your Django application.

## Endpoints

### Endpoint: Scrap Today

**URL:** `scrap/scrap_today/`

**Method:** `GET`

**Description:** This endpoint scrapes the top 100 hot submissions from specified Bitcoin-related subreddits and saves them to the database if they were posted today.

**Parameters:** None

**Response:** An HTTP response with the message "Hello, World!".

**Details:**

This function uses the PRAW (Python Reddit API Wrapper) to interact with Reddit's API. It scrapes the top 100 hot submissions from the subreddits 'CryptoCurrencyTrading', 'btc', 'BitcoinBeginners', and 'Bitcoin'. 

For each submission, it checks if the post was created today and if it doesn't already exist in the database. If both conditions are met, it saves the post to the `PostRaw` model in the database. If an exception occurs during this process, it saves the error message and the post ID to the `ErrorPost` model.

**Example:**

Request: GET /scrap_today/
Response: Hello, World!

---

### Endpoint: Bitcoin Hourly Data

**URL:** `scrap/bitcoin_hourly_data/`

**Method:** `GET`

**Description:** This endpoint returns all OHLC (Open, High, Low, Close) Bitcoin data on an hourly basis.

**Parameters:**

- No parameters required for this endpoint.

**Response:**

A successful response returns an array of Bitcoin OHLC data. Each object in the array represents one hour of data and contains the following fields:

- `date`: The date and time of the data point, in ISO 8601 format, Malaysia timezone.
- `open`: The opening price of Bitcoin at the start of the hour.
- `high`: The highest price of Bitcoin during the hour.
- `low`: The lowest price of Bitcoin during the hour.
- `close`: The closing price of Bitcoin at the end of the hour.
- `volume_btc`: The volume of Bitcoin traded during the hour.
- `volume_usd`: The volume of trades in USD during the hour.

### Endpoint: Save Bitstamp Hourly Data

**URL:** `scrap/save_bitstamp_hourly/`

**Method:** `GET`

**Description:** This endpoint triggers the saving of hourly data from the Bitstamp API.

**Parameters:** None

**Response:** A response indicating that the Bitstamp API hourly data has been triggered.

**Example:**

Request: GET /save_bitstamp_hourly/

Response: Triggered Bitstamp API hourly data


---

### Endpoint: Save Bitstamp Daily Data

**URL:** `scrap/save_bitstamp_daily/`

**Method:** `GET`

**Description:** This endpoint triggers the saving of daily data from the Bitstamp API.

**Parameters:** None

**Response:** A response indicating that the Bitstamp API daily data has been triggered.

**Example:**

Request: 
```json
POST /scrap/add_bitstampminute/ Body: { "unix": 1633027200, "date": "2021-09-30T23:00:00Z", "symbol": "btcusd", "open": 44000.00, "high": 44100.00, "low": 43900.00, "close": 44050.00, "volume_btc": 10.00, "volume_usd": 440500.00 }
```

Response:
```json
{
    "unix": 1633027200,
    "date": "2021-09-30T23:00:00Z",
    "local_date": "2021-09-30T23:00:00Z",
    "symbol": "btcusd",
    "open": 44000.00,
    "high": 44100.00,
    "low": 43900.00,
    "close": 44050.00,
    "volume_btc": 10.00,
    "volume_usd": 440500.00,
    "added_at": "2021-09-30T23:00:00Z"
}
```

---


### Endpoint: Add Bitstamp Hourly Data

**URL:** `/add_bitstamphour/`

**Method:** `POST`

**Description:** This endpoint adds Bitstamp data for an hour.

**Parameters:** The request body should contain the following data:

- `unix`: Integer representing Unix timestamp.
- `date`: DateTime object representing the date.
- `symbol`: String representing the symbol.
- `open`: Decimal representing the opening price.
- `high`: Decimal representing the highest price.
- `low`: Decimal representing the lowest price.
- `close`: Decimal representing the closing price.
- `volume_btc`: Decimal representing the volume in BTC.
- `volume_usd`: Decimal representing the volume in USD.

**Response:** If the data is valid, it returns the serialized data of the newly created entry. If the data is invalid, it returns the errors from the serializer.

**Error Handling:** If the data is invalid, the function will return an HTTP response with the serializer errors.

**Example:**

Request: 
```json
POST /scrap/add_bitstampminute/ Body: { "unix": 1633027200, "date": "2021-09-30T23:00:00Z", "symbol": "btcusd", "open": 44000.00, "high": 44100.00, "low": 43900.00, "close": 44050.00, "volume_btc": 10.00, "volume_usd": 440500.00 }
```

Response:
```json
{
    "unix": 1633027200,
    "date": "2021-09-30T23:00:00Z",
    "local_date": "2021-09-30T23:00:00Z",
    "symbol": "btcusd",
    "open": 44000.00,
    "high": 44100.00,
    "low": 43900.00,
    "close": 44050.00,
    "volume_btc": 10.00,
    "volume_usd": 440500.00,
    "added_at": "2021-09-30T23:00:00Z"
}
```

---

### Endpoint: Add Bitstamp Minute Data

**URL:** `/add_bitstampminute/`

**Method:** `POST`

**Description:** This endpoint adds a new Bitstamp minute data entry.

**Parameters:** The request body should contain the following data:

- `unix`: Integer representing Unix timestamp.
- `date`: DateTime object representing the date.
- `symbol`: String representing the symbol.
- `open`: Decimal representing the opening price.
- `high`: Decimal representing the highest price.
- `low`: Decimal representing the lowest price.
- `close`: Decimal representing the closing price.
- `volume_btc`: Decimal representing the volume in BTC.
- `volume_usd`: Decimal representing the volume in USD.

**Response:** If the data is valid, it returns the serialized data of the newly created entry. If the data is invalid, it returns the errors from the serializer.

**Error Handling:** If the data is invalid, the function will return an HTTP response with the serializer errors.

**Example:**

Request: POST /add_bitstampminute/ Body: { ... }

Response: { "data": { ... } }

---

### Endpoint: Save Bitstamp Minutely Data

**URL:** `scrap/save_bitstamp_minutely/`

**Method:** `GET`

**Description:** This endpoint triggers the saving of minutely data from the Bitstamp API.

**Parameters:** None

**Response:** A response indicating that the Bitstamp API minutely data has been triggered.

**Example:**

Request: GET /save_bitstamp_daily/

Response: Triggered Bitstamp API daily data

---

### Endpoint: All Posts

**URL:** `/all_post/`

**Method:** `GET`

**Description:** This endpoint retrieves all posts from the database.

**Parameters:** None

**Response:** A JSON response containing all the posts. Each post is an object with the following properties:

- `id`: The unique identifier of the post.
- `post_id`: The post's ID.
- `title`: The title of the post.
- `raw_text`: The raw text of the post.
- `created_at`: The creation date and time of the post.
- `added_at`: The date and time when the post was added.
- `platform_source`: The platform source of the post.
- `post_url`: The URL of the post.
- `author_name`: The name of the author of the post.
- `author_id`: The ID of the author of the post.
- `post_score`: The score of the post.
- `status`: The status of the post.

**Example:**

Request:
Response:
```json
[
    {
        "id": 13,
        "post_id": "1ax2n22",
        "title": "SHA-256 Under the Hood",
        "raw_text": "",
        "created_at": "2024-02-22T17:46:47Z",
        "added_at": "2024-02-22T10:08:08.580246Z",
        "platform_source": "Reddit",
        "post_url": "/r/Bitcoin/comments/1ax2n22/sha256_under_the_hood/",
        "author_name": "pickeydotai",
        "author_id": "7kgjzha1s",
        "post_score": 1,
        "status": "PENDING"
    }
]
```

---