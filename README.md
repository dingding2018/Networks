# Network Project
[![Build Status](https://travis-ci.org/dingding2018/Networks.svg?branch=master)](https://travis-ci.org/dingding2018/Networks)

# About
This repo is for the project of Network class.
The website is built using Python, Flask and mySQL.

# Website Fuctions (for the moment)
- User registration/login/logout
- Post a topic
- Comment on a topic
- Search by keyword
- Automated underwriting demo
- Browser info about insurance

# How to run the codes in your local PC
1. Required installations
- Python 2.7
- Flask
- SQLAlchemy
- PyMySQL
- Flask-Migrate
- Virtualenv
- Pycharm (optional)
- Gitbash: https://git-scm.com/download

2. Download the repo from github and run
```shell
git clone https://github.com/dingding2018/Networks.git
cd File/
python auw_demo.py
```
Go to the brower and input:
http://127.0.0.1:5000 or localhost:5000
The webpage should be running.

3. Database
Since the service is running on local, you still need to make sure the database is available on your local PC.

(1) Setup (please do it under virtual flask env)
```shell
cd File/
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
(2) Open mySQL command line
- Input the password "root" to enter the database
- SQL command lines to check the tables in database
```shell
CREATE DATABASE test_demo;
use test_demo;
show tables;
desc user; (check the columns in table "user")
select * from user; (check the information stored in the table "user")
```
