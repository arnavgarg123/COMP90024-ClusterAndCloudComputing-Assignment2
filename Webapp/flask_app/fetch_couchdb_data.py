import couchdb
import xlsxwriter
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