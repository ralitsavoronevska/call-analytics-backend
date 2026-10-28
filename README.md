# Call Analytics Backend

Secure REST API for a telecom call-detail-record (CDR) analytics platform. Built for London Success Academy's Week 3 backend assignment.

## Stack

- Python, FastAPI and Uvicorn
- PostgreSQL (Neon), SQLAlchemy and Alembic
- JWT authentication (PyJWT), Argon2 password hashing (`pwdlib`)
- Pydantic settings and schemas
- Render hosting

## Features

- ✅ Login using email and password; JWT bearer tokens
- ✅ User roles: `admin` and `analyst`
- ✅ Protected call records and analytics endpoints
- ✅ Paginated and filterable CDR records
- ✅ Summary analytics and top callers
- ✅ PostgreSQL persistence with schema migrations
- ✅ CSV/CDR import script (10,000 records imported for the project)
- ✅ Public health endpoint and interactive OpenAPI documentation

## API endpoints

| Method | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/health` | Public | Service health |
| `POST` | `/api/auth/login` | Public | Authenticate and obtain a JWT |
| `GET` | `/api/calls` | Bearer JWT | Paginated call records with query filters |
| `GET` | `/api/analytics/summary` | Bearer JWT | Aggregate call metrics |
| `GET` | `/api/analytics/top-callers` | Bearer JWT | Top callers analytics |

The call records endpoint supports `page` and `page_size` query parameters. Explore additional filter parameters and response schemas in `/docs`.

## Demo accounts

The following accounts are provided for evaluating the **demo application only**. The dataset is synthetic/sample CDR data. Do not reuse these credentials for other services.

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@example.com` | `qazwsxedcrfv123` |
| Analyst | `analyst@example.com` | `tgbyhnujmik,123` |

To test the application, open the [live dashboard](https://call-analytics-dashboard-xi.vercel.app/), sign in with either account, and explore the analytics and call records. The API requires a bearer token for protected endpoints. **These are publicly documented demo credentials; rotate or disable them before connecting real or sensitive data.**

## Local setup

Prerequisites: Python 3.14 (the deployed project uses 3.14.2), a PostgreSQL database, and a valid connection string.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file in the backend project directory:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use the PostgreSQL URL format required by your installed driver and database provider. **Never commit `.env`, passwords, database credentials, or JWT secrets.**

Apply database migrations:

```powershell
alembic upgrade head
```

To load the project dataset, inspect and run `scripts/import_cdr.py` with the required input file. To provision users, run `scripts/create_user.py` and follow its prompts. The publicly documented demo credentials above are intended only for the isolated demonstration environment; use separate strong credentials for any real deployment.

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

## Authentication and authorization

Send a JSON request to `POST /api/auth/login` with `email` and `password`. Use the returned `access_token` on protected requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Missing or invalid authentication is rejected with `401 Unauthorized`. Role-restricted operations reject users without sufficient permissions with `403 Forbidden`.

## Frontend integration and CORS

The backend permits requests from the local Vite development server (`http://localhost:5173`, `http://127.0.0.1:5173`) and the deployed dashboard (`https://call-analytics-dashboard-xi.vercel.app`). See `app/main.py` for the current CORS allowlist.

Frontend repository: https://github.com/ralitsavoronevska/call-analytics-dashboard

## Deployment status (October 28, 2026)

**Active Render service URL:** https://call-analytics-backend-o2lz.onrender.com

- [Interactive API documentation (Swagger UI)](https://call-analytics-backend-o2lz.onrender.com/docs)
- [Health check](https://call-analytics-backend-o2lz.onrender.com/api/health)
- [Live frontend](https://call-analytics-dashboard-xi.vercel.app/)

**Verified on October 28, 2026:** the public health endpoint returned `200 OK`, login via Swagger returned `200 OK`, and the deployed Vercel frontend successfully authenticated and loaded call records from the Render API and Neon PostgreSQL database (10,000 CDR records).

An earlier Render hostname (`call-analytics-backend.onrender.com`) returned `503 Service Unavailable`; it is **not** the active API URL. The frontend production environment variable `VITE_API_BASE_URL` must use the active hostname above, without a trailing slash.

Render environment variables must include `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES`. Do not expose their values.

## Related project

[Call Analytics Dashboard](https://github.com/ralitsavoronevska/call-analytics-dashboard) — React and TypeScript frontend, deployed on Vercel.


---

🙌 Thank you for checking out my project! More is coming 🔜.                                                                                                                          
Stay tuned 🚀 and please don't forget to give the project a star! ⭐                                                                                                                   
Made with lots of 💗, ☕, and a sprinkle of ✨ by Ralitsa Voronevska!                                                                                                                   
