# ドコモビジネスからダウンロードしたCSVファイルを加工する処理です。

import sys
import csv
from pathlib  import Path
import common.common as COM
import common.config as config

# ドコモビジネスからダウンロードした元ファイルをこの名前にリネームします。
path_csv = Path(r"C:\vagrant\sim\csv\TypeComゼロSIM一覧.csv")         # CSVファイルの元ファイル

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
class PROC_MAIN:

    # --------------------------------------------------------------------
    # （01）不要なカラムを削除
    # --------------------------------------------------------------------
    def del_colum():
        
        try:
            # CSVファイルの採番
            ret, path_csv_next, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: raise

            with open(path_csv, mode = 'r', encoding='utf-8-sig', newline = '') as infile, \
                open(path_csv_next, mode = 'w', encoding='utf-8', newline = '') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                # ヘッダー行の処理
                header = next(reader)
                writer.writerow([header[0], header[11], header[16]])

                # データ行の抽出（回線番号,SIMカード番号,国内用IPACT）
                for row in reader:
                    writer.writerow([row[0], row[11], row[16]])

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # （02）自動採番を追加
    # --------------------------------------------------------------------
    def add_colum_saiban():

        try:
            # CSVファイルの採番
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "01")
            if not ret: raise

            # CSVファイルの採番
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "02")
            if not ret: raise

            with open(path_csv_now, mode = 'r', encoding = 'utf-8', newline = '') as infile, \
                open(path_csv_nxt, mode = 'w', encoding = 'utf-8', newline = '') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                header = next(reader)
                writer.writerow(['自動採番'] + header)

                # データ行に連番を付与して書き込む（start_numberから開始）
                for icnt, row in enumerate(reader, start = config.sim["jido_saiban"]):
                    writer.writerow([icnt] + row)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # --------------------------------------------------------------------
    # （03）IPカラムを削除
    # --------------------------------------------------------------------
    def del_colum_ip():

        try:
            # CSVファイルの採番
            ret, path_csv_now, msg = COMMON.get_next_filename(path_csv, "02")
            if not ret: raise

            # CSVファイルの採番
            ret, path_csv_nxt, msg = COMMON.get_next_filename(path_csv, "03")
            if not ret: raise

            with open(path_csv_now, mode = 'r', encoding = 'utf-8', newline = '') as infile, \
                open(path_csv_nxt, mode = 'w', encoding = 'utf-8', newline = '') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile, quoting = csv.QUOTE_ALL)

                #IPカラムを取り除く
                for row in reader:
                    writer.writerow(row[:-1])

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
        ret, msg = COMMON.get_yaml("trd")
        if not ret: raise

        match argv:
            case "01":
                # （01） 不要なカラムを削除
                ret, msg = PROC_MAIN.del_colum()

            case "02":
                # （02） 自動採番を追加
                ret, msg = PROC_MAIN.add_colum_saiban()

            case "03":
                # （03） IPカラムを削除
                ret, msg = PROC_MAIN.del_colum_ip()

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
