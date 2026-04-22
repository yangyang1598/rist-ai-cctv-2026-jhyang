import sys
import os
sys.path.append(os.path.abspath(os.curdir))
import json
from uuid import uuid4

from db.db_manager import DBManager

class DbModelList:
    TABLE_NAME = 'model_list'

    def __init__(self) -> None:
        self.id = 0
        self.model_description = ''
        self.model_name = ''
        self.model_registered_at = None
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        self.map50 = 0
        self.map50_95 = 0
        self.f1_score = 0
        self.speed = 0
        self.status = 0
        
    def insert(self, model_description, model_name, model_registered_at):
        db = DBManager()
        
        try:
            sql = f"INSERT INTO {self.TABLE_NAME} (model_description, model_name, model_registered_at) VALUES (%s, %s, %s)"
                
            params = (
                model_description,
                model_name,
                model_registered_at
            )
            return db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"insert error: {e}")
            return None
    
    def update(self, model_description=None, model_name=None, precision=None, recall=None, map50=None, map50_95=None, f1_score=None, speed=None, status=None):
        db = DBManager()
        try:
            set_clauses = []
            params = []
            conditions = []
           
            if status is not None:
                set_clauses.append("status = %s")
                params.append(status)
            if f1_score is not None:
                set_clauses.append("f1_score = %s")
                params.append(f1_score)
            if map50 is not None:
                set_clauses.append("map50 = %s")
                params.append(map50)
            if map50_95 is not None:
                set_clauses.append("map50_95 = %s")
                params.append(map50_95)
            if precision is not None:
                set_clauses.append("`precision` = %s")
                params.append(precision)
            if recall is not None:
                set_clauses.append("recall = %s")
                params.append(recall)
            if speed is not None:
                set_clauses.append("speed = %s")
                params.append(speed)
            if not set_clauses:
                raise ValueError("No fields provided for update")

            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)}"
            
            if model_description:
                conditions.append("model_description = %s")
                params.append(model_description)
            if model_name:
                conditions.append("model_name = %s")
                params.append(model_name)
                
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            else:
                raise ValueError("No conditions provided for update")

            return db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"update error: {e}")
            return None

    def select(self, id=None, model_description=None, model_name=None, model_registered_at=None, accuracy=None, precision=None, recall=None, map50=None, map50_95=None, f1_score=None, speed=None, status=None, limit=None):
        db = DBManager()
        try:
            conditions = []
            params = []

            if id:
                conditions.append("id = %s")
                params.append(id)
            elif model_name:
                conditions.append("model_name = %s")
                params.append(model_name)
            elif model_description:
                conditions.append("model_description = %s")
                params.append(model_description)
            sql = f"SELECT id, model_description, model_name, model_registered_at, accuracy, `precision`, recall, map50, map50_95, f1_score, speed, status FROM {self.TABLE_NAME}"
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
                    
            if limit:
                sql += " LIMIT %s"
                params.append(limit)

            rows = db.query(sql, params, fetch_type='all')
            m_list = []

            for r in rows:
                ml = DbModelList()
                ml.id = r.get('id')
                ml.model_description = r.get('model_description')
                ml.model_name = r.get('model_name')
                ml.model_registered_at = r.get('model_registered_at')
                ml.accuracy = r.get('accuracy')
                ml.precision = r.get('precision')
                ml.recall = r.get('recall')
                ml.map50 = r.get('map50')
                ml.map50_95 = r.get('map50_95')
                ml.f1_score = r.get('f1_score')
                ml.speed = r.get('speed')
                ml.status = r.get('status')
                m_list.append(ml)

            return m_list
        except Exception as e:
            print(f"select error: {e}")
            return None
    
    def delete(self, model_description=None, model_name=None):
        db = DBManager()
        try:
            conditions = []
            params = []
            
            if model_description:
                conditions.append("model_description = %s")
                params.append(model_description)
            if model_name:
                conditions.append("model_name = %s")
                params.append(model_name)
                
            if not conditions:
                raise ValueError("No conditions provided for delete")
                
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE " + " AND ".join(conditions)
            return db.query(sql, params,fetch_type='none', return_rowcount=True)
        except Exception as e:
            print(f"delete error: {e}")
            return None