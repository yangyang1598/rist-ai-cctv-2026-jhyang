from db.db_manager import DBManager

def get_cctv_list(fields: str='*'):
    sql = f"SELECT {fields} FROM camera_list ORDER BY camera_name, camera_location"
    db = DBManager()
    return db.query(sql, fetch_type='all')


def delete_cctv_by_name(name):
    sql = "DELETE FROM camera_list WHERE camera_name = %s"
    params = (name,)
    db = DBManager()
    return db.query(sql, params, fetch_type='none',return_rowcount=True)

class DbCctvList:
    TABLE_NAME = 'camera_list'

    def __init__(self) -> None:
        self.id = 0
        self.camera_location = ''
        self.camera_name = ''
        self.camera_ip = ''
        self.port = None
        self.ptz_port = None
        self.protocol = ''
        self.rtsp_id = ''
        self.rtsp_pw = ''
        self.stream_path = ''
        self.skip_frame = None
        self.unsafe_event = None

    def insert(self):
        db = DBManager()
        try:
            sql = f"INSERT INTO {self.TABLE_NAME} (id, camera_location, camera_name, camera_ip, port, ptz_port,protocol, rtsp_id, rtsp_pw, stream_path, skip_frame) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (
                self.id if self.id != 0 else None,  # id가 0이면 자동 증가를 위해 None
                self.camera_location,
                self.camera_name,
                self.camera_ip,
                self.port,
                self.ptz_port,
                self.protocol,
                self.rtsp_id,
                self.rtsp_pw,
                self.stream_path,
                self.skip_frame
            )
            return db.query(sql, params, fetch_type='none')
        except Exception as e:
            print(f"insert error: {e}")
            return None

    def update(self, id=None, camera_name=None,camera_location=None, limit=None):
        db = DBManager()
        try:
            conditions = []
            params = []
            set_clauses = []

            # SET 절 구성 - 인스턴스 변수 사용
            if self.camera_location:
                set_clauses.append("camera_location = %s")
                params.append(self.camera_location)
            if self.camera_name:
                set_clauses.append("camera_name = %s")
                params.append(self.camera_name)
            if self.camera_ip:
                set_clauses.append("camera_ip = %s")
                params.append(self.camera_ip)
            if self.port is not None:
                set_clauses.append("port = %s")
                params.append(self.port)
            if self.ptz_port is not None:
                set_clauses.append("ptz_port = %s")
                params.append(self.ptz_port)
            if self.protocol:
                set_clauses.append("protocol = %s")
                params.append(self.protocol)
            if self.rtsp_id:
                set_clauses.append("rtsp_id = %s")
                params.append(self.rtsp_id)
            if self.rtsp_pw:
                set_clauses.append("rtsp_pw = %s")
                params.append(self.rtsp_pw)
            if self.stream_path:
                set_clauses.append("stream_path = %s")
                params.append(self.stream_path)
            if self.skip_frame is not None:
                set_clauses.append("skip_frame = %s")
                params.append(self.skip_frame)
            if self.unsafe_event is not None:
                set_clauses.append("unsafe_event = %s")
                params.append(self.unsafe_event)
            
            if not set_clauses:
                raise ValueError("No fields provided for update")

            sql = f"UPDATE {self.TABLE_NAME} SET " + ", ".join(set_clauses)

            # WHERE 절 구성
            if id is not None:
                conditions.append("id = %s")
                params.append(id)
            elif camera_name is not None:
                conditions.append("camera_name = %s")
                params.append(camera_name)
            elif camera_location is not None:
                conditions.append("camera_location = %s")
                params.append(camera_location)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            if limit:
                sql += " LIMIT %s"
                params.append(limit)
                
            return db.query(sql, params, fetch_type='none',return_rowcount=True)
        except Exception as e:
            print(f"update error: {e}")
            return None

    def select(self, id=None, camera_location=None, camera_name=None, camera_ip=None, 
               port=None, protocol=None, unsafe_event=None, limit=None):
        db = DBManager()
        conditions = []
        params = []
        
        try:
            sql = f"""SELECT id, camera_location, camera_name, camera_ip, port, ptz_port, 
                     protocol, rtsp_id, rtsp_pw, stream_path, skip_frame, unsafe_event 
                     FROM {self.TABLE_NAME}"""

            # WHERE 절 구성
            if id is not None:
                conditions.append("id = %s")
                params.append(id)
            if camera_location is not None:
                conditions.append("camera_location = %s")
                params.append(camera_location)
            if camera_name is not None:
                conditions.append("camera_name = %s")
                params.append(camera_name)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " ORDER BY camera_location, camera_name"

            if limit is not None:
                sql += " LIMIT %s"
                params.append(limit)

            rows = db.query(sql, params, fetch_type='all')
            cctv_list = []

            if rows:
                for r in rows:
                    cctv = DbCctvList()
                    cctv.id = r.get('id')
                    cctv.camera_location = r.get('camera_location')
                    cctv.camera_name = r.get('camera_name')
                    cctv.camera_ip = r.get('camera_ip')
                    cctv.port = r.get('port')
                    cctv.ptz_port = r.get('ptz_port')
                    cctv.protocol = r.get('protocol')
                    cctv.rtsp_id = r.get('rtsp_id')
                    cctv.rtsp_pw = r.get('rtsp_pw')
                    cctv.stream_path = r.get('stream_path')
                    cctv.skip_frame = r.get('skip_frame')
                    cctv.unsafe_event = r.get('unsafe_event')
                    cctv_list.append(cctv)

            return cctv_list
        except Exception as e:
            print(f"select error: {e}")
            return None

    def delete(self, camera_name):
        db = DBManager()
        try:
            sql = f"DELETE FROM {self.TABLE_NAME} WHERE camera_name = %s"
            return db.query(sql, (camera_name,), fetch_type='none',return_rowcount=True)
        except Exception as e:
            print(f"delete error: {e}")
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
        