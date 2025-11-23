import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime, timezone, timedelta

# ==== 日本標準時（JST）のタイムゾーン設定 ====
JST = timezone(timedelta(hours=9))

# ==== このスクリプトと同じフォルダにCSVを作成 ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "experiment_log.csv")


class ExperimentLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("実験データロガー")

        self.start_time = None

        # ====== 曲選択 ======
        frame_music = ttk.LabelFrame(root, text="曲選択")
        frame_music.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_music, text="曲:").pack(side="left", padx=5, pady=5)

        self.music_var = tk.StringVar()
        self.music_combo = ttk.Combobox(
            frame_music,
            textvariable=self.music_var,
            state="readonly",
            width=30,
            values=[
                "G線上のアリア（ゆっくり）",
                "威風堂々：前半（速い）",
                "威風堂々：中間部（変化）",
            ],
        )
        self.music_combo.current(0)
        self.music_combo.pack(side="left", padx=5, pady=5)

        # ====== 演奏者数 ======
        frame_players = ttk.LabelFrame(root, text="演奏者数")
        frame_players.pack(padx=10, pady=5, fill="x")

        self.players_var = tk.IntVar(value=1)
        ttk.Radiobutton(frame_players, text="1人", variable=self.players_var, value=1).pack(
            side="left", padx=5, pady=5
        )
        ttk.Radiobutton(frame_players, text="2人", variable=self.players_var, value=2).pack(
            side="left", padx=5, pady=5
        )

        # ====== 演奏結果 ======
        frame_result = ttk.LabelFrame(root, text="演奏結果")
        frame_result.pack(padx=10, pady=5, fill="x")

        self.result_var = tk.StringVar(value="成功")
        ttk.Radiobutton(frame_result, text="成功", variable=self.result_var, value="成功").pack(
            side="left", padx=5, pady=5
        )
        ttk.Radiobutton(frame_result, text="中止", variable=self.result_var, value="中止").pack(
            side="left", padx=5, pady=5
        )

        # ====== ボタン ======
        frame_buttons = ttk.Frame(root)
        frame_buttons.pack(padx=10, pady=10, fill="x")

        self.btn_start = ttk.Button(frame_buttons, text="開始", command=self.on_start)
        self.btn_start.pack(side="left", padx=5)

        self.btn_stop = ttk.Button(frame_buttons, text="終了 & 記録", command=self.on_stop)
        self.btn_stop.pack(side="left", padx=5)
        self.btn_stop.state(["disabled"])  # 初期状態は無効

        # ====== ステータス表示 ======
        self.status_var = tk.StringVar(value="待機中")
        self.label_status = ttk.Label(root, textvariable=self.status_var)
        self.label_status.pack(padx=10, pady=(0, 10), anchor="w")

        # CSVのヘッダを準備
        self.ensure_csv_header()

    def ensure_csv_header(self):
        """CSVがなければヘッダ付きで作成"""
        if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
            with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["start_time", "end_time", "duration_sec", "music", "num_players", "result"]
                )

    def on_start(self):
        """開始ボタンが押されたとき"""
        if self.start_time is not None:
            messagebox.showwarning("警告", "すでに計測中です。")
            return

        # JSTで現在時刻を取得
        self.start_time = datetime.now(JST)
        self.status_var.set(f"計測中… 開始時刻: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.btn_start.state(["disabled"])
        self.btn_stop.state(["!disabled"])

    def on_stop(self):
        """終了ボタンが押されたとき（CSVに1行追記）"""
        if self.start_time is None:
            messagebox.showwarning("警告", "開始ボタンを押してから終了してください。")
            return

        # JSTで終了時刻
        end_time = datetime.now(JST)
        duration = (end_time - self.start_time).total_seconds()

        music = self.music_var.get()
        num_players = self.players_var.get()
        result = self.result_var.get()

        # CSVに書き込み
        try:
            with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        f"{duration:.3f}",
                        music,
                        num_players,
                        result,
                    ]
                )
        except Exception as e:
            messagebox.showerror("エラー", f"CSVへの書き込みに失敗しました:\n{e}")
            return

        self.status_var.set(
            f"記録完了: {self.start_time.strftime('%H:%M:%S')} → {end_time.strftime('%H:%M:%S')} "
            f"({duration:.1f} 秒) | 曲: {music}, 人数: {num_players}, 結果: {result}"
        )

        # 状態リセット
        self.start_time = None
        self.btn_start.state(["!disabled"])
        self.btn_stop.state(["disabled"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentLoggerApp(root)
    app.run()
