"""
Personal Schedule Assistant - File chính
Ứng dụng quản lý lịch trình cá nhân với xử lý tiếng Việt
"""
import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.insert(0, str(Path(__file__).parent.absolute()))

from nlp.nlp_engine import NLPEngine
from database.db_manager import DatabaseManager
from reminder.reminder_service import ReminderService
from ui.window import MainWindow


def main():
    """Hàm main khởi động ứng dụng"""
    print("=" * 60)
    print("Khởi động Personal Schedule Assistant")
    print("=" * 60)

    # Khởi tạo các component
    print("Đang khởi tạo NLP Engine...")
    nlp_engine = NLPEngine()

    print("Đang khởi tạo Database Manager...")
    db_manager = DatabaseManager()

    print("Đang khởi tạo Reminder Service...")
    reminder_service = ReminderService()

    print("Đang khởi tạo giao diện...")
    app = MainWindow(nlp_engine, db_manager, reminder_service)

    print("Ứng dụng đã sẵn sàng!")
    print("=" * 60)

    # Chạy ứng dụng
    app.run()


if __name__ == "__main__":
    main()
