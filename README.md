This repo contains a simple python script to copy events from ics calendar subscriptions to personal google calendars.

But WHY?!

This lets you:
- group calendar subscriptions as you want
- filter to get only the events you want
- have events the are editable/deletable by you.

The script should be run in a cron job to update ~daily.
It relies on the [icspy API](https://github.com/ics-py/ics-py) for reading ics calendar subscriptions and on the [google calendar API](https://developers.google.com/calendar/overview) to read from and write to your personal google calendars.