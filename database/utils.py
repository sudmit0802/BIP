import psycopg2
import sqlparse
import os

postgres_ctx = {
    "host": "localhost",
    "database": "lab_manager_database",
    "user": "postgres",
    "port": "5433",
    "password": "shizal"
}

def get_connection(ctx):
    return psycopg2.connect(
    host=ctx['host'],
    database=ctx['database'],
    user=ctx['user'],
    port=ctx['port'],
    password=ctx['password']
    )