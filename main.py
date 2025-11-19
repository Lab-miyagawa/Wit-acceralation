import read_data as rd
import cal_angle as ca
import cal_matrix as cm
import pandas as pd
import numpy as np
import csv

#ファイルパスの指定
#To do: フォルダのパスを変数化して、複数データの読み込みに対応させる
initial_file_1 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-08-32-662\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv'
initial_file_2 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-08-32-662\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_1.csv'
data_file_1 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-09-58-052\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv'
data_file_2 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-09-58-052\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_1.csv'

# データ読み込み
ReadData = rd.read_csv_and_format(initial_file_1, initial_file_2, data_file_1, data_file_2)

if1_means = ReadData[0]
if2_means = ReadData[1]
df1_nums = ReadData[2]
df2_nums = ReadData[3]

# 手首角度の計算
WristAngle = ca.calculate_wrist_angle(df1_nums.values.tolist(), df2_nums.values.tolist(), if1_means[15:18].values.tolist(), if2_means[15:18].values.tolist())

# 結果出力
f = open('output\\out.csv', 'w')
data = WristAngle
writer = csv.writer(f)
writer.writerow(data)
f.close()
