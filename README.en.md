# RealWorld API Automation Testing

[简体中文](README.md) | **English**

## Overview

This Python, Pytest, and Requests project tests the RealWorld (Conduit) Django Ninja backend through its HTTP API. The tests exercise core user and article workflows, access control, state changes, error responses, and selected PostgreSQL records. The project focuses on practical API test design, automation, and validation of backend behavior.

## Tech Stack

Python 3.14 · Pytest · Requests · PostgreSQL · psycopg · python-dotenv · pytest-html · uv · GitHub Actions

## Test Scope

| Area                 | Representative checks                                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Authentication       | Registration, login, current user with a bearer token, duplicate email, missing fields, wrong password, and missing or invalid token. |
| Articles             | Create, read, update, and delete; verify changed fields and slug behavior; reject missing required data or unauthorized changes.      |
| Comments             | Create, list, and delete; verify the author and body; reject unauthenticated creation and deletion by another user.                   |
| Profiles and feed    | Follow and unfollow another user, then check the profile state and whether that user's article appears in the follower's feed.        |
| Favorites            | Favorite and unfavorite an article; check `favorited` and `favoritesCount`.                                                           |
| Lists and pagination | Filter articles by author; check `limit`, `offset`, total count, and a partially filled final page.                                   |
| Database             | Check connectivity and expected tables; compare a created article with stored fields and confirm deletion removes its row.            |

## Test Design

Tests combine successful workflows with negative cases such as missing credentials, invalid payloads, nonexistent resources, and attempts to change another user's content. They check both HTTP status and relevant response fields. Follow, favorite, and feed cases verify state transitions through subsequent reads. Article tests also check data integrity after updates and deletes. Pagination checks use a fixed set of generated articles and include a partial final page.

## Project Structure

```text
.
├── .github/workflows/api-testing.yml  # CI run and report artifact
├── conftest.py                        # clients, data, user, article, and DB fixtures
├── pyproject.toml                     # Python and dependencies
├── pytest.ini                         # markers and console logging
├── src/
│   ├── clients/                       # shared HTTP client and domain clients
│   ├── config/settings.py             # environment-based settings
│   ├── db/db_client.py                # SQL connection and query helper
│   └── utils/data_factory.py          # generated test data
└── tests/
    ├── auth/
    ├── articles/
    ├── comments/
    ├── follow/
    ├── db/
    └── test_health.py
```

## Framework Design

`BaseClient` owns the Requests session, HTTP methods, timeouts, and method/URL/status logging. Authentication, article, comment, and profile clients build endpoint-specific requests on top of it. Pytest fixtures provide reusable clients and setup state, including registered users, owned articles, comments, and database connections. The data factory gives users, articles, and comments unique values so tests can create their own records.

## Database Validation

Selected tests follow an API request with a PostgreSQL query. They compare a created article's slug, title, description, and body with the stored `articles_article` row, check that its user exists, and confirm that a deleted article no longer has a row. Separate checks run `SELECT 1` and inspect expected table names. Database connection settings come from environment variables, so local and CI runs can point to different databases.

## Known Defects

- **BUG-AUTH-001:** The invalid bearer-token test expects `GET /api/user` to return 401, while the backend currently returns 500. It uses `pytest.mark.xfail(strict=True)`, so an unexpected pass fails the test run and prompts review of the defect.
- **Repeated favorite:** A test for favoriting the same article twice is marked `xfail` after observing a failure on the second request. Its expected behavior is not established as a business contract here; the mark records the observed issue without making that claim. This mark does not set `strict=True`.

## Logging and Reporting

`BaseClient` logs the request method and URL, then the response status. Pytest displays INFO logs in the console. CI runs `pytest-html` with `--self-contained-html` to create `reports/report.html` and uploads it as the `pytest-report` workflow artifact. The report is generated during a run; it is not committed to this repository.

## CI

The GitHub Actions workflow runs on pushes and pull requests. It checks out the repository, installs uv and Python 3.14, runs `uv sync`, warms up the Render-hosted API with a request to `$BASE_URL/api/articles`, runs the test suite, and uploads the HTML report even if tests fail. It reads `BASE_URL`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_SSLMODE` from GitHub Secrets.

## Running Locally

Install [uv](https://docs.astral.sh/uv/) and make a compatible RealWorld API and PostgreSQL database available. Set `BASE_URL` and the `DB_*` variables listed above in your environment or in a local `.env` file. `BASE_URL` defaults to `http://localhost:8000`; see `src/config/settings.py` for the database defaults. The repository does not currently include an `.env.example` file.

```bash
uv sync
uv run pytest
uv run pytest -m smoke
uv run pytest -m db
```

The registered markers are `smoke`, `api`, and `db`. The current tests use `smoke` and `db`; no test is currently marked `api`. Database tests require a reachable PostgreSQL instance with the expected backend schema. To generate a local HTML report, run:

```bash
mkdir -p reports
uv run pytest --html=reports/report.html --self-contained-html
```

## Current Scope

The current work focuses on API automation and selected database checks. UI automation and performance testing are outside this repository's current scope.
