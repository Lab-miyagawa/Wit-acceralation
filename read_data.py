import pandas as pd
import numpy as np

print(pd.__version__)
print(np.__version__)

def to_python_path(win_path: str) -> str:
    """
    Windows のパスを Python のエスケープ済みパスへ変換する。
    例: "a\b\c.txt" → "a\\b\\c.txt"
    """
    return win_path.replace("\\", "\\\\")


def read_csv_and_format(initial_file_1, initial_file_2, data_file_1, data_file_2):
    #csvファイル読み込み
    #windowsパスをpythonパスに変換
    if1 = to_python_path(pd.read_csv(initial_file_1))
    if2 = to_python_path(pd.read_csv(initial_file_2))
    df1 = to_python_path(pd.read_csv(data_file_1))
    df2 = to_python_path(pd.read_csv(data_file_2))

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

    #不要な行の削除 使わない
    # delete_columns = [9,10,11,12,13,14]
    # np.delete(df1, [9,10,11,12,13,14], axis=1)

    #初期データの平均値計算　数値部分のみ抜き出す
    if1_nums = if1.select_dtypes(include='number')
    if1_means = if1_nums.mean(axis=0)
    print("--- Initial File 1 Means ---")
    print(if1_means)
    if2_nums = if2.select_dtypes(include='number')
    if2_means = if2_nums.mean(axis=0)
    print("--- Initial File 2 Means ---")
    print(if2_means)

    df1_nums = df1.select_dtypes(include='number')
    df2_nums = df2.select_dtypes(include='number')

    #データのカラム説明
    # 0 Time
    # 1 Chip Time()
    # 2 Acceleration X(g)	
    # 3 Acceleration Y(g)	
    # 4 Acceleration Z(g)	
    # 5 Angular velocity X(°/s)	
    # 6 Angular velocity Y(°/s)		
    # 7 SpeedZ(mm/s)	
    # 8 Angle X(°)	
    # 9 Angle Y(°)	
    # 10 Angle Z(°)	
    # 11 Magnetic field X(ʯt)	
    # 12 Magnetic field Y(ʯt)	
    # 13 Magnetic field Z(ʯt)	
    # 14 Temperature(℃)	
    # 15 Quaternions 0()	
    # 16 Quaternions 1()	
    # 17 Quaternions 2()	
    # 18 Quaternions 3()	
    # 19 Raw power()	
    # 20 Power Percent(%)()

    return if1_means,if2_means, df1_nums, df2_nums

#単体でのテスト用コード
if __name__ == "__main__":
    
    #csvファイル読み込み
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

    #不要な行の削除 使わない
    # delete_columns = [9,10,11,12,13,14]
    # np.delete(df1, [9,10,11,12,13,14], axis=1)

    #初期データの平均値計算　数値部分のみ抜き出す

    #データのカラム説明
    # 0 Time
    # 1 Chip Time()
    # 2 Acceleration X(g)	
    # 3 Acceleration Y(g)	
    # 4 Acceleration Z(g)	
    # 5 Angular velocity X(°/s)	
    # 6 Angular velocity Y(°/s)		
    # 7 SpeedZ(mm/s)	
    # 8 Angle X(°)	
    # 9 Angle Y(°)	
    # 10 Angle Z(°)	
    # 11 Magnetic field X(ʯt)	
    # 12 Magnetic field Y(ʯt)	
    # 13 Magnetic field Z(ʯt)	
    # 14 Temperature(℃)	
    # 15 Quaternions 0()	
    # 16 Quaternions 1()	
    # 17 Quaternions 2()	
    # 18 Quaternions 3()	
    # 19 Raw power()	
    # 20 Power Percent(%)()

    if1_nums = if1.select_dtypes(include='number')
    if1_means = if1_nums.mean(axis=0)
    print(if1_means)

    df1_nums = df1.select_dtypes(include='number')