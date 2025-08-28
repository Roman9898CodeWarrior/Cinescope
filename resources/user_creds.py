import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    EMAIL = os.getenv('SUPER_ADMIN_EMAIL')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')