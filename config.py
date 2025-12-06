"""
Cấu hình chung cho ứng dụng Personal Schedule Assistant
Chạy trên Windows
"""
from pathlib import Path

# Đường dẫn
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'events.db'

# Tạo thư mục data nếu chưa có
DATA_DIR.mkdir(exist_ok=True)

# Cấu hình ứng dụng
REMINDER_CHECK_INTERVAL = 60  # Kiểm tra mỗi 60 giây
NLP_CONFIDENCE_THRESHOLD = 0.8  # Độ tin cậy tối thiểu
TIMEZONE = 'Asia/Ho_Chi_Minh'
