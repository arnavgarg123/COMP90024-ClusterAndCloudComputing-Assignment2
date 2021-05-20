import couchdb
import xlsxwriter
import pandas as pd
import geojson
import math

def save_data():
    a=open('../../TwitterAndAurinDataHarvestor/ip.txt')
    a=a.readline()
    a=a.strip()
    a='http://'+a+':5984/'
    couchserver=couchdb.Server(url=a)
    couchserver.resource.credentials=('admin','admin')
    c=[]
    b=couchserver['tweet']
    for i in b.view('all_doc/new-view'):
        c=c+[i.key]
    workbook = xlsxwriter.Workbook('./static/data_files/tweets_couchdb.xlsx')
    worksheet = workbook.add_worksheet()
    row=0
    col=0
    li=['ID','UID','Text','Created_At','City','Country','Co-ordinates','Sentiment']
    for j in li:
        worksheet.write(row, col, j)
        col=col+1
    row=row+1
    for i in c:
        col=0
        for j in i:
            worksheet.write(row, col, j)
            col=col+1
        row=row+1
    workbook.close()

def convert_geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["long"],
                                                    X["lat"])),
                            properties=dict(num_tweets=X["num_tweets"],
                                            radius=X["circle_radius"],num_users=X["num_users"])))
    df.apply(insert_features, axis=1)
    with open('./static/data_files/map1.geojson', 'w') as file:
        geojson.dump(geojson.FeatureCollection(features), file, sort_keys=True, ensure_ascii=False)

df = pd.read_csv('./static/data_files/points.csv',delimiter='|')
log_tweets=[]
long=[]
lat=[]
print(df)
for i in range(len(df)):
    r=df['coordinates'][i].split(',')
    l = [float(elem.strip().strip('[').strip(']')) for elem in r]
    long.append(sum(l[0 : : 2])/(len(l)//2))
    lat.append(sum(l[1 : : 2])/(len(l)//2))
    log_tweets.append(int(math.log(df['num_tweets'][i],2))*5+5)

df['circle_radius']=log_tweets
df['lat']=lat
df['long']=long
df=df[['long','lat','circle_radius','num_tweets','num_users']]

convert_geojson(df)
