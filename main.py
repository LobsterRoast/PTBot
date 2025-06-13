# PTBot
# Written by LobsterRoast
# MIT License

from mcstatus import JavaServer
from openpyxl import Workbook, load_workbook
import datetime
import os

# ---------------------------------------------------------------------------------
# The path of the excel spreadsheet to write to and the IP of the server to monitor
# are in PTBOT_PATH and PTBOT_IP respectively
# ---------------------------------------------------------------------------------

path = os.environ["PTBOT_PATH"]
ip = os.environ["PTBOT_IP"]

print("Loading OneDrive data...")
os.system(f"rm {path}")
os.system("onedrive --sync")
print("Success.\n")

print("Loading worksheet...")
wb = load_workbook(path)
# ---------------------------------------------------------------------------------
# "Data" can be changed to whatever you wanna call your worksheet.
# ---------------------------------------------------------------------------------
ws = wb["Data"]
print("Success.\n")

# ---------------------------------------------------------------------------------
# For some reason, initializing a datetime with a tzinfo doesn't actually change
# the timezone it uses. You have to pass the timezone into individual calls from
# the datetime object. So here's a convenient function to get EST time. It can
# be easily changed to any timezone just by changing the timedelta.
# ---------------------------------------------------------------------------------
tz = datetime.timezone(datetime.timedelta(hours = -5), "EST")
dt = datetime.datetime(1, 1, 1, tzinfo=tz)
print(f"Operating using {tz.tzname(dt)} time.")
def tz_now():
	global tz
	return datetime.datetime.now(tz)

day = tz_now().day
minute = tz_now().minute
elapsed_seconds = 0
last_polled_time = tz_now()
server = JavaServer.lookup(ip)
status = server.status()
player_count = status.players.online
daily_playtime = 0
server_online = True

def write_to_file():
	global day
	global path
	global elapsed_seconds
	global wb
	global ws
	now = tz_now()
	date = f"{now.year}-{now.month}-{now.day}"
	increment()
	ws.append([date, elapsed_seconds/60])
	wb.save(path)
	day = now.day
	elapsed_seconds = 0
	os.system("onedrive --sync")
	

def increment():
	global last_polled_time
	global elapsed_seconds
	now = tz_now()
	timedelta = now - last_polled_time
	elapsed_seconds += timedelta.total_seconds() * player_count
	last_polled_time = now
while(True):
	if day is not tz_now().day:
		print("Date rollover detected. Writing latest statistics to excel spreadsheet")
		write_to_file()

# ---------------------------------------------------------------------------------
# To avoid constantly querying the server and incrementing the playtime, this bot
# simply checks every minute for changes to the player count. If there's a change
# in player count, it increments elapsed_seconds by:
# 	(player count before change) * (timedelta since previous increment)
# The results of this won't be exact, but they'll be close enough to paint a
# general picture of player activity.
# ---------------------------------------------------------------------------------

	if minute is not tz_now().minute:
		minute = tz_now().minute
		try: 
			status = server.status()
			server_online = True
		except:
			server_online = False
			player_count = 0
			continue
		if status.players.online is not player_count:
			now = tz_now()
			current_time = f"{now.hour}:{now.minute}:{now.second}"
			print(f"[{current_time}] Player count changed. Incrementing elapsed time. Player count is now {status.players.online}.")
			increment()
			player_count = status.players.online
			

