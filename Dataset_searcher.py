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
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514'"
		                        "GROUP by UID ORDER BY count(UID) DESC;")
		simultaneous_interpretation_man_list = [(self.show_me_your_id(row[0]), row[-1]) for row in cursor if row[-1] > man_threshold]
		return simultaneous_interpretation_man_list

	def show_me_your_id(self, UID):
		url = f'https://api.bilibili.com/x/space/acc/info?mid={UID}'
		res = requests.get(url)
		return res.json()['data']['name']

	def select_date_within(self, start_date, end_date):
		cursor = self.c.execute("SELECT YMD_time, UID, message, count(YMD_time) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND YMD_time BETWEEN ? AND ?"
		                        "GROUP by YMD_time ORDER BY count(YMD_time) DESC;", (start_date, end_date))
		return [row for row in cursor]

	def show_target_interpretation_from_UID(self, input_UID):

		# Make sure you make (input_UID,) a tuple by adding a comma
		cursor = self.c.execute("SELECT UID, message "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND UID = ?;", (input_UID,))
		return [row for row in cursor]

if __name__ == '__main__':
	ds = Dataset_searcher("test.db")
	ds.connect_dataset()

	date_within = ds.select_date_within(start_date='2019-09-01', end_date='2019-09-30')
	all_interpretation = ds.show_target_interpretation_from_UID(input_UID='268065764')

	start_time = time.time()
	simultaneous_interpretation_man_list = ds.select_simultaneous_interpretation_man(man_threshold=100)
	print("simultaneous_interpretation_man selected within {}".format("--- %s seconds ---" % (time.time() - start_time)))
	print(simultaneous_interpretation_man_list)