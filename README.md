# P12_secure_backend_architecture_with_Django_ORM
Project 12 on 13 of my training to complete my formation as Python application developer

#### This API is the 12th project of a training to obtain a diploma

The aim of this API is to create a CRM to be used internally by the company. 
This API must be secured with a PostgresQL database and Django Rest Framework.
The company is separated in three teams, the sales team, the support team and the management team.  
The goals are to:  
* create two groups of users, the sales team and the support team with different permissions
* use the Django Rest Framework Admin site for the two groups of users as a front-end 
* sales team can:  
    * view, create possible clients and update data and status
    * view, create and update contracts between client and sales person
    * view and create one event linked with a contract signed with a client
* support team can:  
    * view all clients
    * view all contracts
    * view all events and update event linked with the support person dedicated to it


## Installation

This locally-executable API can be installed using the following steps.

### Installation and execution using venv and pip

1. Clone this repository using `$ git clone https://github.com/oliviersamin/P12_secure_backend_architecture_with_Django_ORM.git` (you can also download the repo [as a zip file](https://github.com/oliviersamin/P12_secure_backend_architecture_with_Django_ORM/archive/refs/heads/main.zip))
2. Move to the P12_secure_backend_architecture_with_Django_ORM folder with `$ cd P12_secure_backend_architecture_with_Django_ORM`
3. Create a virtual environment for the project with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
4. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. perform migrations with `$ python manage.py migrate`
7. Run the server with `$ python manage.py runsslserver`

When the server is running after step 7 of the procedure, the API can be requested from endpoints starting with the following base URL: https://127.0.0.1:8000/api/

Steps 1, 3, 5 and 6 are only required for initial installation. For subsequent launches of the API, you only have to execute steps 4 and 7 from the root folder of the project.

## Usage and detailed endpoint documentation
The API can be used from:
* your Web browser using the native DRF browsable API via the URL: https://127.0.0.1:8000/management/  
Some users have already been created and can be used to navigate through the API:
  * administrator user: login:admin1 - password: passwd_admin1 
  * salesman users:
    1. login: sales1  -  password: passwd_sales1  
    2. login: sales2  -  password: passwd_sales2  
    3. login: support1  -  password: passwd_suport1  

  You can then access to all the actions allowed by the role you logged in  
* Postman for example  
You can read the documentation of the API [here](https://documenter.getpostman.com/view/16015714/UVJfhucy).


#### list of all the action to perform, method to use and the associated URI
| ACTION PERFORMED | METHOD | URI |  
| ---------------- | ----------- |  ----------- | 
| User login | POST | api/login/ |  
| User refresh token | POST | api/login/refresh/  |  
| Get the list of all clients | GET | api/clients/ |  
| Create a client | POST | api/clients/ |  
| Search a client by client details | GET | api/clients/ |
| Get a client details | GET | api/clients/{client_id} |  
| Update a client | PUT | api/clients/{client_id} |  
| Get the list of all contracts | GET | api/contracts/ |  
| Create a contract | POST | api/contracts/ |  
| Search a contract by client or contract details | GET | api/contracts/ |
| Get a contract details | GET | api/contracts/{contract_id} |  
| Update a contract | PUT | api/contracts/{contract_id} |
| Get the list of all events | GET | api/events/ |  
| Create an event | POST | api/events/ |  
| Search an event by client contract or event details | GET | api/events/ |
| Get an event details | GET | api/events/{event_id} |  
| Update an event | PUT | api/events/{event_id} |
| Logout | POST | api/logout/ | 


