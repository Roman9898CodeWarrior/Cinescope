import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    EMAIL = os.getenv('SUPER_ADMIN_EMAIL')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

class DBCreds:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

