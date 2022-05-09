# WP-DataServices
Data Manipulation Service &amp; Analytics and EDA for Data Scientists

# Setup

## To do before production stage
- Changes at api/config/settings.py:
  - Change SECRET_KEY
  - DEBUG = False

## Running
```bash
git clone git@github.com:alom101/WP-DataServices.git
cd WP-DataServices
sudo docker-compose up --build -d
```

## Adding a super user
```bash
sudo docker exec -it data-services sh
python api/manage.py createsuperuser
```

## Adding a normal user
```
http://localhost:8000/admin/auth/user/add/
```


# Dev info

## Folder structure
```
WP-DataServices
    |_api                 Django project
    |   |_api             Django app - the actual api code
    |   |_config          Django main app
    |   |_run.sh          Entrypoint for the api container
    |_Dockerfile          To build the api container
    |_docker-compose.yml  To link the api and mongo containers
    |_requirements.txt     Requirements for the api container
```

## Persistent Data
Docker Volumes mapped to:
- /var/WP/WP-DataServices_DB
- /var/WP/WP-DataServices_config

