# Seleniumで楽楽販売の画面を表示するツールです

import time
import sys
import io
import re

from pathlib                            import Path
from datetime                           import date
from selenium                           import webdriver
from selenium.webdriver.chrome.options  import Options
from selenium.webdriver.common.by       import By
from selenium.webdriver.common.keys     import Keys

import common.common as COM
import common.config as config

path_txt = Path(r"C:\vagrant\sim\csv")         # txtファイルの存在フォルダ

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
class PROC_MAIN:

    # ----------------------------------------------------------------
    # 初期処理
    # ----------------------------------------------------------------
    def init_selenium():
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            options.add_argument("--log-level=1")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            driver = webdriver.Chrome(options=options)
            config.driver = driver

            config.driver.get("https://hncapitol.rakurakuhanbai.jp/wfecn6a/")
            time.sleep(0.3)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # ログイン処理
    # ----------------------------------------------------------------
    def disp_login():
            
        try:
            # ログインID
            config.driver.find_element(By.NAME, "loginId").send_keys(config.rakuraku["id"])
            time.sleep(0.2)

            # パスワード
            config.driver.find_element(By.NAME, "loginPassword").send_keys(config.rakuraku["pw"])
            time.sleep(0.2)

            # ログインボタン
            config.driver.find_element(By.ID, "jq-loginSubmit").click()
            time.sleep(0.3)

            # ログイン判断
            if len(config.driver.find_elements(By.CLASS_NAME, "fw-message-text-main")) >= 1:
                msg = config.driver.find_element(By.CLASS_NAME, "fw-message-text-main").text
                if "ログインに失敗" in msg:
                    return False, "ログインID、または、パスワードに誤りがあります。"

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # 端末ID管理－施設テーブル－ゼロSIM一覧を選択
    # ----------------------------------------------------------------
    def disp_tanmatuid():

        try:
            # iframeを取得
            config.driver.switch_to.frame("side")

            # 端末ID管理
            config.driver.find_element(By.ID, "nav-dbg-100169").click()
            time.sleep(0.3)

            # 施設テーブル
            config.driver.find_element(By.ID, 'nav-db-101341').click()
            time.sleep(0.3)

            # ゼロSIM一覧
            config.driver.find_element(By.ID, 'menuli_102550').click()
            time.sleep(0.3)

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # ゼロSIM一覧を編集
    # ----------------------------------------------------------------
    def upd_tanmatuid():

        try:
            # 画面遷移
            config.driver.switch_to.default_content()
            config.driver.switch_to.frame("main")

            # 編集ボタン
            # 編集のrecord_idは起動の度に変化するため毎回取得する
            current_url = config.driver.page_source
            time.sleep(1.0)
            match = re.search(r"recordId/(\d+)", current_url)

            if match:
                record_id = match.group(1)
                config.driver.find_element(By.CSS_SELECTOR, f"#recordAct_{record_id} a[title='編集']").click()
            else:
                print("編集ボタンのrecordIdをHTMLから取得できませんでした")
                raise
            time.sleep(0.3)

            # 自動採番（ユーザー）にセット
            field = config.driver.find_element(By.ID, "field_110725")
            field.clear()
            field.send_keys(config.sim["user_code"])
            field.send_keys(Keys.TAB)
            time.sleep(0.2)

            # 申請日（《現在》をクリック）
            config.driver.find_element(By.CSS_SELECTOR, 'a[href*="setNowDate(\'111901\'"]').click()
            time.sleep(0.3)

            # Active番号
            field = config.driver.find_element(By.ID, "field_112075")
            field.clear()
            field.send_keys(config.sim["active_no"])
            time.sleep(0.2)

            # 施設名
            field = config.driver.find_element(By.ID, "field_110706")
            field.clear()
            field.send_keys(config.sim["sisetu_name"])
            field.send_keys(Keys.TAB)
            time.sleep(0.2)

            # 契約プラン（名称を取得）
            ret, msg = COM_PRI.get_name("keiyaku_plan", config.sim["kyakudasi_plan"])
            if not ret: raise
            
            # 契約プラン
            field = config.driver.find_element(By.ID, "field_110712")
            field.clear()
            field.send_keys(config.sim["keiyaku_plan"])
            field.send_keys(Keys.TAB)
            time.sleep(0.2)

            # 事業（value値を取得）
            ret, val, msg = PROC_MAIN.get_jigyou(config.sim["jigyou"])
            if not ret: raise

            # 事業（ラジオボタン）
            if not val == "":
                input_id = f"field_111500_{val}"
                config.driver.find_element(By.CSS_SELECTOR, f'label[for="{input_id}"]').click()
                time.sleep(0.2)

            # 客出しプラン（名称を取得）
            ret, msg = COM_PRI.get_name("kyakudasi_plan", config.sim["kyakudasi_plan"])
            if not ret: raise

            # 客出しプラン
            field = config.driver.find_element(By.ID, "field_110713")
            field.clear()
            field.send_keys(config.sim["kyakudasi_plan"])
            field.send_keys(Keys.TAB)
            time.sleep(0.2)

            # 期を取得
            ret, msg = COM_PRI.get_ki()
            if not ret: raise

            # 導入期
            field = config.driver.find_element(By.ID, "field_112649")
            field.clear()
            field.send_keys(config.sim["dounyu_ki"])
            field.send_keys(Keys.TAB)
            time.sleep(0.2)
                
            # 確定ボタンを押下は保留

            return True, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # 事業名からvalueを取得
    # ----------------------------------------------------------------
    def get_jigyou(target: str):

        try:
            RADIO_OPTIONS = {
                "110304": "公共（特環）下水処理場",
                "110305": "公共（特環）下水マンホールポンプ",
                "110306": "農集処理場",
                "110307": "農集マンホールポンプ",
                "108591": "水道",
                "110308": "雨水排水機場",
                "110309": "農業用水施設",
                "108594": "アンダーパス",
                "110310": "真空弁",
                "110311": "Xview",
                "110312": "VisualStageS",
                "110313": "浸水センサー",
                "110314": "工事現場",
                "108595": "その他",
                "110326": "防災",
            }

            matched_keys = [key for key, value in RADIO_OPTIONS.items() if target in value]

            if len(matched_keys) == 1:
                val = matched_keys[0]
            else:
                val = ""

            return True, val, None
        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, None, msg
        finally:
            None

# --------------------------------------------------------------------
# 共通クラス（個別）
# --------------------------------------------------------------------
class COM_PRI:
    # ----------------------------------------------------------------
    # txtファイルから名称を取得
    # ----------------------------------------------------------------
    def read_txtfile(txt_file):
        try:
            # txtファイルを読み込む
            with open(path_txt / txt_file, mode = "r", encoding = "utf-8") as f:
                lines = f.readlines()
            line_count = len(lines)

            for i in range(line_count):
                line = lines[i].strip()

                # ACTIVE番号
                if "ACTIVE" in line:
                    config.sim["active_no"] = line.replace("：", ":").split(":", 1)[1]

                # 自動採番（ユーザー）
                elif "エンドユーザー" in line:

                    line = line.replace("：", ":")
                    rest = line[len("エンドユーザー:"):]

                    # 末尾の数値部分だけを取り出す
                    # (.*?)  : 数値以外の部分(できるだけ短くマッチさせる)
                    # \s*    : 数値の前にあるスペース(任意の数)
                    # (\d+)  : 数値部分(1文字以上の数字)
                    # $      : 文字列の末尾
                    match = re.search(r"^(.*?)\s*(\d+)\s*$", rest)

                    if match:
                        config.sim["user_code"] = match.group(2)
                    else:
                        config.sim["user_code"] = ""

                # 施設名
                elif "施設名" in line:

                    line = line.replace("：", ":")
                    if ":" in line:
                        config.sim["sisetu_name"] = line.split(":", 1)[1]
                    else:
                        config.sim["sisetu_name"] = ""

                    if config.sim["sisetu_name"] == "":
                        # 次行の施設名を１行取得
                        if i + 1 < line_count:
                            config.sim["sisetu_name"] = lines[i + 1].strip()
                        
                # 事業
                elif "事業分類" in line:
                    config.sim["jigyou"] = line.replace("：", ":").split(":", 1)[1]
                            
                # 客出しプラン
                elif "プラン" in line:
                    config.sim["kyakudasi_plan"] = line.replace("：", ":").split(":", 1)[1]
                    
            return True, None

        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # 名称を取得
    # ----------------------------------------------------------------
    def get_name(komoku: str, target: str):
        try:
            match komoku:
                # 契約プラン
                case "keiyaku_plan":
                    match target:
                        case _ if "プレミアム"   in target:
                            ret = "TypeCom 500MB LTE"
                        case _ if "スタンダード" in target:
                            ret = "TypeCom 30MB LTE"
                        case _ if "ライト"       in target:
                            ret = "TypeCom 10MB LTE"
                        case _:
                            ret = ""
                    config.sim["keiyaku_plan"] = ret                    # 契約プラン

                # 客出しプラン
                case "kyakudasi_plan":
                    match target:
                        case _ if "プレミアム"   in target:
                            ret = "プレミアムプラン"
                        case _ if "スタンダード" in target:
                            ret = "スタンダードプラン"
                        case _ if "ライト"       in target:
                            ret = "ライトプラン"
                        case _:
                            ret = ""

                    config.sim["kyakudasi_plan"] = ret                  # 客出しプラン
                case _:
                    None

            return True, None
                
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

    # ----------------------------------------------------------------
    # 期を取得
    # ----------------------------------------------------------------
    def get_ki():
        try:
            start_ki = date(1971, 6, 1)                         # 開始期
            
            ki = date.today().year - start_ki.year
            if (date.today().month, date.today().day) < (start_ki.month, start_ki.day):
                ki -= 1
            else:
                ki += 1

            config.sim["dounyu_ki"] = f"{ki:02}"                # 導入期

            return True, None
                        
        except Exception as e:
            msg = f"例外エラーが発生しました。：{e}"
            return False, msg
        finally:
            None

# --------------------------------------------------------------------
# 開発テスト用
# --------------------------------------------------------------------
class TEST_DEV:
    # ソースを標準出力する
    def disp_source():
        print(config.driver.page_source)

# 標準出力の文字コードを指定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMMON = COM.COMMON()

# --------------------------------------------------------------------
# メイン処理
# --------------------------------------------------------------------
def main():
    try:
        # YAMLファイルの読み込み
        ret, msg = COMMON.get_yaml("rakuraku")
        if not ret: raise

        # txtファイルの存在チェック
        ret, fil, msg = COMMON.check_txtfile(path_txt)

        # txtファイルから名称を取得
        ret, msg = COM_PRI.read_txtfile(fil)
        if not ret: raise

        # 初期処理
        ret, msg = PROC_MAIN.init_selenium()
        if not ret: raise

        # ログイン
        ret, msg = PROC_MAIN.disp_login()
        if not ret: raise

        # 端末ID一覧を表示
        ret, msg = PROC_MAIN.disp_tanmatuid()
        if not ret: raise

        # 端末IDを編集
        ret, msg = PROC_MAIN.upd_tanmatuid()
        if not ret: raise

    except Exception as e:
        print(msg)
    finally:
        None
    
# メイン処理
main()
