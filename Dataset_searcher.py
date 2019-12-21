# Created by pren1 at 12/20/2019
import pdb
import sqlite3
from tqdm import tqdm

class Dataset_searcher(object):
	def __init__(self, data_set_name):
		self.data_set_name = data_set_name

	def connect_dataset(self):
		self.conn = sqlite3.connect(self.data_set_name)
		self.c = self.conn.cursor()
		print("Opened database successfully")

	def select_Simultaneous_interpretation_man(self):
		cursor = self.c.execute("SELECT room_id, YMD_time, UID, message, count(UID) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】'"
		                        "GROUP by UID ORDER BY count(UID) DESC;")
		test = [row for row in cursor]
		pdb.set_trace()

if __name__ == '__main__':
	ds = Dataset_searcher("test.db")
	ds.connect_dataset()
	ds.select_Simultaneous_interpretation_man()
