import os
from dotenv import load_dotenv

load_dotenv()

class ChromiumPath:
    CHROMIUM_PATH = os.getenv('CHROMIUM_PATH')