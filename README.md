# Giveaway Discord Bot

<img width="1000" height="750" alt="image" src="https://github.com/user-attachments/assets/71a9e878-2dac-4fea-a59a-04bf1b9ce71d" />


A Discord Bot for Giveaways

## Commands List

### 🎉 Giveaway Commands
> Requires **Administrator** permissions

| Command | Description | Options |
|---|---|---|
| `/giveaway create` | Create a new giveaway | `name` *(text)*, `duration` *(int)*, `unit` — `seconds` \| `minutes` \| `hours` \| `days`, `winners` *(int)* |
| `/giveaway list` | List all active giveaways | — |
| `/giveaway end` | End a giveaway and announce winners | `giveaway_name` *(text)*, `forced` *(optional, default: false)* — skip winner selection and end immediately |

## Quick Start

**1. Create a Discord bot**
* Go to the [Discord Developers Portal](https://discord.com/developers/applications/) and create a new application.
* Add a bot to the application and copy its **Bot Token**.

**2. Set up a PostgreSQL database**
* Create a PostgreSQL database and note your credentials.
* Create a `.env` file in the project root and fill in the following:
```env
DISCORD_TOKEN=your_bot_token_here

# Database configuration
HOST=your_host
USER=your_user
PASSWORD=your_password
DATABASE=your_database
PORT=your_port
```

**3. Install dependencies**
```bash
python -m pip install -r requirements.txt
```

**4. Run the bot**
```bash
python bot.py
```

## Contributing
Contributions are welcome. Please open issues or pull requests with improvements, bug fixes, or new features.
