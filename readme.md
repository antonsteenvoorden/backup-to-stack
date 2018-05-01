Instructions
======
Setup virtualenv `virtualenv venv -p python3`.
Install dependencies using `pip install -r requirements.txt`.
Fill out your information in `config.json.example` and rename to `config.json`.
Run by calling `python main.py` or create a cronjob to run scheduled.

## Cron example
e.g. by using `crontab -e`:
````#every day at 17:00 and write output to file
0 17 * * * python ~/development/backup-to-stack/main.py >> ~/backup-output.txt```

### Mac users
You have to edit the `start.sh.example` script to fit your file location, because it cant run the python script in the virtualenv.
Rename to `start.sh` and add the cron: `0 17 * * * <path_to_parent>/backup-to-stack/start.sh >> ~/backup-output.txt`.