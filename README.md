![apresentation-tip](https://github.com/WandersoNoleto/SmartOrient/blob/main/documentation/Doc-tip.png)

## SmartOrient [![NPM](https://img.shields.io/npm/l/react)](https://github.com/WandersoNoleto/SmartOrient/blob/main/LICENSE) 


## About

SmartOrient is an open-source, web-based management solution for academic thesis guidance. The proposal is to bring together functionalities that encompass the entire process of managing guidance within a single platform, eliminating the need for multiple tools. The application caters to three types of users: 
* Student - can view and register projects, attach files
* Advisor - can view projects they are a part of, accept participation requests, read attached files
* Coordination - responsible for overseeing all actions carried out by other parties

### :clipboard: Tecnologies and Tolls
* Python
* Django - Web framework
* PostgreSQL - SGBD
* [AdminLTE](https://github.com/ColorlibHQ/AdminLTE) - dashboard template based on Bootstrap 5
* [PDF.js](https://github.com/mozilla/pdf.js) - PDF Reader in JavaScript

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 



What things you need to install the software and how to install them

First, clone the repository
```
git clone https://github.com/WandersoNoleto/SmartOrient.git
```
Install the dependencies listed in the requirements.txt file
```
pip install > requirements.txt
```
###### :key: Create a .env file and set the variables according to the [.env.example](https://github.com/WandersoNoleto/SmartOrient/blob/main/smartorient/.env.example). Create a PostgreSQL database named SmartOrient and set the USER and PASSWORD accordingly. In case of issues, check settings.py. 
Generate a new Django key and assign it to SECRET_KEY (in Python CLI)
```
from django.core.management import utils
print(utils.get_random_secret_key())
```

Use the command to run the service
```
python3 manage.py runserver
```

