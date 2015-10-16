
import sys
import os
import string as s
import json 
from pprint import *
from collections import defaultdict
from operator import getitem
from sqlalchemy import *
from datetime import *
import psycopg2
import dictgenerateupdate101415 as gu
import vtminingalgos as ma
import json

class autoviv(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

# visittree=autoviv()

def tree(): return defaultdict(tree)

def dicts(t): return {k: dicts(t[k]) for k in t}

visittree=autoviv()
analysisdict=autoviv()

instructions=json.loads(open('vtmininginstructions.json').read())  
            
# print 'instructions', json.dumps(instructions)
            
db = create_engine("postgresql+psycopg2://LI:PW@IP:PORT/DW")
db_con=db.connect()

algo=instructions["algorithm"]["type"]
algoinstr=instructions["algorithm"]
pervalue=instructions["pervalue"]
selstr=instructions["allresults"]
ctstr=instructions["getcount"]
pagecol=instructions["pagecolumn"]
headerarray=instructions['headerarray']
uniquegrain=instructions['uniquegrain']
critpages=instructions['critpages']	
# critindlist=critpages['critindices'][pervalue]
# critpagelist=critpages['critpages'][pervalue]
tabletodistinct=instructions['tabletodistinct']
arraytodistinct=instructions['arraytodistinct']
# entrypoint=instructions['entrypoint']

pagecolindex=headerarray.index(pagecol)


# print 'addlpages',addlpages
# print 'selstr', selstr

result=db_con.execute(selstr)

resultlen=db_con.execute(ctstr)

resultlen=[row for row in resultlen][0][0]

# print 'resultlen',resultlen

def returnumarray(ary,headarry):
	temparry=[]
	for el in ary:
		if el in temparry==False:
			temparry.append(headarry.index(el))

	return temparry

# https://gist.github.com/hrldcpr/2012250

		
def createjson(t,instructions):
# 	print 'increatejson'
	prevbreakoutvartest=''
	
	pagelist=','
	
	prevuniquegraintest=''	
			
	rowct=0
	pagelist=''
		
	for row in result:
		uniquegraintest=''
		breakoutvartest=''
		
#  condition for current visitorid and visitnumber
		for col in uniquegrain: #store vals			
			uniquegraintest+=str(row[headerarray.index(col)])+'|'
		
		if prevuniquegraintest==uniquegraintest:
# 			print 'case1'
			pagelist+=','+str(row[pagecolindex])
# 			ALSO PUT TIMES
		elif rowct!=0: 
			print 'case2'
			pagelist+=','

			evaldict=ma.evalstring(pagelist,instructions,'d',pervalue,row,None)
## 			print 'evaldict',evaldict
			
# 			NOW BUILD ANALYSIS RESULTS DICT
# 			NOTE THAT IT DOESN'T MATTER IF YOU BUILD THIS BEFORE THE FULL JSON
			
# 			print 'algo is', algo, 'len is', len(evaldict['sandwichpath'])
			
			if algo=='sandwich' and len(evaldict['sandwichpath'])>0:
				print 'building sand dict'
				ma.buildalgoresults(analysisdict,evaldict,instructions,'sandpre',pervalue,arraytodistinct=None,distinctgrain=None)
					
			gu.add(t,evaldict['strfordict'],'u',1,1,arraytodistinct,distinctgrain,None)
			pagelist=','+str(row[pagecolindex])
		else:
# 			print 'case3'
			pagelist=','+str(row[pagecolindex])
		
		if rowct==resultlen-1:
			print 'case4'
			pagelist+=','
			evaldict=ma.evalstring(pagelist,instructions,'d',pervalue,row,None)
## 			print 'evaldict',evaldict

			gu.add(t,evaldict['strfordict'],'u',1,1,arraytodistinct,distinctgrain,None)
			
		distinctgrain=[]
		for col in arraytodistinct:
			tempstr1=row[headerarray.index(col)]
			if not isinstance(tempstr1,basestring):
				tempstr1=str(tempstr1)
			distinctgrain.append(tempstr1)
		
		uniquegrain2=[]
		for col in uniquegrain:
			tempstr1=row[headerarray.index(col)]
			if not isinstance(tempstr1,basestring):
				tempstr1=str(tempstr1)
			uniquegrain2.append(tempstr1)	
			
# 		print 'createjsonrowct',rowct,uniquegrain2
		
		pervalue=row[headerarray.index(instructions["pervalue"])]
		
# 		print 'pervalue in createjson', pervalue
			
		prevuniquegraintest=uniquegraintest
		
		rowct+=1			

createjson(visittree,instructions)
# print 'visittree',json.dumps(visittree)

with open('vtminingtestoutput.json', 'wb') as fp:
    json.dump(visittree, fp)
    
fp.close()

with open('vtanalyticsoutput.json', 'wb') as fp:
    json.dump(analysisdict, fp)
    
fp.close()









