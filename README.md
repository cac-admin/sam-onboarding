# cac-onboarding
## STACK
- Django (REST) + sqlite
- Next JS
- Material UI
- GH Actions
- CentOS / Docker / NGINX
## DECISION
### Task Scheduler:
- Use the GC API to fetch week events (Django)
- Authentication: user specific settings such as working hours, and connect us to their Google account
- User inputs events for the week and their preferences (Next)
- Use preferences, events, and free time from GC API to calculate ideal task schedule
- Send data back to Next
- User can edit (not functional yet), or confirm (Next)
- Django then takes edited or confirmed data and sends a POST to GC API to populate user calendar

https://github.com/SamEThibault/calendar-helper/blob/main/app/calendarAPI.py

# To Do:
- Figure out algorithm bug (specifically, adding tasks in the event of events on Fridays)
- System Test: test GC API to see if current app can access other account calendars
- Set up GH Actions