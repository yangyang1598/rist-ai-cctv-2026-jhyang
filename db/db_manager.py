import json
import requests

class DBManager:
    def __init__(self, host='localhost', port=30443):
        self.url = f"http://{host}:{port}/api/db/query"

    def query(self, query, params=None, fetch_type='all',return_rowcount=False):
        
        payload = {
            "query": query,
            "params": params,
            "fetch_type": fetch_type,
        }
        response = requests.post(self.url, json=payload)
        json_data = response.json()
        # print("json_data",json_data,"\n\n\n")

        if json_data.get("success")==True:
            # print("API 조회 결과:", json_data.get("data"),"\n\n\n")
            if fetch_type=='none' :
                if return_rowcount:
                    return json_data.get("meta").get("affected_rows")
                else:
                    return json_data.get("meta").get("last_insert_id")
            if fetch_type=='all':
                return json_data.get("data")
            if fetch_type=='one':
                return json_data.get("data")
        else:
            raise Exception(f'----------------------- QUERY ERROR: {json_data.get("error")}')

#fetch_type: all, one, none