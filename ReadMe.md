--------------------
Description
--------------------

The goal of this app is to monitor changes and issue MTA status updates, while providing an api to request uptimes and delays.

Possible improvements:
- Set up proper multiprocessed system for requesting data with gunicorn, so that the app works at scale
- Improve testing, use a well formatted protobuf sample instead of sample_gtfs.py

--------------------
Requirements/ Startup
--------------------
- Requires Python 3.7.2, tested on macOS Mojave
- run with
```
sh startup.sh
```

--------------------
Testing
--------------------
- run unit/ integration tests with
```
sh startup.sh test
```

--------------------
Endpoints
--------------------
```
/uptime
```
Http Method: GET
Parameters: line => String
Response: JSON
Response Codes: 200, 400

Sample 200 Response:
```
{
  uptime: 0.63
}
```
Sample 400 Response:
```
{
    "error": "Invalid subway line"
}
```
--------------------
```
/status
```
Http Method: GET
Parameters: line => String
Response: JSON
Response Codes: 200, 400

Sample 200 Response:
```
{
  "status": "delayed"
}
```
```
{
  "status": "not delayed"
}
```
Sample 400 Response:
```
{
    "error": "Invalid subway line 'RSD'"
}
```
