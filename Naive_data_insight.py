# Created by pren1 at 12/21/2019
# Using matplotlib, show the data chart and output .csv file
from Dataset_searcher import Dataset_searcher
import csv
import pandas as pd
import pdb

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

if __name__ == '__main__':
	NDI = Naive_data_insight()
	NDI.output_interpretation_man_rank_csv(csv_name="interpretation_man_rank.csv")