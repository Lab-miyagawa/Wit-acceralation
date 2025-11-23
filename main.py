import read_data as rd
import cal_angle as ca
import cal_matrix as cm
import pandas as pd
import numpy as np
import csv
import os
from datetime import datetime

#ファイルパスの指定
#To do: フォルダのパスを変数化して、複数データの読み込みに対応させる
# d6~： 手首センサ
# d7~： 手の甲センサ
initial_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-05-757\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
initial_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-05-757\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
data_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-18-386\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
data_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-18-386\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
# データ読み込み
ReadData = rd.read_csv_and_format(initial_file_W, initial_file_H, data_file_W, data_file_H)

if1_means = ReadData[0]
if2_means = ReadData[1]
df1_nums = ReadData[2]
df2_nums = ReadData[3]

# 手首角度の計算
WristAngle = ca.calculate_wrist_angle(df1_nums.values.tolist(), df2_nums.values.tolist(), if1_means[15:18].values.tolist(), if2_means[15:18].values.tolist())

# # 結果出力
# f = open('output\\out.csv', 'w')
# data = WristAngle
# writer = csv.writer(f)
# writer.writerow(data)
# f.close()

# deg に変換（n×3）
WristAngle_deg = np.degrees(WristAngle)

# タイムスタンプ（ここでは df1_nums の 0 列目を Time として使う）:contentReference[oaicite:1]{index=1}
time_col = df1_nums.iloc[:, 0].to_numpy()

# 長さを安全にそろえる（calculate_wrist_angle 内で min(len(...)) しているため）:contentReference[oaicite:2]{index=2}
n = WristAngle.shape[0]
time_col = time_col[:n]
# ---- 元 CSV フォルダから日付 & 時刻抽出 ----
session_time_dir = os.path.dirname(initial_file_W)
session_date_dir = os.path.dirname(session_time_dir)

session_time = os.path.basename(session_time_dir)
session_date = os.path.basename(session_date_dir)

# ---- 出力フォルダ（フォルダとして作成） ----
outdir = "output"
os.makedirs(outdir, exist_ok=True)

# 出力ファイル名
outfile = os.path.join(outdir, f"out_{session_date}_{session_time}.csv")

# ---- 書き込み ----
with open(outfile, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Time",
        "Roll(rad)", "Pitch(rad)", "Yaw(rad)",
        "Roll(deg)", "Pitch(deg)", "Yaw(deg)"
    ])

    for i in range(n):
        roll_r, pitch_r, yaw_r = WristAngle[i]
        roll_d, pitch_d, yaw_d = WristAngle_deg[i]

        writer.writerow([
            time_col[i],
            roll_r, pitch_r, yaw_r,
            roll_d, pitch_d, yaw_d,
        ])

print("Saved:", outfile)