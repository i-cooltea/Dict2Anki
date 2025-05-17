import os
import shutil
import zipfile
from datetime import datetime

def create_ankiaddon():
    # 現在のﾃﾞｨﾚｸﾄﾘを取得
    current_dir = os.getcwd()

    today = datetime.today().strftime('%Y%m%d')

    # Zipﾌｧｲﾙ名
    zip_name = f'addon_{today}.zip'

    # Zipﾌｧｲﾙを作成
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_dir):
            # __pycache__ ﾌｫﾙﾀﾞと親ﾃﾞｨﾚｸﾄﾘを除外
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                # meta.json ﾌｧｲﾙとZipﾌｧｲﾙ自体を除外
                if file != 'meta.json' and file != zip_name:
                    zipf.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file),
                                                current_dir))  # 親ﾃﾞｨﾚｸﾄﾘ名を除去

    # 拡張子を .ankiaddon に変更
    os.rename(zip_name, f'addon_{today}.ankiaddon')

# ｽｸﾘﾌﾟﾄを実行
create_ankiaddon()