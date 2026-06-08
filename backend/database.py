# from sqlalchemy import create_engine

# DATABASE_URL = "mysql+pymysql://root:UadUquLmjNCxjRBifsAUMgFKVMVHlUoB@acela.proxy.rlwy.net:30999/railway"


# engine = create_engine(DATABASE_URL)

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


# Let's Understand This URL
# mysql+pymysql://

# Use MariaDB/MySQL driver

# todo_user

# Database username

# todo123

# Password

# localhost

# Database server location

# todo_app

# Database name