PROBLEM DESCRIPTION
1. The aim is to create an endpoint to provide the average number of clicks, per country, within the last 30 days, for the Bitlinks in a user's default group.
2. To achieve this, we first require access_token from the user.
3. Once we get access_token, we place a request using URL https://api-ssl.bitly.com/v4/user to get users group_id.
4. We find bitlinks associated with this group_id using https://api-ssl.bitly.com/v4/groups/{group_id}/bitlinks
5. We then iterate through these bitlinks to get average number of clicks per country within last 30 days
6. In each iteration, we use json data from the API "https://api-ssl.bitly.com/v4/bitlinks/{link}/countries?unit=month&units=1" which provides us the metrics of clicks of the last month
7. We then create json data from the result and return the output.

REQUIREMENTS
Windows: You will need to download install latest python version from here https://www.python.org/downloads/

DEPENDENCIES
Once Python is installed, additionally we will need flask package to run the api. Open command prompt and install the package using below command
	pip install flask

GENERAL USAGE INFORMATION:
-> Download file DailyUserClickStatistics.py.
-> Open the file DailyUserClickStatistics.py using any editor(sublime, vscode, etc.) and update the "access_token" variable with appropriate value. Save the File
	Example: access_token = "abcedjawbukjefniueh"
-> Open command prompt. Navigate to the directory where you downloaded the file
-> Execute the file DailyUserClickStatistics.py using command: 
	python run.py
-> Open Url: http://localhost:5000/getMetric/ as endpoint to get required JSON output



