import sys
import os
sys.path.append(os.path.abspath(os.curdir))
import random
import json
from uuid import uuid4

from db.db_manager import DBManager

class DbLogicList:
    TABLE_NAME = 'logic_list'

    def __init__(self) -> None:
        self.id = 0
        self.logic_name = ''
        self.skip_frame = 0
        self.input_img_size = ''
        self.risk_level = ''
        self.jiguk_direction = ''
        self.logicListData = []
        
    def insert(self):
        db = DBManager()
        try:    
            sql = f"INSERT INTO {self.TABLE_NAME} (id, logic_name, skip_frame, input_img_size, logicListData, risk_level, jiguk_direction) VALUES (%s, %s,%s, %s, %s, %s,%s)"
            params = (self.id, self.logic_name, self.skip_frame, str(self.input_img_size), json.dumps(self.logicListData, ensure_ascii=False), self.risk_level, self.jiguk_direction)
            return db.execute(sql, params)
        except Exception as e:
            print(f"insert error: {e}")
            return None
    
    def update(self, old_logic_name,logic_name=None, skip_frame=None, input_img_size=None, logicListData=None, risk_level=None, jiguk_direction=None):
        db = DBManager()
            
        try:
            set_clauses = []
            params = []
            conditions = []

            if skip_frame is not None:
                set_clauses.append("skip_frame = %s")
                params.append(skip_frame)
            
            if input_img_size:
                set_clauses.append("input_img_size = %s")
                params.append(str(input_img_size))
                
            if logicListData is not None:
                set_clauses.append("logicListData = %s")
                params.append(json.dumps(logicListData, ensure_ascii=False))
                
            if risk_level is not None:
                set_clauses.append("risk_level = %s")
                params.append(risk_level)
            
            if jiguk_direction is not None:
                set_clauses.append("jiguk_direction = %s")
                params.append(jiguk_direction)

            if logic_name is not None:
                set_clauses.append("logic_name = %s")
                params.append(logic_name)
            if not set_clauses:
                raise ValueError("No fields provided for update")
            
            if old_logic_name:
                conditions.append("logic_name = %s")
                params.append(old_logic_name)
            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)}"
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            return db.execute(sql, params)
        except Exception as e:
            print(f"update error: {e}")
            return None

    def select(self, id=None, logic_name=None, skip_frame=None, input_img_size=None, logicListData=None, risk_level=None, jiguk_direction=None, limit=None):
        db = DBManager()
        conditions = []
        params = []
        try:
            if id:
                conditions.append("id = %s")
                params.append(id)
            elif logic_name:
                conditions.append("logic_name = %s")
                params.append(logic_name)

            sql = f"SELECT id, logic_name, skip_frame, input_img_size, logicListData, risk_level, jiguk_direction FROM {self.TABLE_NAME}"

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
                    
            if limit:
                sql += " LIMIT %s"
                params.append(limit)

            rows = db.fetch_all(sql, params)
            lgl_list = []

            for r in rows:
                lgl = DbLogicList()
                lgl.id = r.get('id')
                lgl.logic_name = r.get('logic_name')
                lgl.skip_frame = r.get('skip_frame')
                try:
                    lgl.input_img_size = tuple(map(int, r.get('input_img_size').strip('()').split(',')))
                except:
                    lgl.input_img_size = ''
                try:
                    lgl.logicListData = json.loads(r.get('logicListData'))
                except:
                    lgl.logicListData = []
                lgl.risk_level = r.get('risk_level')
                lgl.jiguk_direction = r.get('jiguk_direction')
                lgl_list.append(lgl)

            return lgl_list
        except Exception as e:
            print(f"select error: {e}")
            return None
    
    def delete(self, logic_name=None, id=None):
        db = DBManager()
        try:
            conditions = []
            params = []
            
            if logic_name:
                conditions.append("logic_name = %s")
                params.append(logic_name)
            elif id:
                conditions.append("id = %s")
                params.append(id)
            else:
                raise ValueError("Either logic_name or id must be provided for deletion")
            
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE " + " AND ".join(conditions)
            return db.execute(sql, params)
        except Exception as e:
            print(f"delete error: {e}")
            return None


def get_event_logic_name():
    sql = "SELECT logic_name FROM logic_list"
    db = DBManager()
    return db.fetch_all(sql)

def get_event_logic_by_logic_name(logic_names):
    placeholders  = ', '.join(['%s'] * len(logic_names))  # → "%s, %s, %s"
    sql = f"SELECT * FROM logic_list WHERE logic_name IN ({placeholders })"
    db = DBManager()
    return db.fetch_all(sql, logic_names)