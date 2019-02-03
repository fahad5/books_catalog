Item Catalog Web App
This web app is a project for the Udacity https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

This project is a RESTful web application utilizing the Flask framework which accesses a SQL database 
that populates categories and their items. OAuth2 provides authentication for further CRUD 
functionality on the application. Currently OAuth2 is implemented for Google Accounts.


To work in this project you should indtall 
Vagrant :https://www.vagrantup.com/
Udacity Vagrantfile :https://github.com/udacity/fullstack-nanodegree-vm
VirtualBox :https://www.virtualbox.org/wiki/Downloads

How to install :
1- install virtualbox 
2- install vagrant
3- clone Udacity Vagrantfile to folder
4- go to that folder 
5- vagrant up
6- vagrant ssh

Please make sure that you have all required packages installed:

flask
google-auth-httplib2
google-api-python-client
sqlalchemy



How to use :
1-from udacity-catalog-project folder run vagrant with vagrant up then vagrant ssh
2- cd /vagrant/udacity-catalog-project
3- run "python database_setup.py"
4- run "python seeder.py"
5- run "python application.py"
6- go to http://localhost:5000/
