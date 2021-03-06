## cornershop-backend-test

### Stack & Technologies

- backend
    * Docker
    * Python 3.8
    * Django
    * PostgreSQL
    * Redis
    * Jupyterlab
    * Recaptcha

- frontend
    * Bootstrap
    * [SB Admin](https://startbootstrap.com/theme/sb-admin-2)
    * Jquery
    * Select2


### Libraries & 3rd parties
* Django restframework
* Swagger
* Flake


### API Rest doc

* Local: http://127.0.0.1:8000/swagger/


## App structure tree
```
|__ account
    |__ bl (bussiness logics)
        |__ utils.py (utility functions)
    |__ fixtures (default users json)
    |__ templates (html)
        |__ emails (email templates html)
        |__ ...others html
    |__ forms.py (login and signup forms)
    |__ models.py
    |__ factories.py (creational class for User)
    |__ tests.py (unit and integration tests)
    |__ urls.py (urls related to account management)
    |__ views.py
|__ api
    |__ tests
        |__ integration
            |__ tests_*.py
        |__ mock.py  (custom mock functions/classes/data)
    |__ views.py
    |__ urls.py
|__ backend_test
    |__ ...config py files
    |__ tasks.py  (celery tasks)
|__ bin  (utility bash scripts)
    |__ *.sh (bash scripts)
|__  common-templates (general purpose templates html)
|__  dashboard
    |__ bl (bussiness logics)
        |__ bot.py (class for parsing a msg and send an slack notification)
        |__ data.py (data structures, constants)
        |__ utils.py (utility functions)
    |__ fixtures (default meals and menu json)
    |__ templates (html)
        |__ ...others html
    |__ tests
        |__ integration
            |__ tests_*.py
        |__ unit
            |__ tests_*.py
        |__ mock.py  (custom mock functions/classes/data)
    |__ context_processor.py (global variables in templates)
    |__ models.py
    |__ factories.py (creational classes for Meal and Menu)
    |__ managers.py (override objects)
    |__ urls.py (urls related to menu and order for employees)
    |__ serializers.py (django-restframework model handlers: used for api)
    |__ signals.py (a post_save signal for menu model)
        |__ def schedule_menu (used to create a async celery task)
    |__ views.py
|__  menu (public sites for employees' actions)
    |__ bl (bussiness logics)
        |__ utils.py (utility functions)
        |__ data.py (data structures, constants)
    |__ fixtures (default order json: used for testing)
    |__ templates (html)
        |__ ...others html
    |__ tests
        |__ integration
            |__ tests_*.py
        |__ unit
            |__ tests_*.py 
    |__ exceptions.py (invalid form handlers)
    |__ forms.py (order forms)
    |__ models.py
    |__ urls.py (urls related to menu and order for employees)
    |__ views.py
|__  static (all css, js, imgs files used in templates)
    |__ ...others files
    |__ sba2 (boostrap admin 2 template) 
```


## Setting up!

### IMPORTANT: Complete environment vars defined in env.example
```
RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
SLACK_OAUTH_TOKEN=
SLACK_CHANNEL=
```

### Copy env.example into .env in same folder
- `cp env.example .env`

### Running the development environment

* `make up`

### After creating development environment
* Run inside backend container: `sh bin/init-migrations.sh`
* Run inside backend container: `sh bin/load-init.sh` 
m* Run inside backend container: `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

### Run all tests

* Run inside backend container: `sh bin/run-tests.sh`

### Run coverage

* Run inside backend container: `sh bin/run-coverages.sh report_name_file.txt`

### Run celery

* Run inside backend container: `/docker-entrypoint.sh celery`

### About schedule a Menu

* in backend_test/settings.py you can change these values

```
# 9:15 AM
SCHEDULE_MENU_TIME = {
    "hours": 9,  # use: 0 to 23
    "minutes": 15,  # use: 0 to 59
}

# 11:00 AM
MAX_HOUR_TO_ORDER = 11  # use: 0 to 23
UTC_TZ_OFFSET = -4  # for chile
```

* It's used as follow:
    - SCHEDULE_MENU_TIME it's the time when notification is 
    about to trigger if you schedule the menu days before (Create button)
    
    - If you create a menu for the current date (TODAY) or in the past (weird case), 
    it'll omit SCHEDULE_MENU_TIME and notification will be sent 5 minutes later.
    
    - If you set MAX_HOUR_TO_ORDER, it's the time to validate an order for employees
    past the time, it throws an exception message in form "Not valid time"
    - UTC_TZ_OFFSET is used to change the UTC time. It's a lazy way to handle dates but it works for now.
    
    - Note: Please use valid numbers as shows in comments