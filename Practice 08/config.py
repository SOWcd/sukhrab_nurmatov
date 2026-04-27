db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "mysecretpassword"
}

#docker run --name pg-phonebook -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
#docker exec -i pg-phonebook psql -U postgres -d postgres < 01_tables.sql
#docker exec -i pg-phonebook psql -U postgres -d postgres < functions.sql
#docker exec -i pg-phonebook psql -U postgres -d postgres < procedures.sql
#python phonebook.py

#остановить
#docker stop pg-phonebook
#docker rm pg-phonebook

#pip install psycopg2-binary