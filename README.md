# Startup Memory Bot

Automatically captures conversations from a private Telegram group, structures them with Claude AI, and stores the knowledge in both Notion and GitHub.

## What it does

1. **Listens** to a private Telegram group (2 founders) via Telethon user session
2. **Groups** messages into sessions (gap > 120 min = new session)
3. **Extracts** decisions, open questions, ideas, and action items via Claude Sonnet
4. **Transcribes** voice messages via OpenAI Whisper
5. **OCRs** images via Claude Vision
6. **Writes to Notion** — Sessions DB + Knowledge Items DB with full page content
7. **Commits to GitHub** — per-session files + cumulative files + auto-regenerated `STARTUP_CONTEXT.md`
8. **Admin bot** — `/status`, `/retry`, `/last`, `/backfill` commands + failure alerts

---

## Installation

### 1. Get Telegram API credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in → API Development tools → Create app
3. Copy `App api_id` and `App api_hash`

### 2. Set up Notion

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) → New integration
2. Copy the **Internal Integration Token**
3. Create two databases in Notion:
   - **Sessions** with properties: Title (title), Date (date), Duration (number), Participants (multi_select), Main Topics (multi_select), Energy (select), Decisions Count (number), Open Questions Count (number), Action Items Count (number), Summary (rich_text), GitHub Link (url), Status (status)
   - **Knowledge Items** with properties: Title (title), Type (select), Status (select), Owner (rich_text), Tags (multi_select), Session (relation → Sessions), Date (date), Priority (select)
4. Share both databases with your integration (... → Add connections)
5. Copy the database IDs from the URL: `notion.so/{workspace}/{DATABASE_ID}?v=...`

### 3. Set up GitHub

1. Create a private repo (e.g., `username/startup-memory`)
2. Go to Settings → Developer settings → Fine-grained tokens
3. Create token with **Contents: Read and write** permission for the repo
4. Copy the token

### 4. Create admin bot

1. Message [@BotFather](https://t.me/BotFather) → `/newbot`
2. Copy the bot token
3. Add the bot to your Telegram group as admin (for notifications)

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with all your credentials
```

Also set Postgres credentials:
```bash
POSTGRES_USER=user
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=startupdb
DATABASE_URL=postgresql+asyncpg://user:yourpassword@postgres:5432/startupdb
```

---

## Generate TG_SESSION_STRING

Run this **once locally** (not in Docker):

```bash
pip install telethon
python generate_session.py
```

Enter your phone number, the confirmation code, and 2FA password if set. Copy the printed `TG_SESSION_STRING` into your `.env` file.

---

## Running with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f worker
docker-compose logs -f listener

# Check status
docker-compose ps
```

Services started:
- `postgres` — database
- `redis` — message queue
- `migrate` — runs Alembic migrations once
- `listener` — watches Telegram group
- `worker` — processes sessions with Claude/Notion/GitHub
- `admin-bot` — Telegram bot for operator commands

---

## Running backfill

To load historical messages:

```bash
# Load ALL history from the beginning
docker-compose run --rm worker python -m src.backfill --since-id 0

# Load from a specific message ID
docker-compose run --rm worker python -m src.backfill --since-id 12345

# Load limited number of messages
docker-compose run --rm worker python -m src.backfill --since-id 0 --limit 1000
```

Backfill is **resumable** — if interrupted, it resumes from the last checkpoint stored in Redis.

---

## Admin bot commands

| Command | Description |
|---------|-------------|
| `/status` | Pending sessions count + last processed session summary |
| `/last` | Detailed summary of the last session |
| `/retry <session_id>` | Re-process a failed session |
| `/backfill <msg_id>` | Start backfill from message ID |

---

## GitHub repo structure

After processing, the GitHub repo looks like:

```
startup-memory/
├── STARTUP_CONTEXT.md           ← regenerated after every session
├── sessions/
│   ├── 2026-05-27-10-01.md
│   ├── 2026-05-27-16-02.md
│   └── 2026-05-28-09-01.md
├── decisions/
│   └── all-decisions.md         ← cumulative, append-only
└── open-questions/
    └── open-questions.md        ← cumulative, closed items marked [CLOSED]
```

### Example STARTUP_CONTEXT.md

```markdown
# Startup Context
_Last updated: 2026-05-27 18:30 UTC_

## What we're building
An AI-powered B2B SaaS platform for automated customer onboarding.
The core product is a conversational wizard that integrates with CRM systems
and reduces time-to-value from weeks to hours.

## Current Status
MVP backend complete. Frontend in progress (ETA: 2 weeks).
Currently validating with 3 pilot customers. Target: paid contract by June 15.

## Key Decisions Made
- [2026-05-10] Use Supabase for auth and database — faster than building custom
- [2026-05-15] Focus B2B only, no consumer market
- [2026-05-20] Charge per seat, not usage — easier for enterprise procurement
- [2026-05-27] Launch on ProductHunt after first paid customer

## Open Questions
- What's the minimum contract size that makes sense?
- Do we need SOC2 for enterprise sales?
- Should we build a mobile app in year 1?

## Next Actions
- @Alex: Set up Stripe billing by 2026-05-30
- @Serzh: Record 3 demo videos for pilots
- @Alex: Schedule calls with 5 more prospects
```

---

## Architecture

```
Telegram Group
     │
     ▼
[Telethon Listener] → Redis Stream (tg:incoming)
                              │
                              ▼
                       [ARQ Worker]
                         │     │
               ┌─────────┘     └─────────┐
               ▼                         ▼
         [Claude API]              [OpenAI STT]
         (structure)               (voice→text)
               │
        ┌──────┴──────┐
        ▼             ▼
  [Notion API]  [GitHub API]
  (Sessions +   (markdown
   Items DBs)    commits)
        │             │
        └──────┬──────┘
               ▼
         [PostgreSQL]
         (state + items)
               │
               ▼
        [Admin Bot]
        (notifications
         + commands)
```
# tg-memory-bot
