import sys
import os
sys.path.append(os.path.abspath(os.curdir))
import random
import json
from uuid import uuid4

from db.db_manager import DBManager

class DbAccounts:
    TABLE_NAME = 'accounts'

    def __init__(self) -> None:
        self.id = 0
        self.user_id=""
        self.user_password=""
        

    def select(self, id=None, user_id=None, user_password=None, limit=None):
        db = DBManager()
        conditions = []
        params = []
        try:
            if id:
                conditions.append("id = %s")
                params.append(id)
            if user_id:
                conditions.append("user_id = %s")
                params.append(user_id)
            if user_password:
                conditions.append("user_password = %s")
                params.append(user_password)

            sql = f"SELECT id, user_id, user_password FROM {self.TABLE_NAME}"

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
                    
            if limit:
                sql += " LIMIT %s"
                params.append(limit)

            rows = db.query(sql, params, fetch_type='all')
            acc_list = []

            for r in rows:
                acc = DbAccounts()
                acc.id = r.get('id')
                acc.user_id = r.get('user_id')
                acc.user_password = r.get('user_password')
            
                acc_list.append(acc)

            return acc_list
        except Exception as e:
            print(f"select error: {e}")
            return None
    
    


