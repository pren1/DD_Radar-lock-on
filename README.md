# DD_Radar-lock-on

<p>
    <img src="image/dd_center.png"/>
</p>

### 📃 Introduction

同 传 摸 鱼 检 测 机

本脚本通过对过去七个月所记录的vtuber相关bilibili直播弹幕处理，实现以下功能：

* 获取目标在vtuber相关直播间发送的弹幕
* 获取在vtuber相关直播间进行同传的名单
* 获取目标在vtuber相关直播间发送的弹幕数量变化
* 获取目标在vtuber相关直播间发送的同传弹幕数量变化
* 获取直播间同传man弹幕数变化情况

### 🌲 Request Packages

[![Generic badge](https://img.shields.io/badge/python3-orange.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/pandas-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/numpy-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/sqlite-blueviolet.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/tqdm-lightgrey.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/matplotlib-ff69b4.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/seaborn-success.svg)](https://shields.io/)

### ⚡️ Quick start

First, download the [bilibili-vtuber-danmaku](https://github.com/dd-center/bilibili-vtuber-danmaku.git) dataset.

Then, run:
```
Dataset_builder.py
```

After that, run:
```
Naive_data_insight.py
```

Then the simultaneous interpretation man list will be saved to interpretation_man_rank.csv:

|     |                 |       | 
|-----|-----------------|-------| 
| 昵称  | 同传弹幕数           |       | 
| 0   | 夜行游鬼            | 38644 | 
| 1   | 殿子desu          | 35289 | 
| 2   | 快递员小黑           | 23237 | 
| 3   | 精神王             | 18245 | 
| 4   | 叫霓裳             | 17710 | 
| 5   | HTdatou         | 12200 | 
| 6   | 天火official      | 11440 | 
| 7   | call_me_Gump    | 10078 | 
| 8   | 徽铯huise         | 9462  | 
| 9   | 長門凖             | 8898  | 
| 10  | 涼風青葉頑張るぞい       | 8143  | 
| 11  | 小V不是弱受          | 6500  | 
| 12  | scPointer       | 5012  | 
| 13  | namelostman     | 4594  | 
| 14  | 小天man           | 4590  | 
| 15  | LEDお兄ちゃん        | 4426  | 
| 16  | 樱晴末雨            | 4297  | 
| 17  | 校了个寂寞           | 4112  | 
| 18  | 有只小强爬过          | 3964  | 
| 19  | 夜语晚樱            | 3823  | 
| 20  | Diana-ディアナ      | 3356  | 
| 21  | 纯白Cco           | 3236  | 
| 22  | 斯辞              | 3226  | 

Moreover, the data will be visualized as follows:

<p>
    <img src="image/dd_center.png"/>
</p>







