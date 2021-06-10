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
```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --user
pip3 install ics --user
```

Then you need the google API credentials as detailed in the prerequisites [here](https://developers.google.com/calendar/quickstart/python) and store the relevant `.json` files in your home directory.


# Running

The structure of your input and output calendars is governed by the `cal_dict` dictionary. Each entry in the dictionary corresponds to a calendar "group". Each group can have multiple input calendars and usually one output calendar. The format is as follows:

```python
cal_dict={
    "GROUP NAME":{
        "input_urls":{
            "INPUT1 LABEL":"<ics1 URL (e.g. https://indico.cern.ch/category/<CATEGORY ID>/events.ics?user_token=1234_XYZ)>",
	    "INPUT2 LABEL":"<ics2 URL>",
        },
        "output_IDs":{
            "OUTPUT LABEL":"<GOOGLE CALENDAR ID>@group.calendar.google.com"
        },
	"filter":{
            "exclude":["THIS BORING MEETING NAME"]
        },
    }
}
```	


To run you simply execute the script:
```bash
./calendar_scraper.py
```

# Cron job

To get this running once every 4 hours in a cron job on lxplus you can run `acrontab -e` and the enter the following line:
```
0 */4 * * * lxplus /afs/cern.ch/user/<USER INITIAL>/<USERNAME>/calendar-scraper/calendar_scraper.py > /afs/cern.ch/user/<USER INITIAL>/<USERNAME>/calendar-scraper/calendar_scraper.log
```