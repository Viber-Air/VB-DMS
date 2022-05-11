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
    "measures"    :[
                    {
                      "name"        : "VMPPT",
                      "value"       : 3.29
                    }
                  ],
    "temperature" : 26,
    "voltage"     : 3.29,
    "timestamp"   : "2018-01-01 00:07:37"
  },

  {
    "module"      : "34.B2.9F.A9",
    "measures"    :[
                    {
                      "name"        : "VMPPT",
                      "value"       : 3.28
                    }
                  ],
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:12:49"
  },

  {
    "module"      : "34.B2.9F.A9",
    "measures"    :[
                    {
                      "name"        : "VMPPT",
                      "value"       : 3.29
                    }
                  ],
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:17:39"
  },

  {
    "module"      : "34.B2.9F.A9",
    "measures"    :[
                    {
                      "name"        : "VMPPT",
                      "value"       : 3.29
                    }
                  ],
    "temperature" : 26,
    "voltage"     : 3.28,
    "timestamp"   : "2018-01-01 00:22:42"
  }
]
```


# Dev info

## Folder structure
```
WP-DataServices
    ├─api                 Django project
    │  ├─ api             Django app - the actual api code
    │  ├─ config          Django main app
    │  └─ run.sh          Entrypoint for the api container
    ├─ Dockerfile          To build the api container
    ├─ docker-compose.yml  To link the api and mongo containers
    └─ requirements.txt     Requirements for the api container
```

## Persistent Data
Docker Volumes mapped to:
- /var/WP/WP-DataServices_DB
- /var/WP/WP-DataServices_config

## Parallel Processing

Done inside the api_databatch() function:

```
                                       process_databatch()
                      ┌ rawbatch#1 ────────────────────────> databatch#1 ┐
             split    │                                                  │    
raw_datas────────────>├ rawbatch#2 ────────────────────────> databatch#2 ├────────────> response
                      │                                                  │
                      └ rawbatch#3 ────────────────────────> databatch#3 ┘
```