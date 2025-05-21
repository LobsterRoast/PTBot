# PTBot
This is a python bot to automatically provide simple statistics on minecraft server playtime and write them to an excel sheet.

# Installation
- Clone the repository to your server
- Run `pip install -r requirements.txt`
- Make sure to set the PTBOT_PATH and PTBOT_IP environment variables
  - The former should be the path on your server to an excel spreadsheet. The latter is the server you want to monitor
- Ensure your excel spreadsheet has a worksheet named "Data"
  - Alternatively, edit the source code of the bot to whichever worksheet name you desire. 
- Run the bot using `python main.py`
- Optionally, you can go into the source code and change the timezone. EST is used by default.
