# Exploring Baseball Pitches & Picth Data

This dockerized `python` `flask` API serves as the backend
for the [Exploring Pitch Data - baseball_ui][1] front end.

In Order to run it locally, please first check the requirements 
and follow the steps below:

1. Open a terminal window 
2. clone the repo using git clone
3. `cd` into the root directory of the repo
    * perform an `ls -l` command and verify you see `Dockerfile`, and `docker-compose.yml`
4. Execute the `make docker` command (defined in the Makefile)
    * If this is the first time you are running the app, the launch will take ~ `20 mins`
    * The app needs to import the data from the csv files into a 
      dockerized postgres database instance
    * The `docker-compose.yml` file references a volume that will be used every 
      subsequent run and speed up load times   
5. In the terminal, when you see `Up and ready!`, the API is ready
6. Included is a Postman Collection to hit the API directly
   * `Baseball API.postman_collection.json`

## Requirements

1. Docker
2. Docker Compose
3. The file `mlb_2021_pitches.csv` saved in the `app/utils` directory
4. The file `players.csv` also saved in the `app/utils` directory
#### Both files are critical to the application running.
#### If you need a copy of the files, please email me.

[1]: https://github.com/jeet-singh3/baseball_ui