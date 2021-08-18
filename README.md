# Flask Movie API[https://flaskmovieapi.herokuapp.com/](https://flaskmovieapi.herokuapp.com/)

It is a movies rest api developed using flask and sqlite.

Movie API is a web based REST API which can be used in various projects by web developers and even developers working on application development which needs to utilize any feature of IMDb website. This API will enable developers to get data according to their needs in an easy to read javascript object-notation (JSON) format.

## Project Directory Structure
```
|flask_movie_api    #Project Directory
|  
|--.github          
|--|--workflows          #Github Actions workflow for CodeQL
|--|----codeql.yml       #yaml code for the CodeQL Workflow
|
|--app                 #Main flask app directory
|  |--data               #Data directory for data storage
|  |  |--db_*.db
|  |  |--movies.json      #Initial Load File
|  |
|  |--logs               #Logs Directory
|  |--|--log_files      
|  |--|--|--*_debug_movies_api.log
|  |
|  |--main               #Main application directory
|  |  |--__init__.py
|  |  |
|  |  |--controller       #Controller files module
|  |  |  |-- __init__.py
|  |  |  |--*_controller.py
|  |  |
|  |  |--model            #Model files module
|  |  |  |-- __init__.py
|  |  |  |-- *model-name.py
|  |  |
|  |  |--service          #Service files module
|  |  |  |--__init__.py
|  |  |  |--*_service.py
|  |  |
|  |  |--util             #Utility files module
|  |     |--__init__.py
|  |     |--dto.py         #data transfer object 
|  |     |--decorator.py   #decortor definition
|  |
|  |--test               #Test Module
|     |-- __init__.py
|     |--test_*.py
|
|--migrations           #Migrations 
|--.gitignore           #git ignore file
|--manage.py            #mange file to run, test the app
|--wsgi.py              #Entry point for the app
|--Procfile             #gunicorn file for deployment
|--runtime.txt          #python runtime version for heroku deployment 
|--Pipfile              #Pipenv - python dependencies
|--requirements.txt     #packages 

```

### Installation

1. Get a free account at [https://dashboard.heroku.com/](https://dashboard.heroku.com/)

2. Clone the repo
   
   ```sh
   git clone https://github.com/bhargavjagan/flaskmovieapi.git
   ```

3. Install Python packages

   ```sh
   pipenv install
   pipenv shell
   pip install -r requirements.txt
   ```

4. Make DB Migrations

   ```
    flask db init
    flask db migrate
    flask db upgrade
   ```

4. Run the application and open https://localhost:5000
   ```
    python manage.py run
   ```


### Terminal commands
Note: make sure you have `pip` and `virtualenv` installed.

    To initialize a pipenv: pipenv install | pipenv install flask | pip install -r requirements.txt

    For python shell: pipenv shell

    To run application: python manage.py run | python wsgi.py | flask run

    To run test: python manage.py test

    To load the inital data: python manage.py load_data

    For help: python manage.py --help


Make sure to run the initial migration commands to update the database.
    
    > flask db init

    > flask db migrate --message 'initial database migration'

    > flask db upgrade

In case there is not update to the database, use the below command 
    
    > flask db stamp head


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/

    Create a user for youself using the endpoint [POST] '/api/v1/user/' which on success return the token.

    Copy the token and append 'Bearer ' to the begining and paste it in the value of the authenticate.
        'Bearer <JWT_token>'


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

### Deployement in Heroku

    Download the heroku CLI [https://devcenter.heroku.com/articles/heroku-command-line](https://devcenter.heroku.com/articles/heroku-command-line)

    After the installation, login to the heroku using the command below.
        ```heroku login```

    Clone the repository
        ```
        heroku git:clone -a flaskmovieapi
        cd flaskmovieapi
        ```
    
    Deploy your changes
        ```
        git add .
        git commit -am "make it better"
        git push heroku master
        ```
    Reference for Heroku Deployment [https://dashboard.heroku.com/apps/flaskmovieapi/deploy/heroku-git](https://dashboard.heroku.com/apps/flaskmovieapi/deploy/heroku-git)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Bhargav Dadi [Github](https://github.com/bhargavjagan)

Project Link: [https://github.com/bhargavjagan/flaskmovieapi.git](https://github.com/bhargavjagan/flaskmovieapi.git)

