from django.contrib.auth.models import User
from base.models import Task, UserProfile
from django.utils.timezone import make_aware
import datetime


# ensure start and end times are logical
def validate_time(preferred_start, preferred_end):
    if (
        preferred_start < 0
        or preferred_start > 24
        or preferred_end < 0
        or preferred_end > 24
        or preferred_end < preferred_start
    ):
        return False
    else:
        return True


# store a task in the db + validate
def store_tasks(data):
    tasks = data["tasks"]
    user = None
    # User validation check / length validation
    try:
        user = User.objects.get(username=data["user"])
        for task in tasks:
            if int(task["length"]) > 24:
                return False

            Task.objects.create(
                user=user,
                name=task["name"],
                length=int(task["length"]),
                start=None,
                end=None,
            )
    except:
        return False  # user does not exist for one or more tasks
    return True


"""
    algorithm to find optimal task schedule
    parameters:
        - username: str, name of the user so we can query db for the tasks they want to do
        - events: list[] of events that the user already has in their calendar for the next week
    It populates the start and end fields for each of the user's tasks, then bundles 
    em into a schedule obj to return to the client
"""


def find_schedule(username, events):
    # start by getting the tasks from the db
    user = User.objects.get(username=username)
    tasks = Task.objects.filter(user=user).order_by(
        "-length"
    )  # sort from longest to shortest
    profile = UserProfile.objects.get(user=user)
    preferred_start = profile.preferred_start
    preferred_end = profile.preferred_end

    """
    At this point, we have the tasks: what the user wants us to find room for
    And we have existing tasks (events) that are already in their calendar.
    Need to find time, considering preferred_start and end constraints, to complete the tasks in the most efficient way possible

    Constraints:
    - Cannot skip the events, you can skip the tasks if it's impossible to add them in
    - Algorithm: always select the next possible task that ends as early as possible, without comprimising the calendar events
    """
    now = datetime.datetime.utcnow()
    event_datetimes = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        try:
            # Format of start and end: 2023-05-05T08:00:00-04:00
            start_dt = datetime.datetime.strptime(
                start.replace("-" + start.split("-")[-1], ""), "%Y-%m-%dT%X"
            )
            end_dt = datetime.datetime.strptime(
                end.replace("-" + end.split("-")[-1], ""), "%Y-%m-%dT%X"
            )
            event_datetimes.append(
                {"start": start_dt.hour, "end": end_dt.hour, "day": start_dt.day}
            )
        except:
            # If that throws exception: it's an all-day event, format is: 2023-05-13
            start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")
            event_datetimes.append({"start": 0, "end": 0, "day": start_dt.day})

    # Go one day at a time: 7 days total
    used = [0] * len(tasks)
    for day in range(1 + now.day, 8 + now.day):
        i = 0
        day_events = []
        """
            here we're collecting the events that are happening on that day, and we're keeping track of their start and end dates:
            The structure is this day_events = [ (Full event information from API, Event start and end dates), ... ]
        """
        for event in event_datetimes:
            if day == event["day"]:
                day_events.append((events[i], event))
            i += 1

        # Now that we have the events that are happening on this day, we check to see if we can fill in any tasks in there
        # Sort these events from earliest start to latest start
        if len(day_events) > 0:
            # there is at least 1 event from the calendar
            # sort these calendar events based on start time as well
            sorted(day_events, key=lambda x: x[1]["start"])

            # idea: find all empty slots between preferred_start - preferred_end
            # Once we find the slot, find the largest task we can fill it in
            slot_size = 0
            i = 0
            curr_time = preferred_start

            while i < len(day_events) and curr_time < preferred_end:
                if day_events[i][1]["start"] > curr_time:
                    slot_size += 1
                    curr_time += 1
                else:
                    j = 0
                    for task in tasks:
                        if task.length <= slot_size and used[j] == 0:
                            print(task.name + ": ")
                            task.start = make_aware(
                                datetime.datetime(
                                    now.year, now.month, day, curr_time - slot_size
                                )
                            )
                            task.end = make_aware(
                                datetime.datetime(
                                    now.year,
                                    now.month,
                                    day,
                                    task.start.hour + task.length,
                                )
                            )
                            task.save()
                            used[j] = 1
                            break
                        j += 1
                    curr_time += slot_size
                    slot_size = 0
                    i += 1
        else:
            # we have all day, squeeze as many tasks as you can in this day between preferred_start and preferred_end
            curr_time = preferred_start
            slot_size = 0

            while curr_time < preferred_end:
                task_len = 0
                j = 0
                temp = 0
                for task in tasks:
                    if task.length <= slot_size and used[j] == 0:
                        task.start = make_aware(
                            datetime.datetime(
                                now.year, now.month, day, curr_time - slot_size
                            )
                        )
                        task.end = make_aware(
                            datetime.datetime(
                                now.year, now.month, day, task.start.hour + task.length
                            )
                        )
                        task.save()
                        task_len = task.length
                        temp = task.end.hour
                        used[j] = 1
                        j += 1
                        break
                    j += 1
                if task_len > 0:
                    curr_time = temp
                    slot_size = 0
                else:
                    curr_time += 1
                    slot_size += 1

    final_tasks = Task.objects.filter(user=user)
    schedule = {"tasks": []}
    for task in final_tasks:
        schedule["tasks"].append(
            {
                "name": task.name,
                "length": task.length,
                "start": task.start,
                "end": task.end,
            }
        )

    return schedule
