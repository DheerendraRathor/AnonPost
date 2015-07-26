# Anon_CMS

This is a anonymous comlaint management system with LDAP authentication backend. 

##Features
* To register posts anonymously*
* To discuss on post/issue with Administrators anonymously

*Note: The anonymity is for Administrators only i.e. Administrators cannot see who have registered the post, but the user details are saved in database so that misuse can be prevented

##Installation
###OS X
* Install [Homebrew](http://brew.sh/) if not already installed
* Install memcached by `brew install memcached` (Or follow this [tutorial](http://www.rahuljiresal.com/2014/03/installing-memcached-on-mac-with-homebrew-and-lunchy/) to configure memcahed with lunchy)
* Install postgresql by `brew install postgresql` (Or follow this [tutorial](http://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/) to configure postgresql with lunchy)
* (Optional) Install [pgAdmin](http://www.pgadmin.org/download/macosx.php) for UI based database configuration and database handling
* Install pip by `sudo easy_install pip`
* Start memcached and postgresql servers (If you've configured lunchy then you can just run commands like `lunchy start memcached`)

Note: One can work on other databases system like MySQL but using postgresql is strongly recommended and supported

####Setting Up Project
You can setup project in normal way but it is recommonded to setup project in a virtual environment to keep things neat and clean.
You can look into [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/index.html) for this purpose
* Install all dependencies by `pip install -r requirements.txt` (Run this command from project root)
* Go to anon_cms directory 
* Copy `settings_user.py.sample` to `settings_user.py`
* Edit essential parameters like `DB_NAME`, `DB_USER`, `DB_PASSWORRD` etc to your database configuration
* Go to project root and run `python manage.py migrate`
* Now start server using `python manage.py runserver` and go to [http://localhost:8000](http://localhost:8000)

##TODO:
* Writing installation instruction for Debian Linux based OS
* Adding file support in post registration
* ~~Creating interface for Administrator~~
