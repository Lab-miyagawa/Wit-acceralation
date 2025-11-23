import numpy as np
from scipy.spatial.transform import Rotation as R

def euler_to_rotation_matrix_scipy_ZYX(angles_deg):
    """
    SciPyを使用してオイラー角 (ロール、ピッチ、ヨー) から回転行列を計算します (ZYX順)。
    
    引数:
        angles_rad (tuple/list/np.array): (Θroll, Θpitch, Θyaw) のラジアン値
        
        注意: SciPyの 'ZYX' 順序では、入力順は (Yaw, Pitch, Roll) です。
              ここでは、入力のタプルを (Roll, Pitch, Yaw) と想定し、
              内部で (Yaw, Pitch, Roll) に並べ替えます。

    戻り値:
        np.array: 3x3 回転行列
    """
    # 1124 出力される回転行列はX：pitch、Y：roll、Z：yawの順番になっている
    # 計算順序はZYX
    # 入力の順序: (Roll, Pitch, Yaw)
    angles_rad = np.radians(angles_deg)
    roll, pitch, yaw = angles_rad[1], angles_rad[0], angles_rad[2]
    
    # SciPyの 'ZYX' オイラー角順序: (Z-angle=Yaw, Y-angle=Pitch, X-angle=Roll)
    euler_scipy_order = np.array([yaw, pitch, roll])
    
    # Rotationオブジェクトを作成し、回転行列に変換
    rot = R.from_euler('ZYX', euler_scipy_order, degrees=False)
    
    return rot.as_matrix()



def rotation_matrix_to_euler_scipy_ZYX(R_matrix):
    """
    SciPyを使用して回転行列からオイラー角 (ロール、ピッチ、ヨー) を計算します (ZYX順)。
    結果はラジアン値のタプルです。
    
    引数:
        R_matrix (np.array): 3x3 回転行列
    
    戻り値:
        tuple: (Θroll, Θpitch, Θyaw) のラジアン値
    """
    # Rotationオブジェクトを作成
    rot = R.from_matrix(R_matrix)
    
    # SciPyの 'ZYX' 順序でオイラー角を取得 (Yaw, Pitch, Roll の順)
    euler_scipy_order = rot.as_euler('ZYX', degrees=False)
    
    # 出力の順序を (Roll, Pitch, Yaw) に戻す
    yaw, pitch, roll = euler_scipy_order[0], euler_scipy_order[1], euler_scipy_order[2]
    
    return (roll, pitch, yaw)

#単体でのテスト用コード
if __name__ == "__main__":
    # 例
    # 45度(π/4)のロール、30度(π/6)のピッチ、60度(π/3)のヨー
    roll_deg = 45
    pitch_deg = 30
    yaw_deg = 60

    R_matrix_scipy = euler_to_rotation_matrix_scipy_ZYX((roll_deg, pitch_deg, yaw_deg))

    print("--- euler_to_rotation_matrix_scipy_ZYX の出力例 ---")
    print(f"入力オイラー角 (deg): (Roll:{roll_deg}, Pitch:{pitch_deg}, Yaw:{yaw_deg})")
    print(R_matrix_scipy)

    # 例
    # 上記で計算した回転行列 R_matrix_scipy を使用
    angles_recovered_scipy = rotation_matrix_to_euler_scipy_ZYX(R_matrix_scipy)

    print("\n--- rotation_matrix_to_euler_scipy_ZYX の出力例 ---")
    print(f"入力回転行列:\n{R_matrix_scipy}")
    print(f"復元されたオイラー角 (rad): (Roll:{angles_recovered_scipy[0]:.3f}, Pitch:{angles_recovered_scipy[1]:.3f}, Yaw:{angles_recovered_scipy[2]:.3f})")
    print(f"復元されたオイラー角 (deg): (Roll:{np.degrees(angles_recovered_scipy[0]):.3f}, Pitch:{np.degrees(angles_recovered_scipy[1]):.3f}, Yaw:{np.degrees(angles_recovered_scipy[2]):.3f})")
    print(f"元のオイラー角 (deg):      (Roll:{roll_deg}, Pitch:{pitch_deg}, Yaw:{yaw_deg})")
