Instructions
======
Install dependencies using `pip install -r requirements.txt`.
Fill out your information in `config.json.example` and rename to `config.json`.
Run by calling `python main.py` or create a cronjob to run scheduled.

## Cron example

e.g. by using `crontab -e`
`0 17 * * * python ~/development/backup-to-stack/main.py` (every day at 17:00)
