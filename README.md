# Scraper Engine

A reusable Python toolkit for building web-scraping pipelines with separate components for HTTP fetching, HTML parsing, structured-data extraction, logging, and storage.

> **Status:** Work in progress — the core architecture is implemented and currently being expanded.

## Why this project?

Scraper Engine is an experiment in extracting recurring concerns into reusable and loosely coupled components that can be shared across different scraping projects.

The project also explores software-design concepts such as dependency inversion, adapters, protocols, and separation of responsibilities.

## Features

* Synchronous HTTP fetching using `curl_cffi`
* Browser impersonation support
* Proxy, headers, query parameters, cookies, and payload support
* HTTP client abstraction through Python `Protocol`
* Adapters for different HTTP client implementations
* Asynchronous multi-URL fetching
* HTML parsing with Beautiful Soup
* CSS selector helpers for text and attributes
* JSON-LD extraction with `extruct`
* SQL database storage using SQLAlchemy Core
* Transaction management
* Structured JSON logging
* Human-readable text logging
* Size-based and time-based log rotation

## Project structure

```text
scraper_engine/
├── src/
│   └── scraper_engine/
│       ├── fetchers/
│       │   ├── async_fetcher.py
│       │   └── sync_fetcher.py
│       ├── handlers/
│       │   └── response_handler.py
│       ├── loggers/
│       │   ├── configs/
│       │   │   ├── custom_formatters.py
│       │   │   ├── custom_handlers.py
│       │   │   └── logging_setup.py
│       │   └── logger_config.yaml
│       ├── parsers/
│       │   ├── html_parser.py
│       │   └── json_ld_parser.py
│       └── storage/
│           ├── db_storage.py
│           └── excel_storage.py
├── pyproject.toml
├── uv.lock
└── Dockerfile
```

## Installation

Python 3.11 or newer is required.

Using [`uv`](https://docs.astral.sh/uv/):

```bash
git clone git@github.com:Alessandroc92/scraper_engine.git
cd scraper_engine

uv sync
```

Activate the environment if needed:

```bash
source .venv/bin/activate
```

## Usage

### Fetch a page

```python
from scraper_engine.fetchers.sync_fetcher import SyncFetcher

fetcher = SyncFetcher()

response = fetcher.request(
    url="https://example.com",
    method="get",
)

print(response.status_code)
print(response.text[:200])
```

A proxy can be configured for the entire fetcher:

```python
fetcher = SyncFetcher(
    proxy="http://user:password@proxy.example.com:8000"
)
```

or for a single request:

```python
response = fetcher.request(
    url="https://example.com",
    method="get",
    proxy="http://user:password@proxy.example.com:8000",
)
```

### Parse HTML

```python
from scraper_engine.parsers.html_parser import HtmlParser

parser = HtmlParser(response.text)

titles = parser.select_text("h1")
links = parser.select_attr("a", "href")

print(titles)
print(links)
```

The parser lazily creates and reuses the underlying `BeautifulSoup` object.

### Extract JSON-LD

```python
from scraper_engine.parsers.json_ld_parser import JsonLdParser

parser = JsonLdParser(response.text)
data = parser.extract()

print(data)
```

### Fetch multiple URLs asynchronously

```python
import asyncio

from scraper_engine.fetchers.async_fetcher import AsyncFetcher


async def main():
    urls = [
        "https://example.com",
        "https://example.org",
    ]

    fetcher = AsyncFetcher(max_clients=5)
    responses = await fetcher.fetch_all(urls)

    for response in responses:
        print(response.status_code)


asyncio.run(main())
```

### Store data with SQLAlchemy

`DbStorage` provides a small wrapper around SQLAlchemy Core for table creation, transactions, queries, and result mapping.

```python
from sqlalchemy import Column, Integer, String, insert, select

from scraper_engine.storage.db_storage import DbStorage


storage = DbStorage("sqlite:///example.db")

pages = storage.create_table(
    "pages",
    Column("id", Integer, primary_key=True),
    Column("title", String),
)

storage.execute_query(
    insert(pages).values(title="Example page")
)

rows = storage.fetch_results(
    select(pages)
)

print(rows)
```

The same component can be used with other databases supported by SQLAlchemy by changing the connection URL.

## HTTP client abstraction

`SyncFetcher` does not depend directly on a specific HTTP session interface.

Instead, it expects an object implementing the `HttpSession` protocol:

```python
class HttpSession(Protocol):
    def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ):
        ...
```

The default implementation uses a `CurlCffiAdapter`, while alternative session implementations can be injected without changing the fetcher itself.

```text
SyncFetcher
    │
    ▼
HttpSession protocol
    │
    ├── CurlCffiAdapter ──► curl_cffi.Session
    │
    └── RequestsAdapter ──► requests-compatible session
```

This keeps fetching logic separated from the underlying HTTP library.

## Logging

The package includes configurable text and JSON logging.

JSON logs contain structured information such as:

```json
{
  "time": "2026-08-27T10:30:00.000+00:00",
  "logger_name": "scraper_engine",
  "logger_level": "ERROR",
  "module": "db_storage",
  "function": "create_transaction",
  "logger_line": 35,
  "message": "CRITICAL ERROR WHEN EXECUTING SQL STATEMENT",
  "exception_info": null,
  "extra": {}
}
```

Logs can be written to:

```text
logs/app.log
logs/app.jsonl
```

with automatic rotation configured in `logger_config.yaml`.

## Current status

| Component                   | Status         |
| --------------------------- | -------------- |
| Synchronous fetching        | ✅ Implemented  |
| HTTP client abstraction     | ✅ Implemented  |
| `curl_cffi` adapter         | ✅ Implemented  |
| Requests-compatible adapter | ✅ Implemented  |
| HTML parser                 | ✅ Implemented  |
| JSON-LD parser              | ✅ Implemented  |
| SQLAlchemy storage          | ✅ Implemented  |
| Structured logging          | ✅ Implemented  |
| Asynchronous fetching       | 🚧 In progress |
| Excel storage               | 📋 Planned     |
| Automated tests             | 📋 Planned     |
| Docker image                | 📋 Planned     |

## Roadmap

Planned improvements include:

* [ ] Add unit and integration tests
* [ ] Complete and harden the asynchronous fetcher
* [ ] Add timeout and error-handling policies
* [ ] Add retry/backoff support
* [ ] Implement Excel storage
* [ ] Improve database abstractions
* [ ] Remove automatic logging configuration from library internals
* [ ] Add Docker support
* [ ] Expand documentation and usage examples
* [ ] Use the engine in real-world scraping projects

## Design goals

The project is intentionally kept separate from site-specific scraping logic.

The engine should provide reusable infrastructure:

```text
fetch → parse → transform → store
```

while individual projects define what to scrape, how to interpret the extracted data, and which domain models to build.

This repository is primarily a learning and portfolio project focused on building maintainable scraping infrastructure rather than a finished scraping framework.
