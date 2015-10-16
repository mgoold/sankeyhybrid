import sys

class autoviv(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

# Path	OK
# Segment	OK
# EntryPoint OK
# EndPoint OK
# OPS	 OK
#PathLength	 OK
#End Point Visits	
# VisitsArray	ConversionArray
# // take entire path, and selected path
# 
# // use selected path as key
# // store length of path
# // store entry point
# // find pages of interest between entry page and entry point
# //	find visits array
# //	find conversion array



def getentrypoint(evalstr,entrypoint):
	entrypt=evalstr.index(entrypoint)
	
	return entrypt
	
def	evalstring(evalstr,instructions=None,evalflg='d',pervalue=None,row=None,substr=None):

# 		print 'pervalue in evalstring', pervalue, 'evalflg', evalflg
		
		if evalflg in ['d','s']:	
			while evalstr.find(',,')>0:
				evalstr=evalstr.replace(',,',',')
		
			evalstr2=evalstr[1:len(evalstr)-1].split(',')
			evalstr2=[int(i) for i in evalstr2]
			
			entrypoint=instructions["entrypoint"][pervalue]	
			
			firstentry=evalstr2.index(entrypoint)
			critindlist=instructions['critpages']['critindices'][pervalue]	
		
			addlpages=[]

			textsearchinjects=instructions['textsearchinjects']

			for k in textsearchinjects.keys():
				tempstr='select distinct '+pagecol+' from '+ tabletodistinct+' where upper(pagenameclean) like \'%%'+textsearchinjects[k]+'%%\''	
				
				inj=db_con.execute(tempstr)
	
				for row in inj:
					addlpages.append(row[0])
				
			combinedlist=critindlist+addlpages		
			
			strfordict=evalstring(evalstr2[firstentry:len(evalstr2)],instructions,'o',pervalue,None,combinedlist)
		
			evaldict=autoviv()
			evaldict['firstentry']=firstentry
			evaldict['cleanstring']=evalstr2
			evaldict['strfordict']=strfordict
							
			if instructions["algorithm"]["type"]=='sandwich':
				endpoint=instructions["algorithm"]["endpoint"][pervalue]
# 				print 'endpoint', endpoint, evalstr2[firstentry:len(evalstr2)]
				if endpoint!=None and endpoint in evalstr2[firstentry:len(evalstr2)]:
					evalstr3=evalstr2[firstentry:len(evalstr2)]
					endindex=evalstr3.index(endpoint)+1
					sandwichpath=[int(i) for i in evalstr3[0:endindex]]
# 					print 'sandwichpath',sandwichpath
# 					print 'firstentry', firstentry
# 					print 'endindex', evalstr2[firstentry:len(evalstr2)].index(endpoint)
# 					print 'evalstr2', evalstr3
					
					evaldict['sandwichpath']=sandwichpath
		
		if evalflg=='o':
			evaldict=[]
			for i in evalstr:	
				if int(i) in substr:
					evaldict.append(i)					
		
##  		print 'evaldict', evaldict
		
		return evaldict

# algo == type of algorithm to run
# algodict == dictionary to store results
# evaldict==dictionary storing data to analyze
# pervalue == key value from current sql row with which to look up args in instructions dict

# Path	OK
# Segment	OK
# EntryPoint OK
# EndPoint OK
# OPS	 OK
#PathLength	 OK

def buildalgoresults(algodict,evaldict,algoinstr,algo='d',pervalue=None,arraytodistinct=None,distinctgrain=None):	
	
	pathkey=','.join(str(i) for i in evaldict['sandwichpath'])

	print 'algo', algo
	
	if algo=='sandpre': 
		algodict['endpoint']=algoinstr['algorithm']['endpoint'][pervalue]
		algodict[pathkey]['entrypage']=evaldict['cleanstring'][0]
		algodict[pathkey]['length']=len(evaldict['sandwichpath'])
		entryindex=evaldict['firstentry']
		
		poilist=[i for i in evaldict['cleanstring'] if i in algoinstr['algorithm']['poi'][pervalue]]
			
		algodict[pathkey]['poi']=poilist
		
		print 'algodict',algodict

			
		
		
		
		
		
		
		
		
		
		
		
