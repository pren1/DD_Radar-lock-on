# Created by pren1 at 12/21/2019
# Using matplotlib, show the data chart and output .csv file
from Dataset_searcher import Dataset_searcher
import csv
import pandas as pd
import pdb
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from constants import DATABASE_NAME, output_interpretation_man_rank_csv

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

class Naive_data_insight(object):
	def __init__(self):
		self.man_threshold = 150
		self.ds = Dataset_searcher(DATABASE_NAME)
		self.ds.connect_dataset()
		self.simultaneous_interpretation_man_list = self.ds.select_simultaneous_interpretation_man(man_threshold=self.man_threshold,
		                                                                                 show_name=False)
		self.pure_uid_man_list = [row[0] for row in self.simultaneous_interpretation_man_list]

	def output_interpretation_man_rank_csv(self, csv_name):
		self.simultaneous_interpretation_man_list = self.ds.get_prefer_room(self.simultaneous_interpretation_man_list)
		interpretation_man_rank_list = [[self.ds.prefetched_man_id(row[0]), row[1], round(int(row[2])/int(row[1]),2), row[2], row[3]] for row in self.simultaneous_interpretation_man_list]
		df = self.time_line_to_dataframe(interpretation_man_rank_list, columns=['昵称', '同传弹幕数' , '平均每条同传字符数' , '总同传字符数', '同传数最多直播间(比例)'])
		df.to_csv(csv_name, sep='\t', encoding='utf-8')

	def visualize_single_room_timeline(self, room_id):
		def visualize_dataframe(new_df, title):
			plt.rcParams['font.sans-serif'] = ['SimHei']
			new_df.loc[:, 'danmaku_count'] = new_df['danmaku_count'].astype(float)
			new_df.YMD_time = pd.to_datetime(new_df['YMD_time'])
			g = sns.FacetGrid(new_df, hue="user_id", height=8, aspect=2)
			g.map(plt.scatter, "YMD_time", "danmaku_count")
			g.fig.legend(loc='best', shadow=True)
			g.map(plt.plot, "YMD_time", "danmaku_count")
			plt.title(title)
			plt.xlabel('时间轴')
			plt.ylabel('弹幕数')
			plt.gcf().autofmt_xdate()
			plt.subplots_adjust(left=0.08, bottom=0.10, right=0.98, top=0.93, wspace=0.05, hspace=0.05)
			plt.show()

		Single_room_id_timeline = self.time_line_to_dataframe(
			self.ds.Single_live_room_interpretation_timeline(input_room_id=room_id, pure_uid_man_list=self.pure_uid_man_list),
			columns=['YMD_time', 'room_id', 'user_id', 'danmaku_count'])
		room_id_nick_name = self.ds.prefetched_room_id(int(room_id))
		visualize_dataframe(Single_room_id_timeline, title=str(room_id_nick_name)+": 直播间同传统计")

	def visualize_single_uid_timeline(self, input_UID):
		def visualize_dataframe(new_df, title):
			plt.rcParams['font.sans-serif']=['SimHei']
			new_df.loc[:, 'danmaku_count'] = new_df['danmaku_count'].astype(float)
			new_df.YMD_time = pd.to_datetime(new_df['YMD_time'])
			g = sns.FacetGrid(new_df, hue="room_id", height=8, aspect=2)
			g.map(plt.scatter, "YMD_time", "danmaku_count")
			g.fig.legend(loc='best', shadow=True)
			g.map(plt.plot, "YMD_time", "danmaku_count")
			plt.title(title)
			plt.xlabel('时间轴')
			plt.ylabel('弹幕数')
			plt.gcf().autofmt_xdate()
			plt.subplots_adjust(left=0.08, bottom=0.10, right=0.98, top=0.93, wspace=0.05, hspace=0.05)
			plt.show()

		Single_UID_interpretation_df = self.time_line_to_dataframe(
			self.ds.Single_UID_interpretation_timeline(input_UID=input_UID),
			columns=['YMD_time', 'room_id', 'user_id', 'danmaku_count'])

		"""Single_UID_all_danmaku_df = self.time_line_to_dataframe(
			self.ds.Single_UID_all_danmaku_timeline(input_UID=input_UID),
			columns=['YMD_time', 'room_id', 'user_id', 'danmaku_count'])"""

		nick_name = self.ds.prefetched_man_id(int(input_UID))

		visualize_dataframe(Single_UID_interpretation_df, title=str(nick_name)+": 同传弹幕统计")
		#visualize_dataframe(Single_UID_all_danmaku_df, title=str(nick_name)+": 全部弹幕统计") #由于数据库目前只录入同传弹幕，暂时关闭全部弹幕查询

	def time_line_to_dataframe(self, timeline, columns):
		df = pd.DataFrame(columns=columns)
		for index, single in enumerate(timeline):
			df.loc[str(index)] = single
		return df

if __name__ == '__main__':
	NDI = Naive_data_insight()
	NDI.output_interpretation_man_rank_csv(csv_name=output_interpretation_man_rank_csv)
	#NDI.visualize_single_room_timeline(room_id='11588230')
	#NDI.visualize_single_uid_timeline(input_UID='739848')
	#NDI.visualize_single_uid_timeline(input_UID='27212086')
	#NDI.visualize_single_uid_timeline(input_UID='9572567')
	
	#NDI.visualize_single_room_timeline(room_id='12235923')
	#NDI.visualize_single_uid_timeline(input_UID='2907459')
