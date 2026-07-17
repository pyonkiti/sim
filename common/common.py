import yaml
import re
import common.config as config
from datetime import date

# --------------------------------------------------------------------
# 共通処理
# --------------------------------------------------------------------
class COMMON:

    # --------------------------------------------------------------------
    # 引数の入力チェック
    # --------------------------------------------------------------------
    def check_argv(self, argv):

        if len(argv[1:]) == 0:
            msg = "引数が指定されていません。"
            return False, None, msg

        if len(argv[1:]) != 1:
            msg = "引数は１つしか指定できません。"
            return False, None, msg
        
        if not argv[1].isdecimal():
            msg = "引数には数値しか指定できません。"
            return False, None, msg
        
        return True, argv[1], None
    
    # --------------------------------------------------------------------
    # YAMLファイルの読み込み
    # --------------------------------------------------------------------
    def get_yaml(self, ordinal_nm):

        try:
            if not config.path_yml.exists():
                msg = "yamlファイルが存在しません。"
                return False, msg
            
            with open(config.path_yml, mode = "r", encoding = "utf-8") as f:
                system = yaml.safe_load(f)

            config.headers                  = system["headers"]                              # ヘッダー
            config.sim["jido_saiban"]       = system["col"][ordinal_nm]["jido_saiban"]       # 自動採番
            config.sim["user_code"]         = system["col"][ordinal_nm]["user_code"]         # 自動採番（ユーザー）

            if system["col"][ordinal_nm]["sinsei_ymd"] in ("yyyy-mm-dd", None, ""):
                config.sim["sinsei_ymd"]    = date.today().strftime("%Y-%m-%d")              # 申請日
            else:
                config.sim["sinsei_ymd"]    = system["col"][ordinal_nm]["sinsei_ymd"]        # 申請日

            config.sim["active_no"]         = system["col"][ordinal_nm]["active_no"]         # ACTIVE番号
            config.sim["genti_kisyu"]       = system["col"][ordinal_nm]["genti_kisyu"]       # 現地機種
            config.sim["sisetu_no"]         = system["col"][ordinal_nm]["sisetu_no"]         # 施設番号
            config.sim["sisetu_name"]       = system["col"][ordinal_nm]["sisetu_name"]       # 施設名
            config.sim["sim_no"]            = system["col"][ordinal_nm]["sim_no"]            # SIM番号
            config.sim["foma_kaisen_no"]    = system["col"][ordinal_nm]["foma_kaisen_no"]    # FOMA回線番号
            config.sim["ninsyo_id"]         = system["col"][ordinal_nm]["ninsyo_id"]         # 認証ID
            config.sim["ninsyo_pwd"]        = system["col"][ordinal_nm]["ninsyo_pwd"]        # 認証パスワード
            config.sim["kotei_ip"]          = system["col"][ordinal_nm]["kotei_ip"]          # 固定IP
            config.sim["keiyaku_plan"]      = system["col"][ordinal_nm]["keiyaku_plan"]      # 契約プラン
            config.sim["kyakudasi_plan"]    = system["col"][ordinal_nm]["kyakudasi_plan"]    # 客出しプラン
            config.sim["setuzoku_type"]     = system["col"][ordinal_nm]["setuzoku_type"]     # 接続タイプ
            config.sim["genkyo"]            = system["col"][ordinal_nm]["genkyo"]            # 現況
            config.sim["nippou"]            = system["col"][ordinal_nm]["nippou"]            # 日報
            config.sim["rialtime_trend"]    = system["col"][ordinal_nm]["rialtime_trend"]    # リアルタイムトレンド
            config.sim["goriyo_kaisi_ymd"]  = system["col"][ordinal_nm]["goriyo_kaisi_ymd"]  # ご利用開始日
            config.sim["haisi_ymd"]         = system["col"][ordinal_nm]["haisi_ymd"]         # 廃止日
            config.sim["yusyo_kaishi_ymd"]  = system["col"][ordinal_nm]["yusyo_kaishi_ymd"]  # 有償開始年月
            config.sim["yusyo_syuryo_ymd"]  = system["col"][ordinal_nm]["yusyo_syuryo_ymd"]  # 有償終了年月
            config.sim["jigyou"]            = system["col"][ordinal_nm]["jigyou"]            # 事業
            config.sim["biko"]              = system["col"][ordinal_nm]["biko"]              # 備考 
            config.sim["tekiyo_jyogai"]     = system["col"][ordinal_nm]["tekiyo_jyogai"]     # 適用除外
            config.sim["dounyu_ki"]         = system["col"][ordinal_nm]["dounyu_ki"]         # 導入期
            config.sim["demo_otamesi"]      = system["col"][ordinal_nm]["demo_otamesi"]      # デモ・お試し利用
            config.sim["syanai_hokan_sim"]  = system["col"][ordinal_nm]["syanai_hokan_sim"]  # 社内保管分のSIM
            config.sim["syukeiyaku_nm"]     = system["col"][ordinal_nm]["syukeiyaku_nm"]     # 主契約者名
            config.sim["donyu_yy"]          = system["col"][ordinal_nm]["donyu_yy"]          # 導入年度(削除予定)
            config.sim["sisetu_no_del"]     = system["col"][ordinal_nm]["sisetu_no_del"]     # 施設番号(削除予定)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None
    
    # --------------------------------------------------------------------
    # CSVファイル名を採番する
    # --------------------------------------------------------------------
    def get_next_filename(self, path_csv, number):

        try:
            filenm = path_csv.stem                              # 拡張子を除いたファイル名
            suffix = path_csv.suffix                            # 拡張子(.txt など)

            # 末尾が "_数字" のパターンにマッチするか確認
            match = re.search(r'_\d+$', filenm)

            if match:
                # 末尾の "_数字" を新しい番号に置き換える
                new_filenm = filenm[:match.start()] + f"_{number}"
            else:
                # 末尾に番号がない場合は追加する
                new_filenm = f"{filenm}_{number}"

            path_csv_next = path_csv.parent / f"{new_filenm}{suffix}"

            return True, path_csv_next, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, None, msg
        finally:
            None

    # --------------------------------------------------------------------
    # CSVファイルの存在チェック
    # --------------------------------------------------------------------
    def check_csvfile(self, path_file):

        if path_file.exists() and path_file.is_file():
            None
        else:
            msg = "指定したcsvファイルが存在しません"
            return False, msg

        return True, None
    