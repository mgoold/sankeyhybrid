import json

def add(t,path,genorupdate='g',val=0,brkoval=0,keynames=None,keyvals=None,algoflag='Default'):
# 	print 'in generatedict', 
	if genorupdate=='g':
		for node in path:
			t = t[node]	
	elif genorupdate=='i':
		rowct2=0;
		for node in path:
			if rowct2==len(path)-1:
				t[node]['total']=val
				for k in keynames:
					 if keyvals[keynames.index(k)] not in t[node]['breakouts'][k].keys():
					 	t[node]['breakouts'][k][keyvals[keynames.index(k)]]=brkoval
					 else:
						 t[node]['breakouts'][k][keyvals[keynames.index(k)]]+=brkoval	
			rowct2+=1							 
			t = t[node]		
				
	elif genorupdate=='u':
		rowct=0;
		temppath=[]
		for node in path:
			temppath.append(node)	

			if rowct==0:
				tempt=t[node]	
			else:
				tempt=tempt[node]		
			
			if tempt.get('total')==None:
				add(t,temppath,'i',val,brkoval,keynames,keyvals)
			else:
				tempval=tempt['total']
				tempval+=1

				add(t,temppath,'i',tempval,brkoval,keynames,keyvals) 

			rowct+=1
	
# def buildlistdict(node,dict):
# 	for k in node.keys():
# 		if node[k]={}:
# 			dict=buildlistdict(node[k],dict)
# 		else:
# 			dict[k]=[]
# 		
# 		
# 				
# def buildvistarray(t,path):
# 		rowct=0;
# 		temppath=[]
# 		returndict=autoviv()
# 		
# 		for node in path:
# 			temppath.append(node)	
# 
# 			if rowct==0:
# 				tempt=t[node]	
# 				returndict['total']=[]
# 				if tempt.get('breakouts')!=None:
# 					for k in tempt['breakouts'].keys()
# 						returndict['breakouts']
# 			else:
# 				tempt=tempt[node]		
# 			
# 			tempt['total']
# 
# 			
# 
# 			add(t,temppath,'i',tempval,brkoval,keynames,keyvals)
# 
# 			rowct+=1


