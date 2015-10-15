import json


def add(t,path,genorupdate='g',val=0,brkoval=0,keynames=None,keyvals=None,algoflag='Default'):
# 	print 'in generatedict', 
	if genorupdate=='g':
		for node in path:
			t = t[node]	
	elif genorupdate in('i','i2'):
		print 'getorupdate',genorupdate
		rowct2=0;
		for node in path:
			if rowct2==len(path)-1:
				t[node]['nodetotal']=val
				for k in keynames:					
					if keyvals[keynames.index(k)] not in t[node]['vartotals'][k].keys():
						t[node]['vartotals'][k][keyvals[keynames.index(k)]]=brkoval
					else:
						t[node]['vartotals'][k][keyvals[keynames.index(k)]]+=brkoval	

				if genorupdate=='i2':
					print 'in i2'
					t2=t[node]['breakoutotals']							
					add(t2,keyvals,'u2',val,brkoval,keynames,keyvals)	

					t[node]['breakoutotals']=t2
					
										
			rowct2+=1										 
			t = t[node]		

	elif genorupdate in('i3'):
		rowct2=0;
		for node in path:
			if rowct2==len(path)-1:
				t[node]['breakouttotal']=val
										
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
			
			if tempt.get('nodetotal')==None:
				add(t,temppath,'i2',val,brkoval,keynames,keyvals)
			else:
				tempval=tempt['nodetotal']
				tempval+=val

				add(t,temppath,'i2',tempval,brkoval,keynames,keyvals) 

			rowct+=1

	elif genorupdate=='u2':
		rowct=0;
		temppath=[]
		print 'in u2 path', path
		for node in path:
			temppath.append(node)	

			if rowct==0:
				tempt=t[node]	
			else:
				tempt=tempt[node]		
			
			print 'in u2 node',node, 'tempt',tempt
			
			if tempt.get('breakouttotal')==None:
				print 'in u2 none'
				add(t,temppath,'i3',1,brkoval,keynames,keyvals)
			else:
				print 'in u2 have total'
				tempval=tempt['breakouttotal']
				tempval+=1

				add(t,temppath,'i3',tempval,brkoval,keynames,keyvals) 

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


