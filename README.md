# Introduction
This is a Flask Http server, which exposes a set of REST APIs to users. It provides service for football(well, you guys may call it soccer) team management. A sample Android app using this service can be found at [my other GitHub repo here.](https://github.com/CristianoYL/MY_TEAM_ANDROID)
# Configurations
## Dependencies
This service relies on serveral other services as well. For example, it uses [Flask_RESTful](https://flask-restful.readthedocs.io/en/latest/) for building REST APIs, [Flask_JWT](https://pythonhosted.org/Flask-JWT/) for tokenized authentication, [Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) for databse interaction etc.

A full dependency list could be found in the [requirement.txt file in this repo](https://github.com/CristianoYL/MY_TEAM_API/blob/master/requirements.txt)

And you may use the Python command to install all the required dependencies easily:
```
pip install -r requirements.txt
```
## Secrets
In order to deploy this service. You'll need to create a ```config.py``` file in the root folder that includes these secret entries:
```
# this file servers for AWS deployment or local testing
# if you wish to deploy on other platforms, please modify this file and the accordingly imports in your code
aws_db_name = <your AWS db name>
aws_db_username = <your AWS db username>
aws_db_password = <your AWS db password>
aws_postgresql_endpoint = <your AWS PostgreSQL database endpoint>
aws_mysql_endpoint = <your AWS MySQL database endpoint>

# construct the url for db driver using the above info
aws_postgresql_url = "postgresql://"+aws_db_username+":"+aws_db_password+"@"+aws_postgresql_endpoint+"/"+aws_db_name
aws_mysql_url = "mysql+pymysql://"+aws_db_username+":"+aws_db_password+"@"+aws_mysql_endpoint+"/"+aws_db_name

# if you want to test the database locally, modifies this url to match yours
local_mysql_url = "mysql+pymysql://<db username>:<db password>@<ip:port>/<db name>"
```

# API Reference
A detailed API Reference can be found in the [API Reference.md file in this repo](https://github.com/CristianoYL/MY_TEAM_API/blob/master/API%20Reference.md)

