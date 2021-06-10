This repo contains a simple python script to copy events from ics calendar subscriptions to personal google calendars.

But WHY?!

This lets you:
- group calendar subscriptions as you want
- filter to get only the events you want
- have events the are editable/deletable by you.

The script should be run in a cron job to update ~daily.

It relies on the [icspy API](https://github.com/ics-py/ics-py) for reading ics calendar subscriptions and on the [google calendar API](https://developers.google.com/calendar/overview) to read from and write to your personal google calendars.

# Setup
The first time you have to do it, setting up the google API authentication is a bit of a pain, but the [instructions](https://developers.google.com/calendar/quickstart/python) are pretty good.

To get the python dependancies it's just two commands:
```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --user
pip3 install ics --user
```

Then you need the google API credentials as detailed in the prerequisites [here](https://developers.google.com/calendar/quickstart/python) and store the relevant `.json` files in your home directory.


# Running

The structure of your input and output calendars is governed by the `cal_dict` dictionary. Each entry in the dictionary corresponds to a calendar "group". Each group can have multiple input calendars and usually one output calendar.


To run you simply execute the script:
```
./calendar-scraper.py
```

# Cron job

To get this running once every 4 hours in a cron job on lxplus you can run `acrontab -e` and the enter the following line:
```
0 */4 * * * lxplus /afs/cern.ch/user/<USER INITIAL>/<USERNAME>/calendar-scraper/calendar-scraper.py > /afs/cern.ch/user/<USER INITIAL>/<USERNAME>/calendar-scraper/calendar-scraper.log
```