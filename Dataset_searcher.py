# Created by pren1 at 12/20/2019
import pdb
import sqlite3
import time
import requests

class Dataset_searcher(object):
	def __init__(self, data_set_name):
		self.data_set_name = data_set_name

	def connect_dataset(self):
		self.conn = sqlite3.connect(self.data_set_name)
		self.c = self.conn.cursor()
		print("Opened database successfully")

	def select_simultaneous_interpretation_man(self, man_threshold):
		'man_threshold: Only record the UID whose interpretation is above this threshold'
		cursor = self.c.execute("SELECT UID, message, count(UID) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】'"
		                        "GROUP by UID ORDER BY count(UID) DESC;")
		simultaneous_interpretation_man_list = [(self.show_me_your_id(row[0]), row[-1]) for row in cursor if row[-1] > man_threshold]
		return simultaneous_interpretation_man_list

	def show_me_your_id(self, UID):
		url = f'https://api.bilibili.com/x/space/acc/info?mid={UID}'
		res = requests.get(url)
		return res.json()['data']['name']

if __name__ == '__main__':
	ds = Dataset_searcher("test.db")
	ds.connect_dataset()
	start_time = time.time()
	simultaneous_interpretation_man_list = ds.select_simultaneous_interpretation_man(man_threshold=100)
	print("simultaneous_interpretation_man selected within {}".format("--- %s seconds ---" % (time.time() - start_time)))
	print(simultaneous_interpretation_man_list)