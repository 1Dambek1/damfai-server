import datetime


a = (datetime.datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0) - datetime.datetime.now(datetime.timezone.utc)).days
print(a)