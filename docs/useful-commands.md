# Commonly used commands for development

## Update persistence

### Update migration information

```shell
docker-compose run osmaxxwebappdev /bin/bash -c 'python3 manage.py makemigrations'
```

### Run migrations on database
```shell
docker-compose run osmaxxwebapp /bin/bash -c 'python3 manage.py migrate'
```


## Run tests
```shell
docker-compose run osmaxxwebappdev /bin/bash -c 'python3 manage.py test'
```


## Use backend

### Create superuser

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py createsuperuser'
```

### Update locales
Please update locales only on release. Otherwise you will get huge diffs in feature pull requests.

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py makemessages -a'
```