# SyncList
Webapp to sync users contact info with friends.

### Technologies
* Python 3
* Flask
* PostgreSQL
* HTML
* CSS
* Jinja2
* Bootstrap

### Instructions
<p>To run the app intially create a file named sercretconfig.cfg in the folder SyncList and add database uri details and your secret key</p>

#### Install required packages
`pip install -r requirements.txt`

#### Make Migrations
`python manage.py db init`

`python manage.py db migrate`

`python manage.py db upgrade`

#### Run Server
`python app.py`
