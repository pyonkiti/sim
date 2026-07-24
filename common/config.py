# グローバル変数を設定するファイル

from pathlib  import Path

path_yml                   = Path(r"C:\vagrant\sim\common\SYSTEM.yaml")      # YAMLファイルのパス
headers                    = None                                            # 施設IDテーブルのヘッダー

# 施設IDテーブルの項目の変数（初期値はすべてNoneで統一）
sim = {"jido_saiban"       : None,        # 自動採番
       "kotei_ip"          : None,        # 固定IP
       "user_code"         : None,        # 自動採番（ユーザー）
       "sinsei_ymd"        : None,        # 申請日
       "active_no"         : None,        # ACTIVE番号
       "genti_kisyu"       : None,        # 現地機種
       "sisetu_no"         : None,        # 施設番号
       "sisetu_name"       : None,        # 施設名    
       "sim_no"            : None,        # SIM番号
       "foma_kaisen_no"    : None,        # FOMA回線番号
       "ninsyo_id"         : None,        # 認証ID
       "ninsyo_pwd"        : None,        # 認証パスワード
       "kotei_ip"          : None,        # 固定IP
       "keiyaku_plan"      : None,        # 契約プラン
       "kyakudasi_plan"    : None,        # 客出しプラン
       "setuzoku_type"     : None,        # 接続タイプ
       "genkyo"            : None,        # 現況
       "nippou"            : None,        # 日報
       "rialtime_trend"    : None,        # リアルタイムトレンド
       "goriyo_kaisi_ymd"  : None,        # ご利用開始日
       "haisi_ymd"         : None,        # 廃止日
       "yusyo_kaishi_ymd"  : None,        # 有償開始年月
       "yusyo_syuryo_ymd"  : None,        # 有償終了年月
       "jigyou"            : None,        # 事業
       "biko"              : None,        # 備考 
       "tekiyo_jyogai"     : None,        # 適用除外
       "dounyu_ki"         : None,        # 導入期
       "demo_otamesi"      : None,        # デモ・お試し利用
       "syanai_hokan_sim"  : None,        # 社内保管分のSIM
       "syukeiyaku_nm"     : None,        # 主契約者名
       "donyu_yy"          : None,        # 導入年度(削除予定)
       "sisetu_no_del"     : None}        # 施設番号(削除予定)

# 楽楽販売のID/PWDの変数（初期値はすべてNoneで統一）
rakuraku = {"id"           : None,        # ID
            "pw"           : None}        # PWD
