from db.db_manager import DBManager

def get_video_layouts():
    sql = "SELECT * FROM video_layouts"
    db = DBManager()
    return db.fetch_all(sql)

def add_video_layout(name, video_data_json):
    sql = "INSERT INTO video_layouts (name, video_data) VALUES (%s, %s)"
    db = DBManager()
    return db.execute(sql, (name, video_data_json))

def update_video_layout_by_name(name, video_data_json):
    sql = "UPDATE video_layouts SET video_data = %s WHERE name = %s"
    db = DBManager()
    return db.execute(sql, (video_data_json, name), return_rowcount=True)

def delete_video_layout_by_name(name):
    sql = "DELETE FROM video_layouts WHERE name = %s"
    db = DBManager()
    return db.execute(sql, name, return_rowcount=True)