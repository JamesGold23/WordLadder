class nil_tree:
	def __init__(self):
		self.entry = 'nil'

	def __repr__(self):
		return self.entry

nil = nil_tree()

class Tree:
	"""
	>>> t = Tree(1)
    >>> t.size
    1
    >>> t.children
    []
    >>> t.parent
    nil
    >>> t.set_children( [ Tree(5, [Tree(2, [Tree(7)])]), Tree(3) ] )
    >>> t.size
    5
    >>> t.child(0).child(0).child(0).ancestors
    [2, 5, 1]
    """
	def __init__(self, entry=None, children = []):
		assert type(children) is list
		for child in children:
			assert type(child) is Tree

		self.entry = entry
		self.children = []
		self.set_children(children)
		self.parent = nil		

	def set_children(self, children):
		assert type(children) is list
		for child in children:
			assert type(child) is Tree

		for child in children:
			self.add_child(self, child)

	def add_child(self, child):
		assert type(child) is Tree
		child.parent = self
		self.children.append(child)

	@property
	def size(self):
		num_children = len(self.children)
		if num_children == 0:
			return 1
		else:
			return 1 + sum(child.size for child in self.children)

	@property
	def ancestors(self):
		if self.parent is nil:
			return []
		return [self.parent.entry] + self.parent.ancestors

	def is_ancestor(self, arg):
		return arg in self.ancestors

	def child(self, index):
		assert type(index) is int and index >=0 and index < len(self.children)
		return self.children[index]

	def __str__(self):
		child_entries = []
		for child in self.children:
			child_entries.append(child.entry)
		return ('Entry: {0}' + '\n' + 'Children: {1}' + '\n' + 'Parent: {2}').format(self.entry, child_entries, self.parent.entry)

WORDS_FILE = 'EnglishWords.txt'

def create_dict(words_file = WORDS_FILE):
	#read the list of words
	with open(words_file, 'r') as f:
	    wordlist = [line.strip() for line in f]

	#find largest word length in the list
	max_len = max(len(w) for w in wordlist)

	#partition the list by length of words
	lists = []
	for length in range(1, max_len+1):
		lists.append( list( w for w in wordlist if len(w) == length ) )

	#create dictionary mapping length of word to list of words of that length
	word_dict = {}
	for l in lists:
		if len(l) > 0:
			word_dict[len(l[0])] = l

	return word_dict

def differ_by_one(a,b):
	"""
	>>> differ_by_one('a', 'b')
	True
	>>> differ_by_one('cake', 'fake')
	True
	>>> differ_by_one('happy', 'soppy')
	False
    """
	check_strs(a,b)
	diffs = 0
	for i in range(len(a)):
		if a[i] != b[i]:
			diffs += 1
	return diffs == 1

def find_sequences(a, b, words, links=5):
	
	def generate_children(t):
		nonlocal num_sequences
		for w in words:
			if differ_by_one(t.entry, w) and not t.is_ancestor(w):
				t.add_child(Tree(w))
				if w == b:
					num_sequences += 1
					print(t.children[-1].ancestors[::-1] + [w])

	num_sequences = 0	
	root = Tree(a)
	parents = [root]
	all_children = []
	for _ in range(1, links):
		for parent in parents:
			generate_children(parent)
			for child in parent.children:
				all_children.append(child)
		parents = all_children
		all_children = []

	print('Total sequences:', num_sequences)
	print('Tree size:', root.size)

def check_strs(a, b):
	assert type(a) is str and type(b) is str and len(a) == len(b) 

def main():
	print('Creating word list.')
	dic = create_dict()
	print('Success.')
	while(True):
		try:
			#get input from user
			input_line = input('Enter two words of the same length and the max number of words you want in each sequence, separated by spaces. For example: cat dog 4 --> ')
			input1, input2, links = input_line.split()[0], input_line.split()[1], input_line.split()[2]
			check_strs(input1, input2)
			#get list of words of same length as the inputs
			words = dic[len(input1)]
			assert input1 in words and input2 in words 
			find_sequences(input1, input2, words, int(links))
		except AssertionError as e:
			print(e)

main()

		




