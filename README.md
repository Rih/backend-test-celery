## cornershop-backend-test

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


