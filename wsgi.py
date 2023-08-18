import os

from dotenv import load_dotenv

# 手动设置环境变量并导入程序实例

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app
