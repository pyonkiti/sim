# 施設名だけのテキストファイルから、楽楽にインポートするフォーマットを作成する処理です。

import sys
import csv
from pathlib  import Path
import common.common as COM
import common.config as config

path_csv = Path(r"C:\vagrant\sim\csv\sample.txt")         # CSVファイルの元ファイル

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
class PROC_MAIN:

    # --------------------------------------------------------------------
    # （01）ヘッダを追加
    # --------------------------------------------------------------------
    def add_header():
        
        try:
            # CSVファイルの採番
            ret, path_csv_next, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: raise

            # CSVファイルの読み込み/書き込み
            with open(path_csv,  mode = "r", encoding = "utf-8", newline = "") as infile, \
                 open(path_csv_next, mode = "w", encoding = "utf-8", newline = "") as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)
                
                outfile.write(",".join('"' + h + '"' for h in config.headers))
                outfile.write("\r\n") 
                
                for row in reader:
                    writer.writerow(row)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # （02）先頭行に自動採番を追加
    # --------------------------------------------------------------------
    def add_colum_saiban():
        
        try:
            # CSVファイルの採番
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: raise

            # CSVファイルの採番
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "02")
            if not ret: raise

            with open(path_csv_now,  mode = "r", encoding = "utf-8", newline = "") as infile, \
                 open(path_csv_nxt, mode = "w", encoding = "utf-8", newline = "") as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                # ヘッダー行を書き出す
                header = next(reader)
                writer.writerow(header)

                # 2行目以降に連番を追加（空行はスキップ）
                icnt = 0
                for row in reader:
                    if not any(field.strip() for field in row):
                        continue

                    seq_num = str(int(config.sim["jido_saiban"]) + icnt)            # 自動採番
                    new_row = [seq_num] + row                                       # 自動採番＋施設名

                    ## 各フィールドをダブルクォートで囲む（フィールド内の " は "" にエスケープ）
                    quoted_fields = ['"' + field.replace('"', '""') + '"' for field in new_row]
                    line = ",".join(quoted_fields) + "\n"

                    outfile.write(line)

                    icnt += 1

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # （03）施設名の前後に固定項目を追加
    # --------------------------------------------------------------------
    def add_colum_other():

        try:
            # CSVファイルの採番
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "02")
            if not ret: raise

            # CSVファイルの採番
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "03")
            if not ret: raise

            with open(path_csv_now,  mode = "r", encoding = "utf-8", newline = "") as infile, \
                 open(path_csv_nxt, mode = "w", encoding = "utf-8", newline = "") as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                # ヘッダー行をそのまま書き出す
                header = next(reader)
                writer.writerow(header)

                # 2行目以降の2列目に固定文字列を挿入（空行はスキップ）
                for row in reader:
                    if not any(field.strip() for field in row):
                        continue

                    new_row     = [""] * len(config.headers)            # 全列を初期化
                    new_row[0]  = row[0]                                # 自動採番
                    new_row[1]  = config.sim["user_code"]               # 自動採番（ユーザー）
                    new_row[2]  = config.sim["sinsei_ymd"]              # 申請日
                    new_row[3]  = config.sim["active_no"]               # ACTIVE番号
                    new_row[4]  = config.sim["genti_kisyu"]             # 現地機種
                    new_row[6]  = row[1]                                # 施設名
                    new_row[12] = config.sim["keiyaku_plan"]            # 契約プラン
                    new_row[13] = config.sim["kyakudasi_plan"]          # 客出しプラン
                    new_row[22] = config.sim["jigyou"]                  # 事業
                    new_row[29] = config.sim["donyu_yy"]                # 導入年度(削除予定)

                    writer.writerow(new_row)
            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # （04）全列がNoneの列を削除
    # --------------------------------------------------------------------
    def del_colum_none():

        try:
            # CSVファイルの採番
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "03")
            if not ret: raise

            # CSVファイルの採番
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "04")
            if not ret: raise

            with open(path_csv_now, mode = "r", encoding = "utf-8", newline = "") as infile:
                reader = csv.reader(infile)
                rows   = list(reader)

            # ヘッダーとデータ行を分離
            header    = rows[0]
            data_rows = rows[1:]

            # データ行においてすべてが""の列インデックスを特定
            empty_col_indexes = set()
            for col_idx in range(len(header)):
                if all(row[col_idx] == "" for row in data_rows if len(row) > col_idx):
                    empty_col_indexes.add(col_idx)

            # 空列を除外して書き出す
            with open(path_csv_nxt, mode = "w", encoding = "utf-8", newline = "") as outfile:
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                for row in rows:
                    new_row = [field for col_idx, field in enumerate(row)
                            if col_idx not in empty_col_indexes]
                    writer.writerow(new_row)

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

        # CSVファイルの存在チェック
        ret, msg = COMMON.check_csvfile(path_csv)
        if not ret: raise

        # YAMLファイルの読み込み
        ret, msg = COMMON.get_yaml("sec")
        if not ret: raise

        match argv:
            case "01":
                # （01） ヘッダを追加
                ret, msg = PROC_MAIN.add_header()

            case "02":
                # （02） 先頭行に自動採番を追加
                ret, msg = PROC_MAIN.add_colum_saiban()

            case "03":
                # （03） 施設名の前後に固定項目を追加
                ret, msg = PROC_MAIN.add_colum_other()

            case "04":
                # （04）全列がNoneの列を削除
                ret, msg = PROC_MAIN.del_colum_none()

            case _:
                ret = False
                msg = "引数に該当する処理がありません。"
                
        if not ret: raise

    except Exception as e:
        print(msg)
    finally:
        None
    
# メイン処理
main()
