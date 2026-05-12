def home_handler(query,params=None):
    clean_params = {k:v[0] for k,v in query.items()}
    return 200, {"status":"success", "data":clean_params}