def clean_junk(string):
	newstring = string
	junk = [",._-;\'\"=/*+()[]"]
	for symbol in junk:
		newstring = newstring.replace(symbol, "")
	return newstring

def tagged(list_of_words):
	from nltk import pos_tag as tag
	return tag(list_of_words, tagset="universal")



class Corpus:

	def __init__(self, list_of_inputs):
		self.data = list_of_inputs
		self.length = len(self.joined_entries())  # in words
		self.entrylist = list_of_inputs
	def clean_junk(string):
		newstring = string
		junk = [",._-;\'\"=/*+()[]"]
		for symbol in junk:
			newstring = newstring.replace(symbol, "")
		return newstring

	def simple_standard_ttr(self):
		tokens = len(self.joined_entries())
		types = len(list(set(self.joined_entries())))
		return round(types / tokens, 2)

	def incremental_standard_ttr(self, chunksize):
		for portion in [self.joined_entries()[0: i] for i in range(0, self.length, chunksize)]:
			tokens = len(portion)
			types = len(set(portion))
			try:
				yield (tokens, types / tokens)
			except ZeroDivisionError:
				pass

	def average_new_words(self, chunksize):
		type_count = []
		diffs = []
		for portion in [self.joined_entries()[0: i] for i in range(0, self.length, chunksize)]:
			types = len(set(portion))
			type_count.append(types)
		for two in [type_count[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				diffs.append[diff]
			except IndexError:
				pass
		return sum(diffs) / len(diffs)

	def incremental_new_words(self, chunksize):
		type_count = []
		for portion in [self.joined_entries()[0: i] for i in range(0, self.length, chunksize)]:
			types = len(set(portion))
			type_count.append(types)
		for two in [type_count[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				yield diff
			except IndexError:
				pass

	def compute_average_pos_density(self, pos=["ALL"], res="ratio", until=-1):
		tags = ["NOUN",
				"ADV",
				"ADJ",
				"VERB",
				]
		tagged_corpus = self.tagged_corpus(until=until)
		if pos == ["ALL"]:
			densities = []
			for tag in tags:
				tag_count = 0
				for entry in tagged_corpus:
					if entry[1] == tag: tag_count += 1
				if res == "absolute": densities.append((tag, tag_count)) 
				elif res == "ratio": densities.append((tag, tag_count / len(tagged_corpus)))
			return densities
		else:
			densities = []
			for tag in pos:
				tag_count = 0
				for entry in tagged_corpus:
					if entry[1] == pos: tag_count += 1
				if res == "absolute": densities.append((tag, tag_count))
				elif res == "ratio": densities.append((tag, tag_count / len(tagged_corpus)))
			return densities
			

	def compute_average_pos_density_variation(self, pos, chunksize):
		counts = []
		diffs = []
		for portion in [tagged(self.joined_entries()[0: i]) for i in range(0, self.length, chunksize)]:
			tag_count = [elem[1] for elem in portion].count(pos)
			counts.append(tag_count)
		for two in [counts[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				diffs.append[diff]
			except IndexError:
				pass
		return sum(diffs) / len(diffs)

	def compute_incremental_pos_density_variation(self, pos, chunksize):
		counts = []
		for portion in [tagged(self.joined_entries()[0: i]) for i in range(0, self.length, chunksize)]:
			tag_count = [elem[1] for elem in portion].count(pos)
			counts.append(tag_count)
		for two in [counts[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				yield diff
			except IndexError:
				pass

	def joined_entries(self):
		one_big_entry = " ".join(self.data)
		remove_newline = one_big_entry.replace("\n", "")
		clean = clean_junk(remove_newline)
		lst = clean.split(" ")
		return [elem for elem in lst if elem != ""]

	def tagged_entries(self):
		from nltk import pos_tag as tag
		from nltk import post_tag_sents as tag_sents
		for entry in self.data:
			yield tag(entry, tagset="universal")

	def tagged_corpus(self, until=-1):
		from nltk import pos_tag_sents as tag
		from nltk import word_tokenize
		tokenized = [word_tokenize(sent) for sent in self.data]
		tagged =  tag(tokenized, tagset="universal")
		joined = []
		for sublist in tagged:
			for elem in sublist:
				joined.append(elem)
		return joined[0:until]

	def yield_entries(self, threshold=0):
		for entry in self.entrylist:
			x = CorpusEntry(entry)
			if x.length > threshold:
				yield CorpusEntry(entry)

	def tagged(list_of_words):
		from nltk import pos_tag as tag
		return tag(list_of_words, tagset="universal")

	@classmethod
	def from_xml_folder(cls, folder):
		from xml.etree import ElementTree as ET

	@classmethod
	def from_sql(cls, database_abspath, table_name, column_name_of_text_data):
		import sqlite3 as sql
		import pandas as pd
		with sql.connect(database_abspath) as conn:
			df = pd.read_sql_query("SELECT * FROM {}".format(table_name), conn)
			text = df[column_name_of_text_data].tolist()
		return cls(text)










class CorpusEntry:
	def __init__(self, string):
		self.rawdata = string
		self.data = clean_junk(string).split()
		self.length = len(self.data)
		# self.simple_ttr = self.simple_standard_ttr()
		# self.simple_pos_density = self.compute_average_pos_density()
		# self.average_new_words = self.average_new_words(100)

	@property
	def tagged(self):
		return tagged(self.data)

	def simple_standard_ttr(self):
		tokens = len(self.data)
		types = len(set(self.data))
		return round(types / tokens, 2)

	def incremental_standard_ttr(self, chunksize):
		for portion in [self.data[0: i] for i in range(0, self.length, chunksize)]:
			tokens = len(portion)
			types = len(set(portion))
			try:
				yield (tokens, types / tokens)
			except ZeroDivisionError:
				pass

	def average_new_words(self, chunksize):
		type_count = []
		diffs = []
		for portion in [self.data[0: i] for i in range(0, self.length, chunksize)]:
			types = len(set(portion))
			type_count.append(types)
		for two in [type_count[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				diffs.append(diff)
			except IndexError:
				pass
		try:
			return sum(diffs) / len(diffs)
		except ZeroDivisionError:
			pass

	def incremental_new_words(self, chunksize):
		type_count = []
		for portion in [self.data[0: i] for i in range(0, self.length, chunksize)]:
			types = len(set(portion))
			type_count.append(types)

		itercount = -2
		for two in [type_count[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				itercount += 2
				yield (itercount * chunksize, diff)
			except IndexError:
				pass

	def compute_average_pos_density(self, pos="ALL", until=-1, res="ratio"):
		tags = ["NOUN",
				"ADV",
				"ADJ",
				"VERB"
				]
		if until == -1: until = self.length
		if pos == "ALL":
			densities = []
			for tag in tags:
				tag_count = 0
				for entry in self.tagged[0:until]:
					if entry[1] == tag: tag_count += 1
				if res == "ratio": densities.append((tag, round(tag_count / until, 2)))
				elif res=="absolute": densities.append((tag, tag_count))
			return densities
		else:
			densities = []
			tag_count = 0
			for entry in self.tagged[0:until]:
				if entry[1] == pos: tag_count += 1
			
			if res == "ratio": return tag_count / until
			elif res == "absolute": return tag_count
			else: raise ValueError("res must be either 'absolute' or 'ratio'")

	def compute_average_pos_density_variation(self, pos=["NOUN", "VERB", "ADJ", "ADV"], chunksize=100, res="ratio"):
		get_tags = self.tagged
		for portion in [get_tags[0:i+chunksize] for i in range(0, len(get_tags), chunksize)]:
			found_tags = [item[1] for item in portion]
			portion_yield = []
			for tag in pos:
				if res=="ratio": posNum = found_tags.count(tag) / len(portion)
				elif res=="absolute": posNum = found_tags.count(tag)
				portion_yield.append((len(portion), tag, posNum))
			yield portion_yield

	def compute_incremental_pos_density_variation(self, pos=["NOUN", "VERB", "ADJ", "ADV"], chunksize=100):
		counts = []
		for portion in [tagged(self.data[0: i]) for i in range(0, self.length, chunksize)]:
			tag_count = [elem[1] for elem in portion].count(pos)
			counts.append(tag_count)
		for two in [counts[i: i+2] for i in range(0, len(type_count), 2)]:
			try:
				diff = two[1] - two[0]
				yield diff
			except IndexError:
				pass

	def pos_aware_ttr(self, until=-1, tags=["NOUN", "VERB", "ADJ", "ADV"]):
		tag = [elem[0] for elem in self.tagged[0:until] if elem[1] in tags]
		return len(set(tag)) / len(tag)

	def pos_aware_weighed_ttr(self, until=-1, tags=["NOUN", "VERB", "ADJ", "ADV"], weights=[1, 1, 1, 1]):
		pass


class RandomGroupedChisquare:

	def __init__(self, values, df_vals=[1,1,1], groups=[5,10,15], cycles=10, function="simple", 
		tags=["NOUN", "VERB", "ADJ", "ADV"], weights=[]):
		self.values = values
		self.df_vals = df_vals
		self.groups = groups
		self.cycles = cycles
		self.function = function
		self.weights = weights
		self.tags = tags
		self.tagged_values = [self.tagged(item) for item in self.values]

	def form_groups(self, length):
		import random
		formed_groups = []
		if self.function == "simple":
			random.shuffle(self.values)
			for formed_group in [self.values[i: i+length] for i in range(0, len(self.values), length)]:
				if len(formed_group) == length: formed_groups.append(formed_group)
			return formed_groups 
		else:
			random.shuffle(self.tagged_values)
			for formed_group in [self.tagged_values[i: i+length] for i in range(0, len(self.tagged_values), length)]:
				if len(formed_group) == length: formed_groups.append(formed_group)
			return formed_groups 

	def mean(self, values):
		return sum(values) / len(values)

	def chisquare(self, values):
		avg = self.mean(values)
		return sum([((val - avg) **2) / avg for val in values])

	def weighed_chisquare(self, group):
		weights = self.weights
		relevant_pos = []
		for item in group:
			item_data = []
			weighed_elements = []
			for tag in self.tags:
				filtered = self.yield_pos(item, tag)
				item_data.append(len(set(filtered)))
			for i, weight in zip(item_data, self.weights):
				weighed_unique = i * weight
				weighed_elements.append(weighed_unique)
			relevant_pos.append(sum(weighed_elements))
		avg = self.mean(relevant_pos)
		chi = sum([((val - avg) **2) / avg for val in relevant_pos])
		return chi

	def pos_aware_chisquare(self, group):
		relevant_pos = []
		for item in group:
			item_data = []
			for tag in self.tags:
				filtered = self.yield_pos(item, tag)
				item_data.append(len(set(filtered)))
			relevant_pos.append(sum(item_data))
		avg = self.mean(relevant_pos)
		chi = sum([((val - avg) **2) / avg for val in relevant_pos])
		return chi

	def yield_pos(self, tagged_text, tag):
		return [elem[0] for elem in tagged_text if elem[1] == tag]

	def tagged(self, string):
		newstring = clean_junk(string).replace("\n", "").split()
		return tagged(newstring)



	def runcalc(self):
		# returns result as list in following format = [[group1, true1, false1]]
		result = {}
		

		for i in range(self.cycles):
			for group, df_val in zip(self.groups, self.df_vals):
				header = "{} - {}".format(group, i+1)
				subres = []
				formed_groups = self.form_groups(group)
				for formed_group in formed_groups:
					if self.function == "simple": chi = self.chisquare(formed_group)
					elif self.function == "weighed": chi = self.weighed_chisquare(formed_group)
					elif self.function == "pos_only": chi = self.pos_aware_chisquare(formed_group)
					subres.append(chi <= df_val)
				result[header] = subres
		return result



class HumanVsMachine:
	
	def __init__(self, corpus, mode="sents", iters=0, pos_aware=True, lenrange=5, margin=10):
		import random
		self.margin = margin
		self.data = corpus
		self.mode = mode
		self.iters = iters
		self.pos_aware = pos_aware
		self.lenrange = lenrange
		if self.mode == "sents": self.elems = list(self.get_sents())
		if self.mode == "words": self.elems = list(self.get_words())

	def get_sents(self):
		for entry in self.data:
			sents = entry.split(".")
			for sent in sents:
				yield sent

	def get_words(self):
		for entry in self.data:
			clean = clean_junk(entry).replace("\n", "")
			spl = clean.split(" ")
			for word in spl:
				yield word

	def form_random_entry(self):
		import random
		choices = []
		for i in range(random.randint(self.lenrange, self.lenrange * 2)):
			choice = random.choice(self.elems)
			choices.append(choice)
		if self.mode == "sents":
			lst = []
			for sent in choices:
				for word in clean_junk(sent).replace("\n", "").split(" "):
					lst.append(word)
			return lst
		elif self.mode == "words":
			return choices

	def pick_random_entry(self, length):
		import random
		tenpercent = int(round((length / 100) * self.margin))
		# print(tenpercent)
		r1 = length - tenpercent
		r2 = length + tenpercent
		eligible = []
		# print(list(range(r1, r2)))
		for entry in self.data:
			leng = len(clean_junk(entry).replace("\n","").split(" "))
			# print(leng)
			if leng in list(range(r1, r2)):
				eligible.append(entry)
		# print("eligible: ", len(eligible))
		choice = random.choice(eligible)
		return clean_junk(choice).replace("\n", "").split()

	def chisquare(self, elem1, elem2):
		df_val = 3.841 # 1 Degree of Freedom
		types1 = len(set(elem1))
		types2 = len(set(elem2))
		avg = (types1 + types2) / 2
		chi = sum([((types1 - avg) **2) / avg, ((types2 - avg) **2) / avg])
		return chi <= df_val

	def pos_chisquare(self, elem1, elem2, tags=["NOUN", "VERB", "ADJ", "ADV"]):
		df_val = 3.841 # 1 Degree of Freedom
		filtered1 = [elem[0] for elem in tagged([elem for elem in elem1 if elem != ""]) if elem[1] in tags]
		filtered2 = [elem[0] for elem in tagged([elem for elem in elem2 if elem != ""]) if elem[1] in tags]

		types1 = len(set(filtered1))
		types2 = len(set(filtered2))
		avg = (types1 + types2) / 2
		chi = sum([((types1 - avg) **2) / avg, ((types2 - avg) **2) / avg])
		return chi <= df_val

	def runcalc(self):
		res = []
		if self.iters == 0:
			while True:
				try:
					rand = self.form_random_entry()
					hum = self.pick_random_entry(len(rand))
					simple_chisquare = self.chisquare(rand, hum)
					pos_chisquare = self.pos_chisquare(rand, hum)
					yield (len(rand), len(hum), simple_chisquare, pos_chisquare)
				except IndexError: pass

		


		else:


			counter = self.iters
			while counter > 0:
				try:
					rand = self.form_random_entry()
					# print(len(rand))
					hum = self.pick_random_entry(len(rand))
					simple_chisquare = self.chisquare(rand, hum)
					pos_chisquare = self.pos_chisquare(rand, hum)
					counter = counter - 1
					# print("found one!")
					yield (len(rand), len(hum), simple_chisquare, pos_chisquare)
				except IndexError: pass

