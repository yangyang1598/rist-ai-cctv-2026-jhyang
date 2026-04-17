from db.db_manager import DBManager

def build_select_query(fields='*', filters=None, group_by=None, order_by=None, limit=None, offset=None):
    """
    sql 예시:
        SELECT * FROM event_log_data
        WHERE
        date BETWEEN '2025-05-11 00:00:00' AND '2025-06-11 08:14:57'
        AND (cctv_location = '1공장' AND cctv_id IN ('CCTV 1', 'CCTV 3', 'CCTV 5'))
        OR (cctv_location = '2공장' AND cctv_id IN ('CCTV 8', 'CCTV 9', 'CCTV 10'))
        OR (cctv_location = '3공장')
        ORDER BY date DESC
        LIMIT 100;
    """

    filters = filters or []
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    order_clause = f"ORDER BY {order_by}" if order_by else ""
    limit_clause = f"LIMIT {limit}" if limit else ""
    offset_clause = f"OFFSET {offset}" if offset else ""
    group_by_clause = f"GROUP BY {' , '.join(group_by)}" if group_by else ""

    return f"SELECT {fields} FROM event_log_data {where_clause} {group_by_clause} {order_clause} {limit_clause} {offset_clause};"

def build_date_filter(start_dt, end_dt):
    if start_dt and end_dt:
        return f"date BETWEEN '{start_dt}' AND '{end_dt}'"
    return None

def build_cctv_filter(selected_cctvs):
    group_conditions = []

    if selected_cctvs:
        for location, info in selected_cctvs.items():
            if info.get("selected"):     # 부모(위치)가 선택된 경우 자식(해당 위치의 CCTV)이 전체 선택된 경우와 동일하므로, 위치만 조건 설정
                group_conditions.append(f"(cctv_location = '{location}')")
            elif info.get("children"):
                children = ", ".join(f"'{c}'" for c in info["children"])
                group_conditions.append(f"(cctv_location = '{location}' AND cctv_id IN ({children}))")

        return f"({' OR '.join(group_conditions)})" if group_conditions else None
    return None

def build_event_filter(selected_events):
    event_filter = []

    if selected_events:
        return f"(content IN ({", ".join(f"'{event}'" for event in selected_events)}))"
    return None

def get_ai_event_logs(fields: str = '*', start_dt: str = None, end_dt: str =None, selected_cctvs: dict = None, selected_events: list = None, order_by: str = "date DESC", group_by: list = None, limit: int = None, offset: int = None):
    """
    field 예시:
        date, cctv_location, cctv_id

    selected_cctvs 예시:
        {
        '1공장': {'selected': False, 'children': ['CCTV 1', 'CCTV 3']},
        '2공장': {'selected': True, 'children': ['all']},
        ...
        }

    selected_events 예시:
        ['사람 검출', '지게차 검출']
    """
    filters = []

    if date_filter := build_date_filter(start_dt, end_dt):
        filters.append(date_filter)

    if cctv_filter := build_cctv_filter(selected_cctvs):
        filters.append(cctv_filter)

    if event_filter := build_event_filter(selected_events):
        filters.append(event_filter)

    sql = build_select_query(
        fields=fields,
        filters=filters,
        group_by=group_by,
        order_by=order_by,
        limit=limit,
        offset=offset
    )

    db = DBManager()
    return db.fetch_all(sql)

def insert_ai_event_log(date, cctv_location, cctv_name, event, severity, image_path):
    sql = "INSERT INTO event_log_data (date, cctv_location, cctv_id, content, severity, image) VALUES (%s, %s, %s, %s,%s, %s)"
    db = DBManager()
    return db.execute(sql, (date, cctv_location, cctv_name, event, severity,image_path))

