# Technical test: Weather API

## Install Instructions

1. Clone repo

    ```bash
    $ git clone git@github.com:rmaceissoft/weather-api-test.git
    ```

2.  Create .env file and replace values saying `CHANGEME!!!`

    Note:
    - Use this [generator](https://djecrety.ir/) for django' SECRET_KEY.
    - Click [here](https://home.openweathermap.org/api_keys) to obtain an OpenWeatherMap API KEY 
    
    ```bash
    $ cp env.dist .env
    $ vi .env
    ```
    
3. Build and spin up local containers
    ```bash
    $ docker-compose up -d
    ```

4. Apply migrations
    ```bash
    # run the following command
    $ docker-compose exec web python manage.py migrate
    ```

5. That's all. Hit the following url from a browser
    
    http://localhost:8000/weather?city=Lima&country=pe
    
## Test from Heroku

This project has also been deployed to heroku:

https://weather-api-test-demo.herokuapp.com/weather?city=Lima&country=pe 


## Running tests

Unit tests are implemented with [pytest](https://docs.pytest.org/). In order to execute them
try the following command from another terminal
    
```bash    
pytest
```     

## TODOs / Improvements:

- Reuse the python library [pyowm](https://pypi.org/project/pyowm/) instead of the custom class `app.weather.utils.OpenWeatherMapClient`.
