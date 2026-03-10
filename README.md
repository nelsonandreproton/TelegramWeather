# TelegramWeather

A lightweight Python service that sends a daily weather report to a Telegram bot at 06:00 AM Lisbon time.

## Sample message

```
☀️ Weather — Tuesday, 10 March 2026

🌡 Temperature
  Min 12°C · Avg 17°C · Max 22°C
  Feels like: 10°C → 20°C

🌧 Rain: 30% chance · 2.5mm
💨 Wind: 15 km/h
💧 Humidity: 68%

🔆 UV Index: 6 (High)
🌅 Sunrise: 06:55 · Sunset: 19:45

🌫 Air Quality: 35 – Fair
   PM2.5: 8.0 µg/m³ · PM10: 15.0 µg/m³
```

## Data sources

- **Weather & UV:** [Open-Meteo Forecast API](https://open-meteo.com/) — free, no API key required
- **Air quality:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) — free, no API key required

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- Your Telegram chat ID

## Quick start

### 1. Get a Telegram bot token

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the token you receive

### 2. Get your Telegram chat ID

Send any message to your bot, then open this URL in a browser (replace `<TOKEN>` with your token):

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

Find `"chat": {"id": ...}` in the response — that number is your chat ID.

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```dotenv
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=123456789
LATITUDE=38.7169
LONGITUDE=-9.1399
```

### 4. Install dependencies

```bash
uv sync
```

### 5. Test it (sends a message immediately)

```bash
uv run python src/test_send.py
```

## Deployment on Hetzner (Docker)

### Prerequisites

SSH into your VM and install Docker if not already present:

```bash
curl -fsSL https://get.docker.com | sh
```

### Deploy

```bash
# Create project directory
mkdir -p /opt/telegram-weather
cd /opt/telegram-weather

# Clone the repository
git clone https://github.com/your-username/TelegramWeather.git .

# Create and fill in your .env
cp .env.example .env
nano .env

# Build and start
docker compose up -d --build

# Verify it's running
docker compose ps
docker compose logs -f
```

The container runs continuously. The message is sent every day at **06:00 AM Europe/Lisbon** time. The container restarts automatically if it crashes or the VM reboots.

### Update after code changes

```bash
cd /opt/telegram-weather
git pull
docker compose up -d --build
```

## Project structure

```
TelegramWeather/
├── src/
│   ├── main.py          # Scheduler entry point (APScheduler, 06:00 Europe/Lisbon)
│   ├── weather.py       # Open-Meteo API calls (forecast + air quality)
│   ├── telegram.py      # Message formatting + Telegram Bot API sender
│   └── test_send.py     # One-shot test script
├── pyproject.toml       # Dependencies (uv)
├── uv.lock              # Locked dependency versions
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Metrics included

| Metric | Source | Notes |
|---|---|---|
| Min / Avg / Max temperature | Open-Meteo daily | °C |
| Feels-like temperature | Open-Meteo daily | Apparent temperature min/max |
| Rain probability | Open-Meteo daily | % |
| Rain amount | Open-Meteo daily | mm |
| Wind speed | Open-Meteo daily | km/h max |
| Humidity | Open-Meteo hourly | Daily average % |
| UV Index | Open-Meteo daily | Max with label (Low → Extreme) |
| Sunrise / Sunset | Open-Meteo daily | Local Lisbon time |
| Air Quality (AQI) | Open-Meteo air quality | European AQI, daily max |
| PM2.5 / PM10 | Open-Meteo air quality | µg/m³ at noon |

### UV Index scale

| Value | Label |
|---|---|
| 0–2 | Low |
| 3–5 | Moderate |
| 6–7 | High |
| 8–10 | Very High |
| 11+ | Extreme |

### European AQI scale

| Value | Label |
|---|---|
| 0–20 | Good |
| 21–40 | Fair |
| 41–60 | Moderate |
| 61–80 | Poor |
| 81–100 | Very Poor |
| 101+ | Extremely Poor |

## Configuration reference

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Yes | Target chat ID (personal: positive int, group/channel: negative int prefixed with `-100`) |
| `LATITUDE` | Yes | Location latitude (decimal degrees) |
| `LONGITUDE` | Yes | Location longitude (decimal degrees) |

## Security notes

- Secrets are loaded from environment variables — never hardcoded
- `.env` is excluded from version control via `.gitignore`
- All external calls use HTTPS with certificate validation (httpx default)
- No inbound ports are exposed — the bot only sends outbound messages
- API keys: none required (Open-Meteo is public)
