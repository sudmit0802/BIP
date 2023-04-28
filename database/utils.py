import psycopg2
import sqlparse
import os

postgres_ctx = {
    "host": "localhost",
    "database": "lab_manager_database",
    "user": "postgres",
    "password": "0802"
}

def get_connection(ctx):
    return psycopg2.connect(
    host=ctx['host'],
    database=ctx['database'],
    user=ctx['user'],
    password=ctx['password']
    )