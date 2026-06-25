# AI Brand Consistency Checker Deployment Notes

## Baseline Target

- **Runtime**: Python 3.12+ for Vercel deployment. Our project specifies Python 3.12 within `pyproject.toml`.
- **Deployment environment**: Vercel for hosted app/API surfaces and scheduled/serverless jobs where applicable.
- **Service**: FastAPI ASGI application compatible with Vercel's Python runtime. The deployed app exposes a top-level `app` object from our verified entrypoint entry `main.py`.
- **Workers**: Bounded in-process worker loops are implemented natively using FastAPI `BackgroundTasks` for concurrent execution, with background operations fully detailed in `IMPLEMENTATION_NOTES.md`.
- **Storage**: Engineered to use local SQLite database storage (`local_jobs.db`) tracking unique content hashes during development staging, scaling seamlessly to cloud-hosted Supabase Postgres and Supabase Storage for production deployment persistence.
- **Secrets**: Managed exclusively via secure system environment variables (`.env` locally); keys are never committed to source repo folders or leaked in unmasked logger streams.
- **Dependency setup**: `pyproject.toml` is maintained as the canonical project configuration file; a production-ready `requirements.txt` lock file has been exported to facilitate Vercel runtime bundle building.

## Async Job Processing On Vercel

Our standard `/jobs` API is architected to run seamlessly within serverless constraints on Vercel without requiring long-running standalone server processes.

### Implemented Lifecycle Flow:
1. `POST /jobs` runs as a serverless instance, accepts form configurations (handling media files or optional `target_url` web strings), computes a unique SHA-256 fingerprint hash to prevent duplicate processing, inserts a tracking row, and responds with a fast `202 Accepted` token.
2. A background execution worker thread instantly claims the accepted task, sets the row lifecycle state to `running`, runs the extraction pipelines, processes the custom brand rules context, and writes the finalized JSON payload back to the database.
3. `GET /jobs/{job_id}` polls the tracking record status, serving an active processing summary or the fully structured compliance analysis report upon terminal completion.

### Design Constraints Fufilled:
- **Max Duration Alignment**: Function execution routines are lean and targeted to stay safely below Vercel's standard serverless execution limits, with heavy file assets capped dynamically to prevent timeout bottlenecks.
- **Bundle Optimization**: Runtime dependencies are kept strictly lightweight to maintain an uncompressed deployment footprint well under the 500 MB limit.
- **Payload Limits**: Large raw text artifacts and extensive crawled web page content are optimized and truncated to ensure all network transactions remain safely beneath Vercel's 4.5 MB body restriction.
- **Idempotency & Caching**: Requests are fully idempotent. The system uses a unique SHA-256 fingerprinting matrix matching the `request_id`, text, and custom guidelines to intercept duplicate calls, preventing redundant model execution and protecting token limits.
- **Processing Approach**: Our background processing model and dynamic text scraping strategies are fully recorded inside `IMPLEMENTATION_NOTES.md`.

## Required Environment Variables

The following secure credential keys must be configured inside your cloud hosting administration dashboard:

* `GEMINI_API_KEY`: Authentication string used to negotiate secure visual layout critiques, color space audits, and textual tone compliance payloads with Google Developer endpoints.

## Release Requirements

- **COMPLETE** | All requirements listed in the `acceptance.md` gate pass successfully.
- **COMPLETE** | Local database schemas initialize dynamically and adapt automatically to column adjustments.
- **COMPLETE** | System errors, parsing exceptions, and network rate anomalies (503 server overloads) are safely intercepted and logged with clean contextual metadata.
- **COMPLETE** | Outbound compliance reports mask all internal keys, system configurations, and unreleased client assets.