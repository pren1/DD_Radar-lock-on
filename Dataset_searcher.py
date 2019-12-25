# Created by pren1 at 12/20/2019
# Manipulate dataset
import pdb
import sqlite3
import time
import requests
import pandas as pd
from tqdm import tqdm
import csv

from constants import DATABASE_NAME, ROOM_ID_CSV, MAN_ID_AND_NICKNAME_CSV

class Dataset_searcher(object):
	def __init__(self, data_set_name):
		self.data_set_name = data_set_name
		self.room_id_df = self.read_in_target_csv(csv_name=ROOM_ID_CSV)
		self.interpretation_man_df = self.read_in_target_csv(csv_name=MAN_ID_AND_NICKNAME_CSV)

	def read_in_target_csv(self, csv_name):
		reader = csv.reader(open(csv_name,encoding='utf-8'))
		room_id_df = {}
		for row in reader:
			key = row[0].split('\t')[0]
			if len(key) == 0:
				# ignore head
				continue
			if key in room_id_df:
				# implement your duplicate row handling here
				assert 1 == 0, "Error read in dict"
			room_id_df[int(key)] = row[0].split('\t')[1]
		return room_id_df

	def connect_dataset(self):
		self.conn = sqlite3.connect(self.data_set_name)
		self.c = self.conn.cursor()
		print("Opened database successfully")

	def build_fast_name_chart(self):
		'Build this for fast room nick name fetch'
		cursor = self.c.execute("SELECT room_id from DD_DANMAKU_TABLE;")
		room_id_set = set([row for row in cursor])
		df = pd.DataFrame(columns=['room_nick_name'])
		for single in tqdm(room_id_set):
			df.loc[single] = self.show_me_your_room_id(single[0])
		df.to_csv("room_id_nick_name_chart.csv", sep='\t', encoding='utf-8')

	def build_simultaneous_interpretation_man_name_chart(self, pure_uid_man_list):
		'Build this for fast simultaneous_interpretation_man nick name fetch'
		df = pd.DataFrame(columns=['man_nick_name'])
		for single in tqdm(pure_uid_man_list):
			df.loc[single] = self.show_me_your_id(single, show_name=True)
		df.to_csv("man_id_nick_name_chart.csv", sep='\t', encoding='utf-8')

	def select_simultaneous_interpretation_man(self, man_threshold, show_name):
		'man_threshold: Only record the UID whose interpretation is above this threshold'
		'Return format: (UID, danmaku count, total danmaku length)'
		cursor = self.c.execute("SELECT UID, count(*), sum(message_length) "
		                        "from DD_DANMAKU_TABLE WHERE UID != 0 "
		                        "GROUP by UID ORDER BY count(*) DESC;")
		simultaneous_interpretation_man_list = [row for row in cursor if row[1] > man_threshold]
		return simultaneous_interpretation_man_list
	
	def get_prefer_room(self, intp_man_info):
		'format of intp_man_info: (UID, danmaku count, total danmaku length)'
		cursor = self.c.execute("SELECT UID, room_id, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID != 0 "
		                        "GROUP by UID, room_id ORDER BY count(*) DESC;")
		perfer_room = {}
		for row in cursor:
			if row[0] not in perfer_room:
				perfer_room[row[0]] = (row[1], row[2]) #format: (room_id, count(room_id))
		return [row + (self.room_id_df[perfer_room[row[0]][0]] + '('+str(round(perfer_room[row[0]][1] / row[1] * 100)) + '%)',) for row in intp_man_info]

	def show_me_your_id(self, UID, show_name):
		if not show_name:
			return UID
		'Get nickname from UID'
		url = 'https://api.bilibili.com/x/space/acc/info?mid='+str(UID)
		#print(url)
		res = requests.get(url)
		name = res.json()['data']['name']
		while len(name) == 0:
			time.sleep(0.1)
			res = requests.get(url)
			name = res.json()['data']['name']
		return name

	def show_me_your_room_id(self, room_id):
		'Get room id name'
		url = 'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid='+str(room_id)
		res = requests.get(url)
		return res.json()['data']['info']['uname']

	def prefetched_room_id(self, room_id):
		'Get prefetched room id name, this method is faster than show_me_your_room_id'
		#print("id="+room_id)
		return self.room_id_df[room_id]

	def prefetched_man_id(self, man_id):
		'Get prefetched man id name, this method is faster than show_your_id'
		try:
			return self.interpretation_man_df[man_id]
		except KeyError:
			return self.show_me_your_id(man_id, show_name=True)
	
	def select_date_within(self, start_date, end_date):
		'Check interpretations within an time interval, deprecated, and never used. Just for debug purpose'
		cursor = self.c.execute("SELECT YMD_time, UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID != 0 AND YMD_time BETWEEN ? AND ? "
		                        "GROUP by YMD_time ORDER BY count(*) DESC;", (start_date, end_date))
		return [row for row in cursor]

	def show_target_interpretation_from_UID(self, input_UID):
		'Return all the interpretation that has been sent by input_UID'
		'Return format: (user_id, danmaku)'
		# Make sure you make (input_UID,) a tuple by adding a comma
		cursor = self.c.execute("SELECT UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID = ?;", (input_UID,))
		return [row for row in cursor]

	def show_all_danmaku_from_UID(self, input_UID):
		'Return all the danmaku that has been sent by input_UID'
		'Return format: (user_id, danmaku)'
		cursor = self.c.execute("SELECT UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID = ?;",
		                        (input_UID,))
		return [row for row in cursor]

	def Single_UID_interpretation_timeline(self, input_UID):
		'Show the timeline of interpretation numbers sent by input_UID'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID = ? "
		                        "GROUP by YMD_time, room_id ORDER BY YMD_time;", (input_UID,))
		return [[row[0], self.prefetched_room_id(row[1]), row[2], row[3]] for row in cursor]

	def Single_UID_all_danmaku_timeline(self, input_UID):
		'Show the timeline of all the danmaku numbers sent by input_UID'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE UID = ?"
		                        "GROUP by YMD_time, room_id ORDER BY YMD_time;", (input_UID,))
		return [[row[0], self.prefetched_room_id(row[1]), row[2], row[3]] for row in cursor]

	def Single_live_room_interpretation_timeline(self, input_room_id, pure_uid_man_list):
		'Show the timeline of interpretation within the target live room'
		'Return format: (YMD_time, room_id, user_id, danmaku_count)'
		man_list_length = len(pure_uid_man_list)
		'Combine the roow_id as total inputs'
		pure_uid_man_list.insert(0, input_room_id)
		cursor = self.c.execute("SELECT YMD_time, room_id, UID, count(*) "
		                        "from DD_DANMAKU_TABLE WHERE room_id = ? AND UID in ({seq})"
		                        "GROUP by YMD_time, UID ORDER BY YMD_time;".format(seq=','.join(['?']*man_list_length)), pure_uid_man_list)
		return [(row[0], row[1], self.prefetched_man_id(row[2]), row[3]) for row in cursor]

if __name__ == '__main__':
	'demo'
	ds = Dataset_searcher(DATABASE_NAME)
	ds.connect_dataset()
	all_interpretation = ds.show_target_interpretation_from_UID(input_UID='739848')
	ds.build_simultaneous_interpretation_man_name_chart(pure_uid_man_list=pure_uid_man_list)
	date_within = ds.select_date_within(start_date='2019-09-01', end_date='2019-09-30')
	all_danmaku = ds.show_all_danmaku_from_UID(input_UID='268065764')
	single_uid_interpretation_timeline = ds.Single_UID_interpretation_timeline(input_UID='37718180')
	single_uid_all_danmaku_timeline = ds.Single_UID_all_danmaku_timeline(input_UID='37718180')
	simultaneous_interpretation_man_list = ds.select_simultaneous_interpretation_man(man_threshold=150, show_name=False)
	pure_uid_man_list = [row[0] for row in simultaneous_interpretation_man_list]
	single_live_roow_interpretation_timeline = ds.Single_live_room_interpretation_timeline(input_room_id='11588230', pure_uid_man_list=pure_uid_man_list)
	ds.build_fast_name_chart()
	