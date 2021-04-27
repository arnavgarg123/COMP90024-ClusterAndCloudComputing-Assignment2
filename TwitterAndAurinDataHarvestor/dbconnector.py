import couchdb
import json
class Couch:
    def __init__(self,ip,dbnamelist):
        couchserver=couchdb.Server(url=ip)
        couchserver.resource.credentials=('admin','admin')
        #self.createstaticdb()
        self.db=[]
        dbsl=['tweet_api','region']
        for dbname in dbsl:
            self.db=self.db+[self.createdb(couchserver,dbname)]
        for dbname in dbnamelist:
            self.db=self.db+[self.createdb(couchserver,dbname)]
        self.create_static()
        
    def createdb(self,couchserver,dbname):
        if dbname in couchserver:
            return couchserver[dbname]
        else:
            return couchserver.create(dbname)

    def create_static(self):
        a=open('tweetapi.json')
        for i in a.readlines():
            b=json.loads(i)
            try:
                self.pushdata(b,'tweet_api')
            except:
                pass
        a=open('region.json')
        for i in a.readlines():
            b=json.loads(i)
            try:
                self.pushdata(b,'region')
            except:
                pass

    def pushdata(self,data,dbname):
        flag=0
        for i in self.db:
            if dbname==i._name:
                flag=0
                i.save(data)
                break
            else:
                flag=1
        if flag==1:
            print(dbname+" does not exist")
    
    def getdata(self,dbname):
        for i in self.db:
            if dbname==i._name:
                for j in i:
                    return i.get(j)
                    break
