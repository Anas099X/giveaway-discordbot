# CensorUp Discord Bot
> This is discord bot version of the [CensorUp Project](https://github.com/Anas099X/CensorUp)

<img width="1897" height="958" alt="image" src="https://github.com/user-attachments/assets/ca0ee0bb-2f03-4d0b-b008-9332923d6e55" />

A Discord Bot Implementation of the CensorUp Project to Censor any unwanted words from any audio/video.

> [Invite link for Demo Bot](https://discord.com/oauth2/authorize?client_id=1383156915424727090&permissions=117760&integration_type=0&scope=bot)

## Commands
To use the bot, simply run the /censor_media command and upload your audio/video file 
then write the list of words you want to be censored from video seperated by comma ex.`Badword1,Badword2,Badword3`.

## Quick start

**1. Create a Discord bot**

* Go to the [Discord Developers Portal](https://discord.com/developers/applications/) and create a new application.
* Add a bot to the application and copy its **Bot Token**.
* Create a `.env` file in the project root and paste the token as:

```env
DISCORD_TOKEN=your_bot_token_here
```


**2. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Run the bot**

```bash
python bot.py
```

## Contributing
Contributions are welcome. Please open issues or pull requests with improvements, bug fixes, or new features.
