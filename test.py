import datetime
start_running_date =datetime.datetime.now(datetime.timezone.utc)
print(start_running_date.tzinfo)
start_running_date = start_running_date.astimezone(datetime.timezone.utc).replace(tzinfo=None)
print(start_running_date)

