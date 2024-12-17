from decouple import config

db_config = {
    "dbname" : config("dbname"),
    "user" : config("user"),
    "password" : config("password"),
    "host" : config("host"),
    "port" : config("port"),
}