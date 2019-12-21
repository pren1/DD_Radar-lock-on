# Created by pren1 at 12/20/2019
import pdb
from File_scan import File_scan
from txt_processor import txt_processor
import sqlite3
from tqdm import tqdm

class Dataset_builder(object):
	def __init__(self, danmaku_folder, data_set_name):
		file_scan = File_scan(danmaku_folder)
		self.all_file_paths = file_scan.path_gen()
		self.data_set_name = data_set_name

	def initialize_dataset(self):
		conn = sqlite3.connect(self.data_set_name)
		c = conn.cursor()
		c.execute('''CREATE TABLE DD_DANMAKU_TABLE
		       (ID INT PRIMARY  KEY NOT NULL,
		       room_id          TEXT NOT NULL,
		       YMD_time         TEXT NOT NULL,
		       single_pass_time TEXT NOT NULL,
		       UID              TEXT NOT NULL,
		       message          TEXT NOT NULL
		       );''')
		print("Table created successfully")
		conn.commit()
		conn.close()

	def insert_all_data(self):
		conn = sqlite3.connect(self.data_set_name)
		c = conn.cursor()
		print ("Opened database successfully")
		global_table_index = 0
		for single_file_path in tqdm(self.all_file_paths):
			processor = txt_processor(single_file_path)
			candidate_danmakus = processor.read_target_txt()
			room_id, YMD_time = self.return_room_and_time(single_file_path=single_file_path)
			if len(candidate_danmakus) > 0:
				for single_danmaku in candidate_danmakus:
					assert len(single_danmaku) == 3, "Error, array length incorrect"
					single_pass_time = single_danmaku[0]
					UID = single_danmaku[1]
					message = single_danmaku[2]
					'insert to the dataset'
					params = (global_table_index, room_id, YMD_time, single_pass_time, UID, message)
					c.execute("INSERT INTO DD_DANMAKU_TABLE VALUES (?, ?, ?, ?, ?, ?)", params)
					global_table_index += 1
					# cursor = c.execute("SELECT ID, room_id, YMD_time, single_pass_time, UID, message  from DD_DANMAKU_TABLE")
		conn.commit()
		print("Records created successfully")
		conn.close()

	def return_room_and_time(self, single_file_path):
		room_id = single_file_path.split('/')[1]
		YMD_time = self.add_leading_zero_to_date(single_file_path.split('/')[2][:-4])
		return room_id, YMD_time

	def add_leading_zero_to_date(self, YMD_time):
		date_list = YMD_time.split('-')
		assert len(date_list) == 3, "YMD time format error"
		date_list[1] = '{:02}'.format(int(date_list[1]))
		date_list[2] = '{:02}'.format(int(date_list[2]))
		return '-'.join(date_list)

if __name__ == '__main__':
	input_path = "bilibili-vtuber-danmaku/"
	dataset_builder = Dataset_builder(input_path, "test.db")
	dataset_builder.initialize_dataset()
	dataset_builder.insert_all_data()
