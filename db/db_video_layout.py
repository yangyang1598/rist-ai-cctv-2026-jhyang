from db.db_manager import DBManager

def get_video_layouts():
    sql = "SELECT * FROM video_layouts"
    db = DBManager()
    return db.query(sql,fetch_type='all')

def add_video_layout(name, video_data_json):
    sql = "INSERT INTO video_layouts (name, video_data) VALUES (%s, %s)"
    db = DBManager()
    return db.query(sql, (name, video_data_json),fetch_type='none')

def update_video_layout_by_name(name, video_data_json):
    sql = "UPDATE video_layouts SET video_data = %s WHERE name = %s"
    db = DBManager()
    return db.query(sql, (video_data_json, name),fetch_type='none', return_rowcount=True)

def delete_video_layout_by_name(name):
    sql = "DELETE FROM video_layouts WHERE name = %s"
    db = DBManager()
    params = (name,)
    return db.query(sql, params,fetch_type='none', return_rowcount=True)
