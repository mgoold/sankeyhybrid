
# pathkey ['1843', '1843', '1843', '1859', '1859', '1859', '402', '402', '1859', '1843', '1843']

import json

def add(t,path,genorupdate='g',val=0,keynames=None,keyvals=None):
	if genorupdate=='g':
		for node in path:
			t = t[node]	
	elif genorupdate=='i':
		print 'ininsert'
		rowct2=0;
		print 'rowlen', len(path)
		for node in path:
			print 'rowct2',rowct2, node, val
			if rowct2==len(path)-1:
				print 'assigning totals'
				t[node]['total']=val
				if keynames!=None:
					for k in keynames:
						 t[node]['breakouts'][k][keyvals[keynames.index(k)]]=val	
			rowct2+=1							 
			t = t[node]		
		print 't', json.dumps(t)	
	elif genorupdate=='u':
		print 'in update'
		rowct=0;
		for node in path:			
			if rowct==0:
				print 'rowct==0'
				temppath=[node]
				tempt=t[node]	
			else:
				print 'rowct>0'
				temppath=path[0:rowct]
				tempt=tempt[node]				
			print 'tempt.get(node)',node, tempt, tempt.get(node)
			
			if tempt.get('total')==None:
				print 'insertval', keynames,keyvals
				add(t,temppath,'i',val,keynames,keyvals)
			else:
				print 'updateval'
				tempval=tempt['total']
				print 'tempval total',tempval
				tempval+=1
				add(t,temppath,'i',tempval,keynames,keyvals) 
			rowct+=1
