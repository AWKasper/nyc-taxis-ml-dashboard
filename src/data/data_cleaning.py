import pandas as pd
import datetime as dt

data= pd.read_csv("yellow_tripdata_2015-01.csv", sep= ",")
df= pd.DataFrame(data)

#drop alle rows met nan (zijn er maar drie)
rows_null= df[df.isna().any(axis=1)]
df= df.dropna()

#Check of er dubbele data zijn
df.drop_duplicates(keep= 'first', inplace=True)

# 1 Column: VendorID-----------------------------------------------------------------------------------------------------------------
values=[1,2]
df = df[df.VendorID.isin(values)== True] 

# 2 Column: tpep_pickup_datetime-----------------------------------------------------------------------------------------------
#tpep_pickup_datetime is op het moment een object ik ga dit eerst veranderen naar datetime

df['tpep_pickup_datetime']= pd.to_datetime(df['tpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')

#tpep_pickup_datetime grenzen stellen.
df= df.loc[(df['tpep_pickup_datetime'] > '2015-01-01') & (df['tpep_pickup_datetime']< '2020-12-31')]

# 3 Column: tpep_dropoff_datetime-------------------------------------------------------------------------------------------------
#tpep_dropoff_datetime is op het moment een object ik ga dit eerst veranderen naar datetime
df['tpep_dropoff_datetime']= pd.to_datetime(df['tpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')

#tpep_dropoff_datetime grenzen stellen.

df= df.loc[(df['tpep_dropoff_datetime'] > '2015-01-01') & (df['tpep_dropoff_datetime']< '2020-12-31')]

# 4 Column(toevoegen): time_difference-------------------------------------------------------------------------------------------------
df.insert(3,'time_difference', (df.tpep_dropoff_datetime - df.tpep_pickup_datetime), True)
df['time_difference'] = df['time_difference'].astype(str).map(lambda x: x[7:])

# 5 Column : passenger_count----------------------------------------------------------------------------------------------------------
df= df[df["passenger_count"] > 0] #ritjes van nul kan niet 
df= df[df['passenger_count'] <= 9 ] #ritjes boven de 9 lijkt me ongmogelijk in een taxi

# 6 Column: Trip_distance ----------------------------------------------------------------------------------------------------------
df= df[df["trip_distance"].between(0.01,186)] #186 miles komt overeen met 300km 

# 7 Column: Pickup_longitude ----------------------------------------------------------------------------------------------------------
df= df[df["pickup_longitude"].between(-78,-68)] #coördinaten van new york en ook daarbuiten lengtegraad

# 8 Column: pickup_latitude ----------------------------------------------------------------------------------------------------------
df= df[df["pickup_latitude"].between(37,47)] #coördinaten van new york en ook daarbuiten breedtegraad

# 9 Column: RateCodeID ----------------------------------------------------------------------------------------------------------
ratecodevalues= [1,2,3,4,5,6]
df = df[df.RateCodeID.isin(ratecodevalues)== True] 

# 10 Column: Store_and_fwd_flag ----------------------------------------------------------------------------------------------------------
storeflagvalues= ["Y","N"]
df = df[df.store_and_fwd_flag.isin(storeflagvalues)== True]

# # 11 Column: dropoff_longitude ----------------------------------------------------------------------------------------------------------
df= df[df["dropoff_longitude"].between(-78,-68)] #coördinaten van new york en ook daarbuiten breedtegraad

# 12 Column: dropoff_latitude ----------------------------------------------------------------------------------------------------------
df= df[df["dropoff_latitude"].between(37,47)] #coördinaten van new york en ook daarbuiten lengtegraad

# 13 Column: Payment_type ----------------------------------------------------------------------------------------------------------
payment_typevalues= [1,2,3,4,5,6]
df = df[df.payment_type.isin(payment_typevalues)== True] 

# 14 Column: Fare_amount ----------------------------------------------------------------------------------------------------------
# Ik heb geen idee of dit negatief mag zijn. 
# print(df.nsmallest(5,'fare_amount'))

#15 Column: Extra ----------------------------------------------------------------------------------------------------------
# ik vermoed dat dit of 0.50 en 1 is.
df= df[df["extra"] >= 0]

#16 Column: MTA_tax ----------------------------------------------------------------------------------------------------------
df= df[df["mta_tax"] >= 0.5 ]

#17 Column: tip_amount ----------------------------------------------------------------------------------------------------------
df= df[df["tip_amount"] >= 0]

#18 Column: tolls_amount ----------------------------------------------------------------------------------------------------------
df= df[df["tolls_amount"] >=0]

#16 Column: Improvement_surcharge ----------------------------------------------------------------------------------------------------------
df= df[df["improvement_surcharge"] >=0]

#18 Column total_amount ----------------------------------------------------------------------------------------------------------
df= df[df["total_amount"] > 0.1]

print(df)