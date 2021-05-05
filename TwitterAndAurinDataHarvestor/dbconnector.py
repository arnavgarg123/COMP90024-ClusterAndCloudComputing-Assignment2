# Assignment 2 - COMP90024 Course at The University of Melbourne
#
# Cluster and Cloud Computing - Team 48
#
# Authors:
#
#  * Arnav Garg (Student ID: 1248298)
#  * Piyush Bhandula (Student ID: 1163716)
#  * Jay Dave (Student ID: 1175625)
#  * Vishnu Priya G (Student ID: 1230719)
#  * Gurkirat Singh Chohan (Student ID: 1226595)
#
# Location: India, Melbourne, Singapore
#
import couchdb
import json
import time
import random

class Couch:
    def __init__(self,ip,dbnamelist):
        couchserver=couchdb.Server(url=ip)
        couchserver.resource.credentials=('admin','admin')
        self.db=[]
        dbsl=['tweet_api','region']
        f=open("ip.txt", "r")
        couchdb_master_ip=f.readline().rstrip()
        couchdb_master_login_url='http://admin:admin@'+couchdb_master_ip+':5984/'
        db_children=f.readlines()
        f.close()
        for dbname in dbsl:
            self.db=self.db+[self.createdb(couchserver,dbname)]
            for child in db_children:
                couchserver.replicate(couchdb_master_login_url+dbname,'http://admin:admin@'+child.rstrip()+':5984/'+dbname,create_target=True,continuous=True)
        for dbname in dbnamelist:
            self.db=self.db+[self.createdb(couchserver,dbname)]
            for child in db_children:
                couchserver.replicate(couchdb_master_login_url+dbname,'http://admin:admin@'+child.rstrip()+':5984/'+dbname,create_target=True,continuous=True)
        self.create_static()

    def createdb(self,couchserver,dbname):
        if dbname in couchserver:
            return couchserver[dbname]
        else:
            return couchserver.create(dbname)

    def create_static(self):
        a=open('tweetapi.json')
        for i in a.readlines():
            c=json.loads(i)
            try:
                self.pushdata(c,'tweet_api')
            except:
                pass
        a=open('region.json')
        for i in a.readlines():
            d=json.loads(i)
            try:
                self.pushdata(d,'region')
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
        while True:
            for i in self.db:
                if dbname==i._name:
                        r=str(random.randint(1,19))
                        harvest_obj=i.get(r)
                        if harvest_obj['flag']==0:
                            try:
                                harvest_obj['flag']=1
                                count=harvest_obj['count']
                                count+=1
                                harvest_obj['count']=count
                                i.save(harvest_obj)
                                print("id: ",r,i._name)
                                return harvest_obj
                            except:
                                print("id: ",r," wait: 15 sec sleep")
                                time.sleep(15)
                                pass

    def resetflag(self,column,value,dbname):
        for i in self.db:
            if dbname==i._name:
                for j in i:
                    target=i.get(j)
                    if target[column]==value:
                        target['flag']=0
                        i.save(target)

    def updatesinceid(self,column,value,since_id):
        for i in self.db:
            if 'region'==i._name:
                for j in i:
                    target=i.get(j)
                    if target[column]==value:
                        target['since_id']=since_id
                        i.save(target)
