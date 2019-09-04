# Shorter

### An application for shortening and manage URLs.

* The user is able to create an account and log in;
* When the user doesn't log in, he can only create shorten urls;
* When the user logged in, he can create shorten urls and manage it: he can see a list of his created urls and he is able to edit and delete them;
* Each entry has author, origin url, shorten url, text, clicks, created date and expiration date;
* If the user didn't indicate shorten urls in creating, it will generate randomly;
* User can share short URLs with other users and in case they try to access it, they will be redirected to the original URL;
* The application counts the amount of short URL usage;
* The application uses a Queue to parse original URLs and store the text of the first html tag (p, span, h1-h6);
* Each text from finding an html tag is modify by the following way: after each word of six characters there should be an icon “TM”.
* Entry will remove from DB on the 14th day after its creation;
* The application is containerized via Docker/Docker compose;
* The application has an API for short URL creations.

#### Users:

* admin (password: admin)
* vladjkeee13 (password: vlad)


#### Installation && Launch
      
- Ports `5432, 8000, 6379` have to be available!
- Create an env file in the directory where located your application and write this value:
    `DB_PASSWORD=<some_password>`
- Build the Docker image via command `docker-compose build`.
- Start the project via command `docker-compose up`.
- Stop the project via command `docker-compose down`.


### Migrations and db dump 

- Up the docker
- Find the container with an application via command `docker ps`
- Go into the container and make migrations via command `docker exec -i -t <container_id> bash`
- Load fixtures to database via command `python manage.py loaddata fixtures/initial.json` (in the same container)