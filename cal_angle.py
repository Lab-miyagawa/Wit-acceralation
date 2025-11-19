import numpy as np  
import pandas as pd
import cal_matrix as cm

# 与えられた姿勢データから手首角度を計算する関数
def calculate_wrist_angle(data_w,data_h,init_w,init_h):
    
    #初期姿勢の回転行列計算
    w_init = cm.euler_to_rotation_matrix_scipy_ZYX(init_w)
    h_init = cm.euler_to_rotation_matrix_scipy_ZYX(init_h)
    
    #ToDo : データ長の不一致対応 短いほうに合わせる タイムスタンプ参照
    n = min(len(data_w), len(data_h))
    wrist_angle = np.zeros((n, 3))  # 手首角度を格納する配列 (ラジアン)
    for i in range(n):
        # 姿勢データから手首角度を算出する
        w_turn_deg = data_w[i][15:18]  # 例:手首のロール、ピッチ、ヨー角度
        h_turn_deg = data_h[i][15:18]  # 例:手の甲のロール、ピッチ、ヨー角度
        #1.回転行列の計算
        w_turn = cm.euler_to_rotation_matrix_scipy_ZYX(w_turn_deg)
        h_turn = cm.euler_to_rotation_matrix_scipy_ZYX(h_turn_deg)

        #2.初期姿勢からの相対化
        #逆行列の計算
        invw_i = np.linalg.inv(w_init)
        invh_i = np.linalg.inv(h_init)

        #初期姿勢からの回転行列の計算
        w_i_t = np.dot(invw_i, w_turn)
        h_i_t = np.dot(invh_i, h_turn)

        #3.手首と手の甲の相対化
        #逆行列の計算
        invw_it = np.linalg.inv(w_i_t)
        #手首に対する手の甲の回転行列の計算
        b_a = np.dot(invw_it, h_i_t)

        print(b_a)

        #4.手首角度の計算
        wrist_angle[i][0:3] = cm.rotation_matrix_to_euler_scipy_ZYX(b_a)
        # print("Wrist angle (rad):", wrist_angle)
        # print("Wrist angle (deg):", np.degrees(wrist_angle))

    return wrist_angle  # ラジアン値の配列を返す

#単体でのテスト用コード
if __name__ == "__main__":
    姿勢データから手首角度を算出する
    w_init_deg = [-3.664, -0.807,178.072]  # 例:手首の初期ロール、ピッチ、ヨー角度
    h_init_deg = [14.233, -11.354, -3.966]  # 例:手の甲の姿勢ロール、ピッチ、ヨー角度
    w_turn_deg = [75.877, -8.992, -19.587]  # 例:手首のロール、ピッチ、ヨー角度
    h_turn_deg = [-7.495, 6.548, -172.667]  # 例:手の甲のロール、ピッチ、ヨー角度
    # a = [a_turn[i] - a_init[i] for i in range(3)]
    # b = [b_turn[i] - b_init[i] for i in range(3)]
    # wrist_angle = np.array(b) - np.array(a)
    # print(wrist_angle.tolist())

    #1.回転行列の計算
    w_init = cm.euler_to_rotation_matrix_scipy_ZYX(w_init_deg)
    h_init = cm.euler_to_rotation_matrix_scipy_ZYX(h_init_deg)
    w_turn = cm.euler_to_rotation_matrix_scipy_ZYX(w_turn_deg)
    h_turn = cm.euler_to_rotation_matrix_scipy_ZYX(h_turn_deg)

    #2.初期姿勢からの相対化
    #逆行列の計算
    invw_i = np.linalg.inv(w_init)
    invh_i = np.linalg.inv(h_init)

    #初期姿勢からの回転行列の計算
    w_i_t = np.dot(invw_i, w_turn)
    h_i_t = np.dot(invh_i, h_turn)

    #3.手首と手の甲の相対化
    #逆行列の計算
    invw_it = np.linalg.inv(w_i_t)
    #手首に対する手の甲の回転行列の計算
    b_a = np.dot(invw_it, h_i_t)

    print(b_a)

    #4.手首角度の計算
    wrist_angle = cm.rotation_matrix_to_euler_scipy_ZYX(b_a)
    print("Wrist angle (rad):", wrist_angle)
    print("Wrist angle (deg):", np.degrees(wrist_angle)) 
