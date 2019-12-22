# Created by pren1 at 12/21/2019
# Using matplotlib, show the data chart and output .csv file
from Dataset_searcher import Dataset_searcher
import csv
import pandas as pd
import pdb
import matplotlib.pyplot as plt
import seaborn as sns

class Naive_data_insight(object):
	def __init__(self):
		self.man_threshold = 100
		self.ds = Dataset_searcher("test.db")
		self.ds.connect_dataset()
		self.simultaneous_interpretation_man_list = self.ds.select_simultaneous_interpretation_man(man_threshold=self.man_threshold,
		                                                                                 show_name=False)
		self.pure_uid_man_list = [row[0] for row in self.simultaneous_interpretation_man_list]

	def output_interpretation_man_rank_csv(self, csv_name):
		interpretation_man_rank_list = self.ds.select_simultaneous_interpretation_man(man_threshold=self.man_threshold,
		                                                                                 show_name=True)
		df = pd.DataFrame(columns=['昵称', '同传弹幕数'])
		for index, single in enumerate(interpretation_man_rank_list):
			df.loc[f'{index}'] = single
		df.to_csv(csv_name, sep='\t', encoding='utf-8')

	def visualize_single_uid_timeline(self, input_UID):
		single_uid_interpretation_timeline = self.time_line_to_dataframe(
			self.ds.Single_UID_interpretation_timeline(input_UID=input_UID), columns=['YMD_time', 'room_id', 'user_id', 'danmaku_count'])
		# single_uid_interpretation_timeline[['YMD_time', 'danmaku_count']].set_index('YMD_time').plot()
		# single_uid_all_danmaku_timeline = self.ds.Single_UID_all_danmaku_timeline(input_UID=input_UID)
		# ax = sns.scatterplot(x="YMD_time", y="danmaku_count", hue="room_id", data = single_uid_interpretation_timeline)

		# new_df = single_uid_interpretation_timeline.set_index('YMD_time')
		new_df = single_uid_interpretation_timeline
		new_df.loc[:, 'danmaku_count'] = new_df['danmaku_count'].astype(float)
		# new_df.room_id = new_df.room_id.astype('category')
		new_df.YMD_time = pd.to_datetime(new_df['YMD_time'])

		g = sns.FacetGrid(new_df, hue="room_id", height=8)
		g.map(plt.scatter, "YMD_time", "danmaku_count")
		g.add_legend()
		# g.fig.legend(loc='best', shadow=True, fontsize='xx-small')
		g.map(plt.plot, "YMD_time", "danmaku_count")
		# ax = sns.scatterplot(x=new_df.index, y=new_df.danmaku_count, hue=new_df.room_id, palette=sns.color_palette("Set1", len(set(new_df.room_id))), data=new_df)
		plt.gcf().autofmt_xdate()
		# legend = plt.legend(loc='best', shadow=True, fontsize='xx-small')
		# legend.get_frame().set_facecolor('w')
		plt.show()
		pdb.set_trace()


	def time_line_to_dataframe(self, timeline, columns):
		df = pd.DataFrame(columns=columns)
		for index, single in enumerate(timeline):
			df.loc[f'{index}'] = single
		return df

if __name__ == '__main__':
	NDI = Naive_data_insight()
	# NDI.output_interpretation_man_rank_csv(csv_name="interpretation_man_rank.csv")
	NDI.visualize_single_uid_timeline(input_UID='37718180')