#!/usr/local/bin/python3
#/usr/bin/env python3

# includes for gCal API
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']
cred_dir = os.environ["HOME"]

# includes for ics API
from ics import Calendar
import requests

# Misc includes
import pprint
import pytz
import dateutil.parser


cal_dict={
    "HSF":{
        "input_urls":{
            "HSF Gen":"https://indico.cern.ch/export/categ/8460.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=1bbdb4650aaca5878e705cf8a4d813cc4dd053ef",
            "HSF Coord":"https://indico.cern.ch/export/categ/7970.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=9eedf5095d2544f573adbb756ae5809028c438e9"
        },
        "output_IDs":{
            "HSF":"flg2mj5lv0432013c02s3jhiv4@group.calendar.google.com"
        },
        "filter":None,
    },


    "Top+X":{
        "input_urls":{
            "ATLAS Top+X":"https://indico.cern.ch/export/categ/12104.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=23d64faf6b2f598b2a998200f6fbbb7822dd5204",
            "ATLAS HTop":"https://indico.cern.ch/export/categ/9788.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=d3a58260e55ce56e1ecad3698607f17b73752bb7",
            "Global EFT":"https://indico.cern.ch/category/13634/events.ics?user_token=56945_50Z_rm3Q7FGn8I8SI2Na5qEoXTnrng6_n0t_fN6Hx5U",
        },
        "output_IDs":{
            "Top+X":"1mue6og8iee85iuigf9n8r2a3c@group.calendar.google.com",
        },
        "filter":{
            "exclude":["Heavy neutrinos search in ttbar decays","SM tqGamma analysis meeting","CLFV in top-quark decays","Four tops re-interpretation working meeting","Top Yukawa coupling","FCNC photon informal meeting"]
        }
    },


    "ATLAS Plenaries":{
        "input_urls":{
            "ATLAS Top":"https://indico.cern.ch/export/categ/3332.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=3f74262d700b2c654cc2a6088c53f8ffa12cd74a",
            "ATLAS Higgs":"https://indico.cern.ch/export/categ/3966.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=883d265cbae2731fd5029de644f0fa69ae8e5857",
            "ATLAS Weekly":"https://indico.cern.ch/category/2636/events.ics?user_token=56945_bUCz2q9qTIj50tKIYQYKZA9QCrMWwnQA07ldk8N8lCg",
            "ATLAS Weeks":"https://indico.cern.ch/export/categ/6848.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=ff35771f9a16bebe452d0a2c2dad59eb13f46c34",
            "ATLAS P&P Weeks/Workshops":"https://indico.cern.ch/category/6945/events.ics?user_token=56945_dh-FtiAf3AXHwwywsgLMAgCyNxhVO1ND7nf3Gj9CeS0",
        },
        "output_IDs":{
            "ATLAS Plenaries":"rvehr8oeva6ajstqr3f4q20f2s@group.calendar.google.com",
        },
        "filter":None,
    },
    

    "Sussex":{
        "input_urls":{
            "Sussex ATLAS":"https://indico.cern.ch/export/categ/3756.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=45e22b2978cd0656eaf376db83bb51ce2e3a7af3",
            },
        "output_IDs":{
            "Sussex Meetings":"fusq2rkvovusl7ctjv7l019p5c@group.calendar.google.com",
        },
        "filter":None,   
    },


    "PMG":{
        "input_urls":{
            "PMG Plenaries":"https://indico.cern.ch/export/categ/10312.ics?apikey=d465b7f8-bb8d-4da9-b4e0-069b534b2af3&from=-31d&signature=76faf7f17a03715236e38a49263e03bf82932049"
            },
        "output_IDs":{
            "PMG":"e8b4pbarfrahv4u1vub33lsc3g@group.calendar.google.com",
        },
        "filter":None,   
    },

    
    
}


def main():

    # Get google calendar API service
    service=get_gcalsvc()

    total_new_events=0
    
    # Iterate over calendar groups in calendar dictionary
    for cal_grp in cal_dict:
        
        print(f"Processing calendar group {cal_grp}")
        
        events=[]

        # Get all events from input ics subscriptions
        for in_lab,in_url in cal_dict[cal_grp]["input_urls"].items():
            print(f"   - Getting events from {in_lab}: {in_url}")
            events.extend(get_icsevents(get_icscal(in_url)))
        print(f'   Found {len(events)} event(s) from {len(cal_dict[cal_grp]["input_urls"])} calendar(s)')


        # Write events to output google calendar (if they do not already exist and pass filter requirements)
        for out_lab,out_ID in cal_dict[cal_grp]["output_IDs"].items():
            outcal_events=get_existing_gcal_events(service,out_ID)
            events_to_write=gcal_events_to_update(events,outcal_events,cal_dict[cal_grp]["filter"])
            total_new_events+=len(events_to_write)
            print(f"   - Sending {len(events_to_write)} new event(s) to {out_lab}: {out_ID}")
            for event in events_to_write:
                insert_gcal_event(service,out_ID,event)
                
    print(f'\nFound a total of {total_new_events} new event(s) to write.')
    
def get_gcalsvc():
    """Gets google calendar API service"""

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cred_dir+'/token.json'):
        creds = Credentials.from_authorized_user_file(cred_dir+'/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_dir+'/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cred_dir+'/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service



def create_gcal_event(summary,start,end,location=None,description=None,url=None):
    """Put standard event data in dictionary format that can be passed directly to google API"""
    event = {}
    event['summary']=f'{summary}'
    event['start']={
        'dateTime': f'{start}',
        'timeZone': 'Europe/London',
    }
    event['end']={
        'dateTime': f'{end}',
        'timeZone': 'Europe/London',
    }

    if location:
        event['location']=f'{location}'

    if description:
        event['description']=f'{description}'

    if url:
        event['htmlLink']=f'{url}'

    #pprint.pprint(event)
    return event


def insert_gcal_event(service,calendarId,event):
    """Add new event to google calendar"""
    event = service.events().insert(calendarId=calendarId, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    return
    
def get_existing_gcal_events(service,calendarId):
    """Get existing events from google calendar"""
    events_result = service.events().list(calendarId=calendarId).execute()
    events = events_result.get('items', [])
    return events
    
def get_icscal(url):
    """Get icspy calendar object from ics url"""
    c = Calendar(requests.get(url).text)
    return c


def get_icsevents(c):
    """Takes input ics Calender object to extract events and return them in google calendar format"""
    events_for_gcal=[]
    for e in list(c.events):
        print(f'      - {e.name}: {e.begin}-{e.end}, {e.url}')
        events_for_gcal.append(create_gcal_event(e.name,e.begin,e.end,description=e.description,url=e.url))

    return events_for_gcal
        

def match_datetimes(ds1,ds2):
    """Dates can be read from different timezones but correspond to the same time, this compares datetimes at UTC"""
    dt1 = dateutil.parser.parse(ds1)
    dt2 = dateutil.parser.parse(ds2)
    local_dt1 = dt1.astimezone(pytz.utc)
    local_dt2 = dt2.astimezone(pytz.utc)
    #print(local_dt1,local_dt2)
    return local_dt1 == local_dt2


def gcal_events_to_update(events_found,events_in_cal,filters):
    """Work out which events need to be written"""

    events_to_write=[]
    for w_evt in events_found:
        write=True

        # only update events
        for c_evt in events_in_cal:
            #print(w_evt["summary"],c_evt["summary"],w_evt["start"],c_evt["start"])

            if w_evt["summary"] == c_evt["summary"] and match_datetimes(w_evt["start"]["dateTime"],c_evt["start"]["dateTime"]):
                write=False
                break

        # apply filters
        if filters:
            if "exclude" in filters:
                for exc in filters["exclude"]:
                    if exc in w_evt["summary"]:
                        print(f'Skipping because exclude string "{exc}" found in event summary "{w_evt["summary"]}"')
                        write=False
                        break

            if "include" in filters:
                failed_matches=[inc for inc in filters["include"] if inc not in w_evt["summary"]]
                if len(failed_matches) == len(filters["include"]):
                    print(f'Skipping because none of include strings {filters["include"]} found in event summary "{w_evt["summary"]}"')
                    write=False
                    
        if write: events_to_write.append(w_evt)
        
    return events_to_write
    

if __name__ == '__main__':
    main()
