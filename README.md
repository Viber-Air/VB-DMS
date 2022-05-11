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

# Exemples

MODULE
```json
{
  "module_num"  : "34.B2.9F.A9",
  "module_type" : "Sensor",
  "asset"       : "Solar Panel",
  "sensor_type" : "P-Solar Panel"
}
```

RAW_DATA
```json
[
  {
    "module"      : "34.B2.9F.A9",
    "name"        : "VMPPT",
    "value"       : 3.29,
    "temperature" : 26,
    "voltage"     : 3.29,
    "timestamp"   : "2018-01-01 00:07:37"
  },

  {
    "module"      : "34.B2.9F.A9",
    "name"        : "VMPPT",
    "value"       : 3.28,
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:12:49"
  },

  {
    "module"      : "34.B2.9F.A9",
    "name"        : "VMPPT",
    "value"       : 3.29,
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:17:39"
  },

  {
    "module"      : "34.B2.9F.A9",
    "name"        : "VMPPT",
    "value"       : 3.29,
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:22:42"
  }

]
```

DATABATCH
```json
{
  "module"          : "34.B2.9F.A9",
  "window_size"     : 2,
  "raw_data_begin"  : "1",
  "raw_data_end"    : "4"
}
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

