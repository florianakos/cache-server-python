# cache-server-python

A simple service written in `Python` that uses `AWS DynamoDB` to cache responses from `VirusTotal`.

For authorization to VirusTotal API, there is a `.env` file which loads the API key into the app container as **VT_API_KEY** env variable.

The setup can be run via docker-compose:

```
docker-compose up --build --abort-on-container-exit
```