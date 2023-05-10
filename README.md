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

# Development
- Use `npm run dev` and change Django settings.py `DEBUG` variable to `True`, change back to false before merging to main branch (deployment)
- To spin up containers:
Backend: `sudo docker build -t django-docker . && sudo docker run -d -p 8000:8000 django-docker`
Same thing for frontend, but container's called nextjs-docker. Make sure to stop and remove existing/running containers before building from the image again to save space.
