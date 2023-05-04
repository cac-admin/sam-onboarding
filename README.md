# cac-onboarding

## IDEAS
- Task Scheduling Algorithm (Greedy), with GC API
- Auto Tab and Application Opener: - Path\To\Chrome\chrome.exe superuser.com stackoverflow.com ...
	Just make them create an account, enter their browser exe path, and then create sessions with different automations
	Would need to bundle executable windows application, so not rly web app

## STACK
- Django (REST), check for db options
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
- User can edit, or confirm (Next)
- Django then takes edited or confirmed data and sends a POST to GC API to populate user calendar

https://github.com/SamEThibault/calendar-helper/blob/main/app/calendarAPI.py

# To Do:
- Test Google Calendar API
- Write scheduling algorithm
- Design UI
- Design endpoints
- Write Schema (from Figma)
- Test Auth
- Fetch from Next
- System Test
- Deploy if time permits

