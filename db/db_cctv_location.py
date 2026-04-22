# 안전관리 포인트에 대한 정보를 관리하는 DB 클래스
# 
# 안전관리 포인트 명칭
# CCTV 연결 경로(URL)
# AI_MODEL 명칭
# 알람타워 제어(ON) 경로(URL)
# 알람타워 제어(OFF) 경로(URL)

import sys, os
sys.path.append(os.path.abspath(os.curdir))
import random
from db.db_manager import DBManager

class DbCctvLocation():
    TABLE_NAME = 'camera_location'

    def __init__(self) -> None:
        self.id = 0
        self.camera_location = None


    def update(self,camera_location=None):
        """카메라 정보를 업데이트하고, 변경된 카메라가 스트림 중이면 재시작"""
    
        # DB 업데이트 실행
        db = DBManager()
        try:
            set_clauses = []
            params = []
            conditions = []
            if camera_location is not None:
                set_clauses.append("camera_location = %s")
                conditions.append("camera_location = %s")
                params.append(self.camera_location)
                params.append(camera_location)
            if not set_clauses:
                raise ValueError("No fields provided for update")

            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)}"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"update error: {e}")
            return None
      

        
    def delete(self, camera_location):
        db = DBManager()
        sql= f"DELETE FROM {self.TABLE_NAME} WHERE camera_location=%s;"
        params = (camera_location,)
        return db.query(sql, params,fetch_type='none')

    def insert(self):
        # 기본적으로 skip_frame 값을 None으로 설정
        db = DBManager()
        try: 
            sql = f"INSERT INTO {self.TABLE_NAME}(camera_location) VALUES (%s)"
            params = (self.camera_location,)
            return db.query(sql,params,fetch_type='none')
        except Exception as e:
            print(f"insert error: {e}")
            return None

    def select(self, id=None, camera_location=None):
        db = DBManager()
        conditions = []
        params = []
        try:
            if id:
                conditions.append("id = %s")
                params.append(id)
            elif camera_location:
                conditions.append("camera_location = %s")
                params.append(camera_location)

            sql = f"SELECT id, camera_location FROM {self.TABLE_NAME}"
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

           
            rows = db.query(sql, params, fetch_type='all')

            cl_list = []
            for r in rows:
                cl = DbCctvLocation()
                cl.id = r.get('id')
                cl.camera_location = r.get('camera_location')
                cl_list.append(cl)
            
            return cl_list
        except Exception as e:
            print(f"select error: {e}")
            return None



if __name__ == "__main__":
    cl = DbCctvLocation()
    
    cl.camera_location = 'n 공장'
    print(cl.sql_insert())
    cl.insert()