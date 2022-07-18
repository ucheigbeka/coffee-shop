import os
from dotenv import load_dotenv
from .api import app

project_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(project_dir, '..', '.env')

load_dotenv(dotenv_file)
