# ArtMan

### (Work in progress)
---
## Overview
Web application to manage CRUD operations on monthly reports and cargo specifications. Working environment - multiple users with various permissions on antarctic station.

##### Additional features:
- generate finished specification to pdf file,
- upload scans/photos,
- generate csv file for all specifications,
- generate finished specification to xlsx file (in progress),
- generate monthly report to pdf file (in progress).

## Main technologies:
- Python 3.6.8
- Django 2.2.4
- Bootstrap 4.3.1
- PostgreSQL

### Installation/Setup
- Create a virtual environment
- Install packages (requirements.txt needs to be cleaned - develop phase) using 
```sh
pip install -r requirements.txt
```
- Create database (and set it up in settings.py), then makemigrations and migrate
- You can populate database (currently only 'report' part) using
```sh
python manage.py runscript populate_report
```

### Basic workflow
After entering webpage you need to login and then it will display landing page. From there you can enter 'report' or 'cargo specification' subpage. 'Report' part allows you to create sections/subsections and notes for mentioned above. 'Cargo specification' part allows you to create/modify/delete specifications, upload files, generate pdf's.