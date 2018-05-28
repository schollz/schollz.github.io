import glob

def process(fname):
	m = open(fname,'r').read()
	t = m.split('---')
	if len(t) != 3:
		return
	print(t[1])

	d = ''
	for l in t[1].split('\n'):
		if 'date' in l:
			d = l.split()[1].split('T')[0].split('-')
			t[1] += 'written: ["{}","{}","{}"]\n'.format(d[0],'-'.join(d[0:2]),'-'.join(d[0:3]))
		if 'written' in l:
			return
	with open(fname,'w') as f:
		f.write('---'.join(t))
	print(fname)
	
for fname in glob.glob("*.md"):
	process(fname)
