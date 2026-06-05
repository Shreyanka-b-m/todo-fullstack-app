from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://todo_user:todo123@localhost/todo_app"

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