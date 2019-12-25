# Created by pren1 at 5/24/2019
# process data from the .txt files
import pdb
import numpy as np

class txt_processor:
	def __init__(self, path_to_txt):
		self.path = path_to_txt
		self.txt_list = []

	def read_target_txt(self):
		# Read in target txt into a string list
		if not self.path.endswith('.txt'):
			assert (1 == 0), "extension is not txt"
		with open(self.path, "r", encoding='utf-8') as txtfile:
			data = txtfile.readlines()
		# Remove '\n'
		self.txt_list = [string.rstrip('\n') for string in data]
		# process the readin list with format: [Time, UID, Message]
		self.txt_list = self.preprocess_readin_list()
		# Turn to numpy array...
		try:
			self.txt_list = np.asarray(self.txt_list)
		except MemoryError:
			print("error at %s" % self.path)
			return []
		return self.txt_list

	def preprocess_readin_list(self):
		# Remove the SPEAKERNUM, and append Time stamp to each message
		new_list = []
		# Avoid bug
		current_time_stamp = 0
		for single_string in self.txt_list:
			if single_string[:4] == 'TIME':
				current_time_stamp = self.Time_to_stamp_number(single_string)
			elif single_string[:10] == 'SPEAKERNUM':
				continue
			else:
				
				sep = single_string.split(':', 2)
				if len(sep) == 1 and sep[0] == 'V2':
					continue
				
				else:
					if len(sep) == 1: #if time_stamp and UID are NOT RECORDED
						sep = ['0', '0'] + sep
					elif len(sep) == 2: #if time_stamp is NOT RECORDED
						try:
							int(sep[0])
							sep = ['0'] + sep #if sep[0] is numbers, UID is RECORDED
						except ValueError:
							sep = ['0', '0', single_string] #otherwise, UID is NOT RECORDED
					else:
						try:
							int(sep[1]) 
						except ValueError: #maybe time_stamp is NOT RECORDED
							try:
								int(sep[0])
								sep = ['0', sep[0], sep[1]+':'+sep[2]] #here sep[0] records UID
							except ValueError: #time_stamp is NOT RECORDED
								sep = ['0', '0', single_string]
					new_list.append([current_time_stamp, sep[1], sep[2]])
		return new_list

	def Time_to_stamp_number(self, time_string):
		assert time_string[:4] == 'TIME'
		# First, remove the first four characters: 'TIME'
		time_string = time_string[4:]
		# Then, find the position of the string 'ONLINE'
		end_pos = time_string.find('ONLINE')
		# After that, get the time string we need:
		time_string = time_string[:end_pos].split(':')
		assert len(time_string) == 2
		hour = int(time_string[0])
		minute = int(time_string[1])
		fin_time = hour * 60 + minute
		return fin_time