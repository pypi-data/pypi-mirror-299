import json
import os
import shutil
import string
from datetime import timedelta, datetime
from typing import List
import random

def generate_date_range(day_from: datetime, day_to: datetime) -> List[datetime]:
    return [day_from + timedelta(days=i) for i in range((day_to - day_from).days + 1)]

def prepare_directory(folder) -> None:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase, k=length))