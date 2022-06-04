from sqlalchemy import MetaData

def get_table(engine, table_name : str):
    meta_data = MetaData(bind=engine)
    meta_data.reflect()
    table = meta_data.tables[table_name]
    return table