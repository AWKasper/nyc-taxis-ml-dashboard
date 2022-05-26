from sqlalchemy import create_engine, insert, MetaData, Table
import pandas as pd

DATE_COL = "tpep_pickup_datetime"
LONGI = "pickup_longitude"
LATI = "pickup_latitude"

def __get_data(amount = 50000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"""SELECT {DATE_COL}, {LONGI}, {LATI} FROM 
    (SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount}) 
    AS limited_data"""
    return pd.read_sql(query, engine)
    
def __format_date_strings(df : pd.DataFrame):
    df[DATE_COL] = df.apply(lambda row:row['tpep_pickup_datetime'][:-6], axis=1)
    return df

def __order_coords_by_date(df : pd.DataFrame):
    dic = dict()
    for i, row in df.iterrows():
        dic.setdefault(row[DATE_COL], list())
        dic[row[DATE_COL]].append([row[LONGI],row[LATI]])
    return dic

def __write_to_file(filename : str, data : dict):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def __write_to_db(data : dict):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    _list_of_data = []
    for key in data:
        point_string = ""
        for point in data[key]:
            point_string += f"{point[0]} {point[1]} "
        _list_of_data.append({"Date" : key, "Points" : point_string})

    meta_data = MetaData(bind=engine)
    meta_data.reflect()

    _table = meta_data.tables['Points_grouped_by_date']
    stmt = _table.insert().values(_list_of_data)
    engine.execute(stmt)
    

if __name__ == '__main__':
    df = __get_data(50)
    df = __format_date_strings(df)
    dic = __order_coords_by_date(df)
    __write_to_db(dic)
    #__write_to_file("rides.json", dic)
    
