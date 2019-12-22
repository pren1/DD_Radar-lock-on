# Created by pren1 at 12/20/2019
# Manipulate dataset
import pdb
import sqlite3
import time
import requests
import pandas as pd
from tqdm import tqdm
import csv

class Dataset_searcher(object):
	def __init__(self, data_set_name):
		self.data_set_name = data_set_name
		reader = csv.reader(open('room_id_nick_name_chart.csv'))
		self.room_id_df = {}
		for row in reader:
			key = row[0].split('\t')[0]
			if len(key) == 0:
				# ignore head
				pass
			if key in self.room_id_df:
				# implement your duplicate row handling here
				assert 1==0, "Error read in dict"
			self.room_id_df[key] = row[0].split('\t')[1]

	def connect_dataset(self):
		self.conn = sqlite3.connect(self.data_set_name)
		self.c = self.conn.cursor()
		print("Opened database successfully")
		# Run this one time, please keep this line Commented unless you loss room_id_nick_name_chart.csv or you wanna update it
		# self.build_fast_name_chart()

	def build_fast_name_chart(self):
		'First, get all the room_id'
		cursor = self.c.execute("SELECT room_id from DD_DANMAKU_TABLE;")
		room_id_set = set([row for row in cursor])
		df = pd.DataFrame(columns=['room_nick_name'])
		for single in tqdm(room_id_set):
			df.loc[single] = self.show_me_your_room_id(single[0])
		df.to_csv("room_id_nick_name_chart.csv", sep='\t', encoding='utf-8')

	def select_simultaneous_interpretation_man(self, man_threshold, show_name):
		'man_threshold: Only record the UID whose interpretation is above this threshold'
		'Return format: (user_id, danmaku count)'
		cursor = self.c.execute("SELECT UID, message, count(UID) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514'"
		                        "GROUP by UID ORDER BY count(UID) DESC;")
		simultaneous_interpretation_man_list = [(self.show_me_your_id(row[0], show_name), row[-1]) for row in cursor if row[-1] > man_threshold]
		return simultaneous_interpretation_man_list

	def show_me_your_id(self, UID, show_name):
		if not show_name:
			return UID
		'Get nickname from UID'
		url = f'https://api.bilibili.com/x/space/acc/info?mid={UID}'
		res = requests.get(url)
		return res.json()['data']['name']

	def show_me_your_room_id(self, room_id):
		'Get room id name'
		url = f'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={room_id}'
		res = requests.get(url)
		return res.json()['data']['info']['uname']

	def prefetched_room_id(self, room_id):
		'Get prefetched room id name, this method is faster than show_me_your_room_id'
		return self.room_id_df[room_id]

	def select_date_within(self, start_date, end_date):
		'Check interpretations within an time interval, deprecated, and never used. Just for debug purpose'
		cursor = self.c.execute("SELECT YMD_time, UID, message, count(YMD_time) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND YMD_time BETWEEN ? AND ?"
		                        "GROUP by YMD_time ORDER BY count(YMD_time) DESC;", (start_date, end_date))
		return [row for row in cursor]

	def show_target_interpretation_from_UID(self, input_UID):
		'Return all the interpretation that has been sent by input_UID'
		'Return format: (user_id, danmaku)'
		# Make sure you make (input_UID,) a tuple by adding a comma
		cursor = self.c.execute("SELECT UID, message "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND UID = ?;", (input_UID,))
		return [row for row in cursor]

	def show_all_danmaku_from_UID(self, input_UID):
		'Return all the danmaku that has been sent by input_UID'
		'Return format: (user_id, danmaku)'
		cursor = self.c.execute("SELECT UID, message "
		                        "from DD_DANMAKU_TABLE WHERE UID != '114514' AND UID = ?;",
		                        (input_UID,))
		return [row for row in cursor]

	def Single_UID_interpretation_timeline(self, input_UID):
		'Show the timeline of interpretation numbers sent by input_UID'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, message, count(message) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND UID = ?"
		                        "GROUP by YMD_time, room_id ORDER BY YMD_time;", (input_UID,))
		return [[row[0], self.prefetched_room_id(row[1]), row[2], row[4]] for row in cursor]

	def Single_UID_all_danmaku_timeline(self, input_UID):
		'Show the timeline of all the danmaku numbers sent by input_UID'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, message, count(message) "
		                        "from DD_DANMAKU_TABLE WHERE UID != '114514' AND UID = ?"
		                        "GROUP by YMD_time, room_id ORDER BY YMD_time;", (input_UID,))
		return [[row[0], self.prefetched_room_id(row[1]), row[2], row[4]] for row in cursor]

	def Single_live_roow_interpretation_timeline(self, input_room_id, pure_uid_man_list):
		'Show the timeline of interpretation within the target live room'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		man_list_length = len(pure_uid_man_list)
		'Combine the roow_id as total inputs'
		pure_uid_man_list.insert(0, input_room_id)
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, message, count(message) "
		                        "from DD_DANMAKU_TABLE WHERE substr(message,1,1) = '【' AND substr(message,-1,1) = '】' AND UID != '114514' AND room_id = ? AND UID in ({seq})"
		                        "GROUP by YMD_time, UID ORDER BY YMD_time;".format(seq=','.join(['?']*man_list_length)), pure_uid_man_list)
		return [(row[0], row[1], row[2], row[4]) for row in cursor]

if __name__ == '__main__':
	ds = Dataset_searcher("test.db")
	ds.connect_dataset()
	all_interpretation = ds.show_target_interpretation_from_UID(input_UID='739848')
	simultaneous_interpretation_man_list = ds.select_simultaneous_interpretation_man(man_threshold=100, show_name=False)
	date_within = ds.select_date_within(start_date='2019-09-01', end_date='2019-09-30')
	all_interpretation = ds.show_target_interpretation_from_UID(input_UID='739848')
	all_danmaku = ds.show_all_danmaku_from_UID(input_UID='268065764')
	single_uid_interpretation_timeline = ds.Single_UID_interpretation_timeline(input_UID='37718180')
	single_uid_all_danmaku_timeline = ds.Single_UID_all_danmaku_timeline(input_UID='37718180')
	pure_uid_man_list = [row[0] for row in simultaneous_interpretation_man_list]
	single_live_roow_interpretation_timeline = ds.Single_live_roow_interpretation_timeline(input_room_id='11588230', pure_uid_man_list=pure_uid_man_list)