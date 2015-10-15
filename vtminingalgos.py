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

# ma.buildalgoresults(algo='d',evaldict,algoinstr,arraytodistinct,distinctgrain)	

# //needed arguments: 
# dictionary to build /instructionsdict
# complete set of pages to eval /evalstr
# entry page /aid
# final page /aid
# intermediatePOIS /aid

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
			
			strfordict=evalstring(evalstr2[firstentry:len(evalstr2)],None,'o',pervalue,None,combinedlist)
		
			evaldict=autoviv()
			evaldict['firstentry']=firstentry
			evaldict['cleanstring']=evalstr2
			evaldict['strfordict']=strfordict
		
# 		if evalflg=='s':
# 			endpoint=instdict["algorithm"]["Sandwich"]["endpoint"][pervalue],
# 			if endpoint!=None and endpoint in evalstr2[firstentry:len(evalstr2)]:
# 				sandwichpath=[int(i) for i in evalstr2[firstentry:endpoint]]
# 				evaldict['Sandwich']=sandwichpath
		
		if evalflg=='o':
			evaldict=[]
			for i in evalstr:	
				if int(i) in substr:
					evaldict.append(i)					
		
# 		print 'evaldict', evaldict
		
		return evaldict


def buildalgoresults(algo='d',pervalue=None,evaldict,algoinstr,arraytodistinct=None,distinctgrain=None):	
	pathkey=','.join(substring)
	
	if algo=='SandPre': 
		d['endpoint']=algoinstr['Sandwich']['endpoint'][pervalue]
		d[pathkey]['entrypage']=evaldict['cleanstring'][0]
		d[pathkey]['length']=len(pathkey)
		entryindex=evaldict['firstentry']
		poi=algoinstr['Sandwich']['poi'][pervalue]
		for k in keynames:
			d[pathkey]['breakouts']=[k]=[keyvals[keynames.index(k)]]
		temppoi=evalstring('o',evaldict['cleanstring'][1:entryindex],poi)
		d[pathkey]['POIs']=','.join(temppoi)
# 
# def fillalgovisits(algo='d',evaldict,algodict):	
# 	
# 	if algodict=='SandPost': 
# 		for k in algodict.keys():
			
			
		
		
		
		
		
		
		
		
		
		
		
