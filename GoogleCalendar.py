from pprint import pprint
from Googlesit import create_service

CLIENT_SECRET_FILE = 'Google_Calendar.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
#create calendar
def create_calendar(summary):
    if service:
        request_body = {
            'summary': summary
        }
        try:
            service.calendars().insert(body=request_body).execute()
            print('Calendar created successfully.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Failed to create Google Calendar service instance')

#list calendar
def GET_Calendar_ID(service,summary):
    if service:
        try:
            calendars = service.calendarList().list().execute()
            for calendar in calendars['items']:
                if calendar['summary'] == summary:
                    return calendar['id']
            return None    
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Failed to create Google Calendar service instance')

   #delete calendar 
def delete_calendar(calendar_summary_id):     
    if service:
        try:
            # Replace with the correct calendarId
            calendar_id = calendar_summary_id
            service.calendars().delete(calendarId=calendar_id).execute()
            print('Calendar deleted successfully.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Failed to create Google Calendar service instance')

def create_event( month: int, day: int, hour: int, name: str, calendar: str) -> None:
            event_request_body = {
                'start': {
                    'dateTime': '2024-{}-{}T{}:00:00'.format(month, day, hour),
                    'timeZone': 'Africa/Cairo'
                },
                'end': {
                    'dateTime': '2024-{}-{}T{}:00:00'.format(month, day, hour),
                    'timeZone': 'Africa/Cairo'
                },
                'summary': name,
                'colorId': '10',
                'status': 'confirmed',
                'transparency': 'opaque',
                'visibility': 'private',
                'location': 'Egypt',
            }
            calendar_id_summary: str = GET_Calendar_ID(service, calendar)
            sendNotification: bool = True
            sendUpdates: str = 'all'
            service.events().insert(calendarId=calendar_id_summary,
                                    sendNotifications=sendNotification,
                                    sendUpdates=sendUpdates,
                                    body=event_request_body).execute()
            print('Event created successfully.')


def delete_event(calendar_name, event_name):
    try:
        if service:
            calendar_id_summary = GET_Calendar_ID(service, calendar_name)
            event_id= GET_Event_ID(service, calendar_name, event_name)
            service.events().delete(calendarId=calendar_id_summary, eventId=event_id).execute()
            print('Event deleted successfully.')
        else:
            print('Failed to delete Google Calendar event')     
    except Exception as e:
        print(f'An error occurred: {e}')    
        
        
def GET_Event_ID(service, calendar_name, event_name):
    if service:
        try:
            calendar_id_summary = GET_Calendar_ID(service, calendar_name)
            events = service.events().list(calendarId=calendar_id_summary).execute()
            for event in events['items']:
                if event['summary'] == event_name:
                    return event['id']
            return None
        except Exception as e:
            print(f'An error occurred: {e}')
while True:
    user_input = input("How can I help you?  ")
    if 'create calendar' in user_input.lower():
        calendar_summary = input("sure, what is the calendar name?  ")
        create_calendar(calendar_summary)
        
    elif 'delete calendar' in user_input.lower():
        calendar_summary = input("sure, what is the calendar name?  ")
        calendar_id = GET_Calendar_ID(service, calendar_summary)  
        delete_calendar(calendar_id)
        
    elif 'create event' in user_input.lower():
        month=input("Enter the month of the event: ")
        day=input("Enter the day of the event: ")
        hour=input("Enter the hour of the event: ")
        name = input("Enter the name of the event: ")
        calendar = input("Enter the name of the calendar: ")
        create_event(month, day, hour, name, calendar)
        
    elif'delete event' in user_input.lower():
        calendar_name = input("Enter the name of the calendar: ")
        event_name = input("Enter the name of the event: ")
        delete_event(calendar_name, event_name)
          
          
        
          
    
        
        