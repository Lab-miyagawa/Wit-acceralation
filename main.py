import read_data as rd
import cal_angle as ca
import cal_matrix as cm
import pandas as pd
import numpy as np
import csv
import os
from datetime import datetime

# ファイルパスの指定
# d6~： 手首センサ (Wrist)
# d7~： 手の甲センサ (Hand)
# initial_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\01-05-29-970\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
# initial_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\01-05-29-970\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
# data_file_W    = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\01-05-42-434\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
# data_file_H    = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\01-05-42-434\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
initial_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\03-43-38-397\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
initial_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\03-43-38-397\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
data_file_W    = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\03-43-59-202\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
data_file_H    = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-24\03-43-59-202\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"


# データ読み込み
# if1,if2： 初期データの平均値（数値列のみ）
# df1_nums,df2_nums： 本番データ（数値列のみ）
ReadData = rd.read_csv_and_format(initial_file_W, initial_file_H, data_file_W, data_file_H)
if1_means = ReadData[0]   # 初期手首 W の平均値（数値列）
if2_means = ReadData[1]   # 初期手の甲 H の平均値（数値列）
df1_nums  = ReadData[2]   # 手首 W の本番データ（数値列のみ）
df2_nums  = ReadData[3]   # 手の甲 H の本番データ（数値列のみ）

# 手首角度（相対）の計算（rad）
CalAngleData = ca.calculate_wrist_angle(
    df1_nums.values.tolist(),
    df2_nums.values.tolist(),
    if1_means[6:9].values.tolist(),  # Angle X,Y,Z (deg) を想定
    if2_means[6:9].values.tolist()
)
print(if1_means[6:9].values.tolist())
print(if2_means[6:9].values.tolist())

WristAngle = CalAngleData[0]  # 相対手首角度 (rad)
WristDebug = CalAngleData[1]  # デバッグ用手首角度 (rad)
HandDebug  = CalAngleData[2]  # デバッグ用手の甲角度 (rad)

# deg に変換（n×3）
WristAngle_deg = np.degrees(WristAngle)
WristDebug_deg = np.degrees(WristDebug)
HandDebug_deg  = np.degrees(HandDebug)

# --- 2. time は data_file_W のものを使用 ---
# df1_nums は data_file_W 由来なので、その 0 列目を Time として使う
time_col = df1_nums.iloc[:, 0].to_numpy()

# 長さを安全にそろえる（calculate_wrist_angle 内で min(len(...)) しているため）
n = WristAngle.shape[0]
time_col = time_col[:n]

# --- 1. data_file_W / H の AngleX,Y,Z を出力に追加するために取り出す ---
# コメントより、Angle X/Y/Z が 15,16,17 列目（数値列側でも同じ位置を想定）:contentReference[oaicite:2]{index=2}
angle_W_deg = df1_nums.iloc[:n,6:9].to_numpy()  # (n,3) 手首センサの実測角度
angle_H_deg = df2_nums.iloc[:n, 6:9].to_numpy()  # (n,3) 手の甲センサの実測角度

# ---- 3. 出力ファイル名は main.py 実行日時ベース ----
outdir = "output"
os.makedirs(outdir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
outfile = os.path.join(outdir, f"out_{timestamp}.csv")

# ---- CSV 書き込み ----
with open(outfile, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # ヘッダ行
    writer.writerow([
    "No","Time",
    "Roll(rad)", "Pitch(rad)", "Yaw(rad)",          # 相対手首角度 (rad)
    "Roll(deg)", "Pitch(deg)", "Yaw(deg)",          # 相対手首角度 (deg)
    "W_AngleX(deg)", "W_AngleY(deg)", "W_AngleZ(deg)",  # data_file_W の Angle
    "H_AngleX(deg)", "H_AngleY(deg)", "H_AngleZ(deg)",  # data_file_H の Angle
    # ↓ ここから debug 用
    # "Debug_Roll(rad)", "W_Debug_Pitch(rad)", "W_Debug_Yaw(rad)",
    "W_Debug_Roll(deg)", "W_Debug_Pitch(deg)", "W_Debug_Yaw(deg)",
    # _Debug_Roll(rad)", "H_Debug_Pitch(rad)", "H_Debug_Yaw(rad)",
    "H_Debug_Roll(deg)", "H_Debug_Pitch(deg)", "H_Debug_Yaw(deg)",
    ])


    # データ行
    for i in range(n):
        # 相対手首角度
        roll_r,  pitch_r,  yaw_r  = WristAngle[i]
        roll_d,  pitch_d,  yaw_d  = WristAngle_deg[i]

        # 元データの angle（センサそのものの姿勢）
        wx, wy, wz = angle_W_deg[i]
        hx, hy, hz = angle_H_deg[i]

        # デバッグ用：初期姿勢からの wrist / hand 角度
        # wd_roll_r, wd_pitch_r, wd_yaw_r = WristDebug[i]
        # hd_roll_r, hd_pitch_r, hd_yaw_r = HandDebug[i]
        wd_roll_d, wd_pitch_d, wd_yaw_d = WristDebug_deg[i]
        hd_roll_d, hd_pitch_d, hd_yaw_d = HandDebug_deg[i]

        writer.writerow([
            i,time_col[i],
            # 相対手首角度
            roll_r,  pitch_r,  yaw_r,
            roll_d,  pitch_d,  yaw_d,
            # 元センサ角度
            wx, wy, wz,
            hx, hy, hz,
            # debug: 初期からの wrist
            # wd_roll_r, wd_pitch_r, wd_yaw_r,
            wd_roll_d, wd_pitch_d, wd_yaw_d,
            # debug: 初期からの hand
            # hd_roll_r, hd_pitch_r, hd_yaw_r,
            hd_roll_d, hd_pitch_d, hd_yaw_d,
        ])


print("Saved:", outfile)




# import read_data as rd
# import cal_angle as ca
# import cal_matrix as cm
# import pandas as pd
# import numpy as np
# import csv
# import os
# from datetime import datetime

# #ファイルパスの指定
# #To do: フォルダのパスを変数化して、複数データの読み込みに対応させる
# # d6~： 手首センサ
# # d7~： 手の甲センサ
# initial_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-05-757\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
# initial_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-05-757\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
# data_file_W = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-18-386\_WT901BLE67(d6-a8-b9-ee-a0-b7)_0.csv"
# data_file_H = r"C:\Users\takmu\Box\2025\User\Miyagawa\開発\code\Wit-acceralation\Witmotion(V2025.11.12.3)\Record\2025-11-23\18-37-18-386\_WT901BLE67(d7-ab-97-c1-e4-84)_0.csv"
# # データ読み込み
# ReadData = rd.read_csv_and_format(initial_file_W, initial_file_H, data_file_W, data_file_H)

# if1_means = ReadData[0]
# if2_means = ReadData[1]
# df1_nums = ReadData[2]
# df2_nums = ReadData[3]

# # 手首角度の計算
# WristAngle = ca.calculate_wrist_angle(df1_nums.values.tolist(), df2_nums.values.tolist(), if1_means[15:18].values.tolist(), if2_means[15:18].values.tolist())

# # # 結果出力
# # f = open('output\\out.csv', 'w')
# # data = WristAngle
# # writer = csv.writer(f)
# # writer.writerow(data)
# # f.close()

# # deg に変換（n×3）
# WristAngle_deg = np.degrees(WristAngle)

# # タイムスタンプ（ここでは df1_nums の 0 列目を Time として使う）:contentReference[oaicite:1]{index=1}
# time_col = df1_nums.iloc[:, 0].to_numpy()

# # 長さを安全にそろえる（calculate_wrist_angle 内で min(len(...)) しているため）:contentReference[oaicite:2]{index=2}
# n = WristAngle.shape[0]
# time_col = time_col[:n]
# # ---- 元 CSV フォルダから日付 & 時刻抽出 ----
# session_time_dir = os.path.dirname(initial_file_W)
# session_date_dir = os.path.dirname(session_time_dir)

# session_time = os.path.basename(session_time_dir)
# session_date = os.path.basename(session_date_dir)

# # ---- 出力フォルダ（フォルダとして作成） ----
# outdir = "outputs"
# os.makedirs(outdir, exist_ok=True)

# # 出力ファイル名
# outfile = os.path.join(outdir, f"out_{session_date}_{session_time}.csv")

# # ---- 書き込み ----
# with open(outfile, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)

#     writer.writerow([
#         "Time",
#         "Roll(rad)", "Pitch(rad)", "Yaw(rad)",
#         "Roll(deg)", "Pitch(deg)", "Yaw(deg)"
#     ])

#     for i in range(n):
#         roll_r, pitch_r, yaw_r = WristAngle[i]
#         roll_d, pitch_d, yaw_d = WristAngle_deg[i]

#         writer.writerow([
#             i,time_col[i],
#             roll_r, pitch_r, yaw_r,
#             roll_d, pitch_d, yaw_d,
#         ])

# print("Saved:", outfile)