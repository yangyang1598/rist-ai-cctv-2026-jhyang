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

class DbCctvSetting():
    TABLE_NAME = 'cctv_setting'

    def __init__(self) -> None:
        self.id = 0
        self.camera_location = None
        self.camera_name = 'cctv n'
        self.fps_limit=None
        self.unsafe_event=None

    def update(self,camera_location=None, camera_name=None,fps_limit=None, unsafe_event=None):
        """카메라 정보를 업데이트하고, 변경된 카메라가 스트림 중이면 재시작"""
    
        # DB 업데이트 실행
        db = DBManager()
        try:
            set_clauses = []
            params = []
            conditions = []
            if self.camera_location is not None:
                set_clauses.append("camera_location = %s")
                params.append(self.camera_location)
            if self.camera_name is not None:
                set_clauses.append("camera_name = %s")
                params.append(self.camera_name)
            if self.fps_limit is not None:
                set_clauses.append("fps_limit = %s")
                params.append(self.fps_limit)
            if self.unsafe_event is not None:
                set_clauses.append("unsafe_event = %s")
                params.append(self.unsafe_event)
            if not set_clauses:
                raise ValueError("No fields provided for update")
            
            if camera_name:
                conditions.append("camera_name = %s")
                params.append(camera_name)
            if camera_location:
                conditions.append("camera_location = %s")
                params.append(camera_location)
            
            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)} WHERE {' AND '.join(conditions)}"
            
            db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"update error: {e}")
            return None

    def delete(self, camera_name):
        db = DBManager()
        sql= f"DELETE FROM {self.TABLE_NAME} WHERE camera_name=%s;"
        params = (camera_name,)
        return db.query(sql, params,fetch_type='none')

    def insert(self):
        # 기본적으로 skip_frame 값을 None으로 설정
        db = DBManager()
        try: 
            
            sql = f"INSERT INTO {self.TABLE_NAME}(id, camera_location, camera_name, fps_limit, unsafe_event) VALUES (%s, %s, %s, %s, %s)"
            params = (
                self.id,
                self.camera_location,
                self.camera_name,
                self.fps_limit,
                self.unsafe_event
            )
            return db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"insert error: {e}")
            return None

    def select(self, id=None, camera_location=None, camera_name=None,fps_limit=None,unsafe_event=None, limit=None):
        db = DBManager()
        conditions = []
        params = []
        try:
            if id:
                conditions.append("id = %s")
                params.append(id)
            elif camera_name:
                conditions.append("camera_name = %s")
                params.append(camera_name)
            elif camera_location:
                conditions.append("camera_location = %s")
                params.append(camera_location)

            sql = f"SELECT id, camera_location, camera_name, fps_limit, unsafe_event FROM {self.TABLE_NAME}"
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            if limit is not None:
                sql += f" LIMIT {limit}"
                
            rows = db.query(sql, params, fetch_type='all')

            cs_list = []
            for r in rows:
                cs = DbCctvSetting()
                cs.id = r.get('id')
                cs.camera_location = r.get('camera_location')
                cs.camera_name = r.get('camera_name')
                cs.fps_limit = r.get('fps_limit')
                cs.unsafe_event = r.get('unsafe_event')
                cs_list.append(cs)
            
            return cs_list
        except Exception as e:
            print(f"select error: {e}")
            return None

    def change_unsafe_event_name(self, old_logic_name=None, logic_name=None):
        """unsafe_event 열에서 old_logic_name을 logic_name으로 변경"""
        # DB 업데이트 실행
        db = DBManager()
        try:
            set_clauses = []
            params = []
            conditions = []
            
            # old_logic_name과 logic_name이 제공되었는지 확인
            if old_logic_name is not None and logic_name is not None:
                set_clauses.append("unsafe_event = REPLACE(unsafe_event, %s, %s)")
                params.extend([old_logic_name, logic_name])
                # LIKE 패턴을 Python에서 구성
                like_pattern = f"%{old_logic_name}%"
                conditions.append("unsafe_event LIKE %s")
                params.append(like_pattern)
            
            # 업데이트할 필드가 없으면 에러 발생
            if not set_clauses:
                raise ValueError("old_logic_name and logic_name must be provided")
            
            # SQL 쿼리 구성
            sql = f"UPDATE {self.TABLE_NAME} SET {', '.join(set_clauses)}"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            # 디버깅을 위해 쿼리와 파라미터 출력
            print(f"Executing SQL: {sql}")
            print(f"Parameters: {params}")
            
            # 쿼리 실행
            db.query(sql, params,fetch_type='none')
        except Exception as e:
            print(f"update_logic_in_db error: {e}")
            return None

if __name__ == "__main__":
    cs = DbCctvSetting()
    
    cs.camera_location = 'n 공장'
    cs.camera_name='cctv n'
    cs.fps_limit=30
    cs.unsafe_event='none'
    print(cs.sql_insert())
    cs.insert()