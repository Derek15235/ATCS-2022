"""
Our main application logic
"""

from twitter import * 
from database import init_db, db_session
from models import *




        
            

tw = Twitter()
tw.run()
