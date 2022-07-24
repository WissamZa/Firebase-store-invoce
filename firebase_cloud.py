from daily import dailys
import sys
from datetime import datetime,  timedelta
from typing import List

import firebase_admin
from firebase_admin import credentials, firestore
 


def setDailys_invoc(db: firestore, date: datetime, item: List) -> None:

    if str(item[0])[0] == "-":
        dtime = timedelta(days=int(str(item[0])[1:]))
        date = date - dtime
    else:
        date = date + timedelta(days=int(item[0]))

    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")

    docs = db.collection("myStore").document(
        year).collection(month).document(day)
    d = dailys(date.strftime("%d/%m/%Y"),
               float(item[1]), float(item[2]), float(item[3]))

    docs.set({
        u"اليوم": d.date,
        u"الكاش": d.inCash,
        u"الشبكة": d.inCrdit,
        u"اجمالي الدخل": d.inTotal,
        u"المصروفات": d.outgoing,
        u"الصافي": d.totalNet
    })
    print(f'{d.date} Successfully created')


def getDailys_invoce(db, year):
    dailyList: List[dailys] = []
    collections = db.collection('myStore').document(str(year)).collections()
    for collection in collections:
        
        for doc in collection.stream():
            tempDict = doc.to_dict()
            inCash = tempDict['الكاش']
            inCrdit = tempDict['الشبكة']
            date = datetime(int(year), int(collection.id), int(doc.id))
            dailyList.append(dailys(date.strftime('%d/%m/%Y'), inCash, inCrdit))
    return dailyList


# Use a service account
def connectToFirebase(path):
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = connectToFirebase("serviceAccountKey.json")
date = datetime.today()

#setDailys_invoc(db, date, sys.argv[1:])

print(getDailys_invoce(db, date.today().year))
