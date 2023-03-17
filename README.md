# booking

bird fans platform

for update project:
> git pull && docker-compose down && docker-compose up -d --build && watch -x docker ps

You can use virtualenv like this:
> sudo apt install virtualenv
> virtualenv env
> . ./env/bin/activate
> python manage.py migrate

Then write fake database with by this command
> python mange.py fake_data

Also, you can check tests:
> python mange.py test


For start Local:
> sudo apt install gettext

for create locale:
> python manage.py makemessages -l

for update locale:
> python manage.py makemessages -a

for compile locale:
> python manage.py compilemessages -f

