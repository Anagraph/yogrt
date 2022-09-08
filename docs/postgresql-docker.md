# Create dev instance of PostgreSQL using docker

##


```bash
docker pull postgis/postgis:14-3.2
docker run -e  POSTGRES_PASSWORD=mypassword -p 5432:5432 postgis/postgis:14-3.2
```