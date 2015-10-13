
import json

def add(t,path,genorupdate='g',val=0,brkoval=0,keynames=None,keyvals=None):
	if genorupdate=='g':
		for node in path:
			t = t[node]	
	elif genorupdate=='i':
# 		print 'pathininsert', path
		rowct2=0;
# 		print 'rowlen', path, len(path)
		for node in path:
			if rowct2==len(path)-1:
# 				print 'assigning totals'
				t[node]['total']=val
# 				print 'keynames',keynames, keyvals
				for k in keynames:
# 					print 'k is', keyvals[keynames.index(k)]
					 if keyvals[keynames.index(k)] not in t[node]['breakouts'][k].keys():
					 	t[node]['breakouts'][k][keyvals[keynames.index(k)]]=brkoval
					 else:
						 t[node]['breakouts'][k][keyvals[keynames.index(k)]]+=brkoval	
			rowct2+=1							 
			t = t[node]		
# 		print 't', json.dumps(t)	
		
	elif genorupdate=='u':
# 		print 'in update'
# 		print 'pathinupdate',path
		rowct=0;
		temppath=[]
		for node in path:
			temppath.append(node)	
# 			print 'rowct in update', rowct, 'node', node
			if rowct==0:
# 				print 'rowct==0'
				tempt=t[node]	
			else:
# 				print 'rowct>0'
				tempt=tempt[node]		
# 			print 'temppath',temppath	
# 			print 'tempt.get(node)',node, tempt, tempt.get(node)

			rowct+=1
			
			if tempt.get('total')==None:
# 				print 'nototal', keynames,keyvals,type(temppath)
				add(t,temppath,'i',val,brkoval,keynames,keyvals)
			else:
# 				print 'havetotal',keynames,keyvals,type(temppath)
				tempval=tempt['total']
	# 				print 'tempval total',tempval
				tempval+=1

				add(t,temppath,'i',tempval,brkoval,keynames,keyvals) 
				

