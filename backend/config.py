import os
import random


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL") or "sqlite:///../data/salary.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "".join([chr(random.randint(65, 92)) for _ in range(50)])
