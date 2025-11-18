import pandas as pd
import numpy as np

print(pd.__version__)
print(np.__version__)

#To do: フォルダのパスを変数化して、複数データの読み込みに対応させる
initial_file_1 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-08-32-662\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv'

data_file_1 = 'Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-09-58-052\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv'

#df = pd.read_csv('Witmotion(V2025.11.12.3)\\Record\\2025-11-12\\16-09-58-052\\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv').values.tolist()
# if1 = pd.read_csv(initial_file_1).values.tolist()
# df1 = pd.read_csv(data_file_1).values.tolist()
if1 = pd.read_csv(initial_file_1)
df1 = pd.read_csv(data_file_1)

#データのカラム説明
# 0 Time
# 1 Device name
# 2 Chip Time()
# 3 Acceleration X(g)	
# 4 Acceleration Y(g)	
# 5 Acceleration Z(g)	
# 6 Angular velocity X(°/s)	
# 7 Angular velocity Y(°/s)	
# 8 Angular velocity Z(°/s)	
# 9 ShiftX(mm)	
# 10 ShiftY(mm)	
# 11 ShiftZ(mm)	
# 12 SpeedX(mm/s)	
# 13 SpeedY(mm/s)	
# 14 SpeedZ(mm/s)	
# 15 Angle X(°)	
# 16 Angle Y(°)	
# 17 Angle Z(°)	
# 18 Magnetic field X(ʯt)	
# 19 Magnetic field Y(ʯt)	
# 20 Magnetic field Z(ʯt)	
# 21 Temperature(℃)	
# 22 Quaternions 0()	
# 23 Quaternions 1()	
# 24 Quaternions 2()	
# 25 Quaternions 3()	
# 26 Raw power()	
# 27 Power Percent(%)()

#不要な行の削除 いらないかも
# delete_columns = [9,10,11,12,13,14]
# np.delete(df1, [9,10,11,12,13,14], axis=1)

#初期データの平均値計算

# df1_means = np.mean(if1, axis=1)
# print("Initial data means:")

if1_nums = if1.select_dtypes(include='number')
if1_means = if1_nums.mean(axis=0)
print(if1_means)

#初期姿勢からの相対化　装着前に机においてキャリブレーションする
#各センサの絶対方位のズレを補正

df1_nums = df1.select_dtypes(include='number')

#

#

#print(df)