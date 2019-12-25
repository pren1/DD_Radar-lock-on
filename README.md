# 同 传 摸 鱼/DD 检 测 机

<p>
    <img src="image/dd_center.png"/>
</p>

### 🤝 Contributor: 

[pren1](https://github.com/pren1), [scPointer](https://github.com/scPointer)

### 📃 Introduction

本脚本通过对过去七个月所记录的vtuber相关bilibili直播弹幕处理，实现以下功能：

* 获取目标在vtuber相关直播间发送的弹幕
* 获取在vtuber相关直播间进行同传的名单
* 获取目标在vtuber相关直播间发送的同传弹幕数量变化
* 获取直播间同传man弹幕数变化情况

### 📦 Update by [scPointer](https://github.com/scPointer)
#### version 1.1
debug :
1. 修改有关文件路径 '\'为 os.sep 
2. 原文件中用最后一个半角冒号分隔UID和弹幕，但弹幕中可能出现冒号，如 "_(:зゝ∠)_"，导致UID未正确划分 
3. 一些弹幕文件信息出错导致 numpy 的 asarray 函数请求过量空间。用 try-except 特判解决 

功能改动：
4. 修改同传判定规则，并附在建库代码中。这意味着同传判定在建库时进行而不是在查询时。
5. 原弹幕数据bilibili-vtuber-danmaku中最初记录数据没有UID或时间戳，用txt_processor.preprocess_readin_list()中一长串特判解决了这个问题。没有UID的同传部分单独划分到UID=0。
6. 增加输出信息项：同传平均字符数，同传偏爱直播间等。所有附加信息只使用一次查询实现。

时间效率改进：
7. 修改数据库输入信息，现在只录入同传弹幕的用户/直播间/日期/时间/长度，且不记录弹幕内容。数据库大小3.11GB -> 38MB，所有信息都可以几秒出解。后续可以增加记录弹幕内容，改动不大。
8. 修改数据库内记录项的格式。之前所有格式均为文本，增加了搜索数据时比较项不必要的时间。

结构改动：
9. 因为更新了判定规则，检测到的同传man变多了，所以顺便更新了man_id_nick_name_chart.csv
10. 修改 Data_seatcher.py 中sqlite查询语句的结构。
11. 使用constants统一规范一些变量：数据库名，同传man的id/昵称对应文件名，直播间的id/昵称对应文件名，输出同传man的rank的文件名

适配：
12. 暂时把所有形如 f'abc{d}'的改成 'abc'+str(d) (done)
13. 调用b站api找直播间和同传man名字时可能会卡，加个delay

### 🌲 Request Packages

[![Generic badge](https://img.shields.io/badge/python3-orange.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/pandas-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/numpy-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/sqlite-blueviolet.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/tqdm-lightgrey.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/matplotlib-ff69b4.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/seaborn-success.svg)](https://shields.io/)

### ⚡️ Quick start

首先，下载本repo:
```
git clone https://github.com/pren1/DD_Radar-lock-on.git
```

然后，下载 [bilibili-vtuber-danmaku](https://github.com/dd-center/bilibili-vtuber-danmaku.git) 弹幕数据库到**本repo**文件夹下:
```
git clone https://github.com/dd-center/bilibili-vtuber-danmaku.git
```



运行:
```python3
python3 Dataset_builder.py
```

然后，运行:
```python3
python3 Naive_data_insight.py
```

### 🎉 Result examples

同传man名单（含排名）将会被保存到 interpretation_man_rank.csv:


| Rank  | 昵称           | 同传弹幕数 | 平均每条同传字符数 | 偏爱直播间(占该同传man条数的比例)
|-|-|-|-|-|
| 0   | 殿子desu            | 60303 | 8.94 | 癒月巧可Official(57%)
| 1   | 夜行游鬼          | 40586 | 8.46|夏色祭Official(74%)
| 2   | 快递员小黑           | 31689 | 10.55|大神澪Official(43%)
| 3   | 精神王             | 21830 | 8.9|夜空梅露Official(62%)
| 4   | HTdatou             | 20656 | 10.21|百鬼绫目Official(13%)
| 5   | 叫霓裳         | 18126 | 8.42|湊-阿库娅Official(52%)
| 6   | Searrle      | 15506 | 8.46|Milky_Vtuber(100%)
| 7   | 涼風青葉頑張るぞい    | 13031 | 8.25|白上吹雪Official(85%)
| 8   | 天火official         | 12383  | 8.71|夏色祭Official(83%)
| 9   | call_me_Gump             | 10277  | 8.05|赤井心Official(79%)
| 10  | 徽铯huise       | 10250  | 9.04|夏色祭Official(56%)
| 11  | 小V不是弱受          | 9648  | 10.25|猫又小粥Official(75%)
| 12  | 長門凖       | 9049  | 11.28|白百合リリィOfficial(98%)
| 13  | namelostman     | 6094 | 9.73|贝尔蒙德Official(89%)
| 14  | 小天man           | 5572  | 9.45|百鬼绫目Official(78%)
| 15  | LEDお兄ちゃん        | 5142  | 11.72|Kanna_康娜Official(90%)
| 16  | scPointer            | 5043  | 12.55|神楽Mea_Official(99%)
| 17  | 樱晴末雨          | 4326  | 7.94|湊-阿库娅Official(43%)
| 18  | 校了个寂寞         | 4119  | 9.27|夏色祭Official(82%)
| 19  | 有只小强爬过            | 3978  | 11.14|花园Serena(68%)
| 20  | 夜语晚樱     | 3851  | 8.87|花园Serena(78%)
| 21  | MEISSS          | 3422  | 10.61|百鬼绫目Official(51%)
| 22  | Diana-ディアナ              | 3371  | 9.77|高槻律official(93%)

接下来是相关数据可视化:

#### 直播间同传弹幕数量变化
<p>
    <img src="image/fubuki.png"/>
</p>

<p>
    <img src="image/mazili.png"/>
</p>

#### 同传man同传弹幕数量变化

<p>
    <img src="image/dianzi.png"/>
</p>

<p>
    <img src="image/xiaov.png"/>
</p>

#### 弹幕数量变化（包含同传与非同传）

<p>
    <img src="image/feixue.png"/>
</p>

### ☁️ Utilization
更详细的注释在相应函数内

```python3
from Naive_data_insight import Naive_data_insight
NDI = Naive_data_insight()

# '导出同传man名单'
NDI.output_interpretation_man_rank_csv(csv_name="interpretation_man_rank.csv")

# ‘显示直播间同传弹幕数量变化’
NDI.visualize_single_room_timeline(room_id='13946381')

# ‘显示同传man同传弹幕数量变化 与 普通弹幕数量变化’
NDI.visualize_single_uid_timeline(input_UID='27212086')
```

```python3
from Dataset_searcher import Dataset_searcher
ds = Dataset_searcher("test.db")
ds.connect_dataset()

# '返回目标同传man发送的所有同传弹幕'
all_interpretation = ds.show_target_interpretation_from_UID(input_UID='739848')

# ‘返回目标发送的所有弹幕’
all_danmaku = ds.show_all_danmaku_from_UID(input_UID='739848')

# ‘返回目标同传弹幕信息随时间的变化’
single_uid_interpretation_timeline = ds.Single_UID_interpretation_timeline(input_UID='739848')

# ‘返回目标弹幕数量随时间的变化’
single_uid_all_danmaku_timeline = ds.Single_UID_all_danmaku_timeline(input_UID='739848')

# ‘设定最少发送的同传弹幕数，并以此筛选同传man名单’
simultaneous_interpretation_man_list = ds.select_simultaneous_interpretation_man(man_threshold=100, show_name=False)

# ‘获取某一时间段内的弹幕信息’
date_within = ds.select_date_within(start_date='2019-09-01', end_date='2019-09-30')

# ‘返回同传man的UID列表’
pure_uid_man_list = [row[0] for row in simultaneous_interpretation_man_list]

# ’返回目标直播间弹幕信息随时间的变化‘
single_live_roow_interpretation_timeline = ds.Single_live_room_interpretation_timeline(input_room_id='11588230', pure_uid_man_list=pure_uid_man_list)

# ‘生成直播间 ID与vtuber昵称的对应列表’
ds.build_fast_name_chart()

# ‘生成同传man UID与昵称的对应列表’
ds.build_simultaneous_interpretation_man_name_chart(pure_uid_man_list=pure_uid_man_list)
```
### ☀️ Special thanks
* 感谢所有【同传man】对bilibili vtuber直播所付出的努力
* 感谢[simon3000](https://github.com/simon300000)在开发过程中关于id与昵称转换的帮助
* 感谢[Curtis Xiao](https://github.com/wudifeixue)对开发提出的建议
