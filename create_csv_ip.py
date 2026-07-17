# 楽楽の新規作成するゼロSIMデータを作成します。自動採番＋IP＋固定項目を更新します。

import sys
import csv
import common.config as config
import common.common as COM
from pathlib  import Path

path_csv = Path(r"C:\vagrant\sim\csv\create_csv_ip.txt")            # CSVファイルの元ファイル

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
class PROC_MAIN:

    # --------------------------------------------------------------------
    # CSVファイルを更新する（自動採番）
    # --------------------------------------------------------------------
    def add_colum_ip():

        try:
            parts    = config.sim["kotei_ip"].split(".")
            prefix   = ".".join(parts[:3])                          # XXX.XXX.XXX
            start    = int(parts[3])                                # 第4オクテットの開始番号

            if start < 1:
                msg = "IPアドレスの第4オクテットに1より小さい値は設定できません"
                return False, msg

            if start > 254:
                msg = "IPアドレスの第4オクテットに254より大きい値は設定できません"
                return False, msg

            ip_list = [f"{prefix}.{i}" for i in range(start, 254 + 1)]

            path_csv.unlink(missing_ok = True)
            path_csv.touch()

            # CSVファイルを作成
            with open(path_csv, mode = "w", encoding = "utf-8", newline = "") as f:
                writer = csv.writer(f, quoting = csv.QUOTE_ALL)

                # ヘッダー行を書き込む
                writer.writerow(config.headers)

                # データ行を書き込む
                for i, ip in enumerate(ip_list):
                    row     = [""] * len(config.headers)            # 全列を初期化
                    row[0]  = config.sim["jido_saiban"] + i         # 自動採番
                    row[11] = ip                                    # 固定IP

                    writer.writerow(row)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # CSVファイルを更新する（施設名）
    # --------------------------------------------------------------------
    def add_colum_other():

        try:
            # CSVファイルの採番
            ret, path_csv_next, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: return False, msg

            # CSVファイルの読み込み
            with open(path_csv, mode = "r", encoding = "utf-8-sig", newline = "") as f_in:

                reader = csv.reader(f_in)
                rows   = list(reader)

            if not rows:
                return False, "CSVにデータがありません。"

            header = rows[0]
            data_rows = rows[1:]

            for row in data_rows: 
                row[1]  = config.sim["user_code"]           # 自動採番（ユーザー）
                row[6]  = row[11]                           # IPアドレスを施設名にセット
                row[9]  = config.sim["ninsyo_id"]           # 認証ID
                row[10] = config.sim["ninsyo_pwd"]          # 認証パスワード
                row[12] = config.sim["keiyaku_plan"]        # 契約プラン
                row[18] = config.sim["goriyo_kaisi_ymd"]    # ご利用開始日
                row[28] = config.sim["syukeiyaku_nm"]       # 主契約者名

            path_csv_next.unlink(missing_ok = True)
            path_csv_next.touch()

            # CSVファイルの書き込み
            with open(path_csv_next, mode = "w", encoding = "utf-8-sig", newline = "") as f_out:

                writer = csv.writer(f_out, quoting = csv.QUOTE_ALL) 
                writer.writerow(header)
                writer.writerows(data_rows)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # CSVファイルから列を削除する（自動採番）
    # --------------------------------------------------------------------
    def del_colum_jido_saiban():

        try:
            # CSVファイルの採番（今のファイル）
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: return False, msg

            # CSVファイルの採番（次のファイル）
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "02")
            if not ret: return False, msg

            path_csv_nxt.unlink(missing_ok = True)
            path_csv_nxt.touch()

            with open(path_csv_now, mode = "r", encoding = "utf-8", newline = "") as f_in, \
                open(path_csv_nxt, mode = "w", encoding = "utf-8", newline = "") as f_out:

                reader = csv.reader(f_in)
                writer = csv.writer(f_out, quoting = csv.QUOTE_ALL)

                # 自動採番列を削除
                for row in reader:
                    writer.writerow(row[1:])

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

COMMON = COM.COMMON()

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
def main():
    try:
        # 引数の入力チェック
        ret, argv, msg = COMMON.check_argv(sys.argv)
        if not ret: raise

        # YAMLファイルの読み込み
        ret, msg = COMMON.get_yaml("fst")
        if not ret: raise

        match argv:
            case "01":
                # CSVファイルを更新する（自動採番＋IP）
                ret, msg = PROC_MAIN.add_colum_ip()

            case "02":
                # CSVファイルを更新する（施設名＋固定項目）
                ret, msg = PROC_MAIN.add_colum_other()

            case "03":
                # CSVファイルから列を削除する（自動採番）
                ret, msg = PROC_MAIN.del_colum_jido_saiban()

            case _:
                ret , msg = False, "引数に該当する処理がありません。"
                
        if not ret: raise

    except Exception as e:
        print(msg)
        None
    finally:
        None
    
# メイン処理
main()
