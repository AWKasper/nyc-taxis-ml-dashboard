from sqlalchemy import create_engine, insert, MetaData, Table, select
import pandas as pd

DATE_COL = "tpep_pickup_datetime"
LONGI = "pickup_longitude"
LATI = "pickup_latitude"

# amount = 0 will be interpreted as all
def __get_data(offset = 0, amount = 50000, chunksize = 10000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"SELECT {DATE_COL}, {LONGI}, {LATI} FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount} OFFSET {offset}"
    if amount == 0: query = f"SELECT {DATE_COL}, {LONGI}, {LATI} FROM uncleaned_NYC_yellowcabs_2015"
    chunks = pd.read_sql(query, engine, chunksize = chunksize )
    return pd.concat(chunks, ignore_index=True)
    
def __format_date_strings(df : pd.DataFrame):
    df[DATE_COL] = df.apply(lambda row:row['tpep_pickup_datetime'][:-6], axis=1)
    return df

def __order_coords_by_date(df : pd.DataFrame):
    dic = dict()
    for i, row in df.iterrows():
        dic.setdefault(row[DATE_COL], list())
        dic[row[DATE_COL]].append(row[LONGI])
        dic[row[DATE_COL]].append(row[LATI])
    return dic

def __write_to_file(filename : str, data : dict):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def __write_to_db(data : dict):
    import json
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    
    _table = __get_table(engine,'Points_grouped_by_date')

    _to_send_to_db = list()
    for key in data:
        point_list = [point for point in data[key]]
        json_object = json.dumps({key : point_list})
        _to_send_to_db.append({"Date" : key, "Data" : json_object})  

    engine.execute(_table.insert(), _to_send_to_db)

def execute_processing():
    df = __get_data(0, 0, 25000)
    df = __format_date_strings(df)
    dic = __order_coords_by_date(df)
    __write_to_db(dic)

def __get_table(engine, table_name : str):
    meta_data = MetaData(bind=engine)
    meta_data.reflect()
    table = meta_data.tables[table_name]
    return table

def get_points_at_date(date : str) -> list[float]:
    import json
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    table = __get_table(engine, 'Points_grouped_by_date')
    stmt = select(table).where(table.c.Date == date)
    rows = [row for row in engine.execute(stmt)]
    js = json.loads(rows[0]['Data'])
    return js[date]

if __name__ == '__main__':
    print(get_points_at_date('2015-01-02 15'))
    #execute_processing()
    # df = __get_data(50,9)
    # df = __format_date_strings(df)
    # dic = __order_coords_by_date(df)
    # __write_to_db(dic)
    #__write_to_file("rides.json", dic)
    
