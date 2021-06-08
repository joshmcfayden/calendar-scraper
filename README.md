This repo uses a simple python script to copy events from ics calendar subscriptions to personal google calendars.
But WHY?!

This lets you:
- group keep ics subscriptions as you want
- filter to get only the events you want
- have events the are editable/deletable by you.

The script should be run in a cron job.
It relies on the `icspy` API for reading ics calendar subscriptions and on the google calendar API to read from and write to your personal google calendars.