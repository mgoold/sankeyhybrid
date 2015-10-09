
class autoviv(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def add(t,path,genorupdate='g',val=0):
	if genorupdate=='g':
		for node in path:
			t = t[node]	
	elif genorupdate=='i':
		for node in path:
			if path.index(node)==len(path)-1:
				t[node]=val
			t = t[node]		
	elif genorupdate=='u':
		print 'path',path,'val',val
		for node in path:
			print 'index',path.index(node)
			if path.index(node)==0:
				print 'case1', node, t[node]
				if node in t.keys():
					tempt=t[node]				
			elif path.index(node)==len(path)-1:
				if tempt.get(node)==None:
					print 'case2', node
					add(t,path,'i',val)
				elif node in tempt.keys():
					print 'case2b', node
					tempval=tempt[node]+val
					add(t,path,'i',tempval)
			else:
				print 'case3', node, tempt[node]
				if node in tempt.keys():
					tempt=tempt[node]	

	
	
