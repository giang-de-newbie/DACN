"""
Reminder Service - Hệ thống nhắc nhở tự động
Chạy thread riêng, kiểm tra mỗi 60 giây
"""
import threading
import time
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from config import REMINDER_CHECK_INTERVAL
import pytz


class ReminderService:
    def __init__(self, callback=None):
        self.db = DatabaseManager()
        self.callback = callback  # Hàm callback để hiển thị popup
        self.is_running = False
        self.thread = None
        self.tz = pytz.timezone('Asia/Ho_Chi_Minh')

    def start(self):
        """Khởi động service"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._check_loop, daemon=True)
            self.thread.start()
            print("Reminder Service started")

    def stop(self):
        """Dừng service"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        print("Reminder Service stopped")

    def _check_loop(self):
        """Vòng lặp kiểm tra"""
        while self.is_running:
            try:
                self._check_reminders()
            except Exception as e:
                print(f"Error in reminder check: {e}")

            time.sleep(REMINDER_CHECK_INTERVAL)

    def _check_reminders(self):
        """Kiểm tra và gửi nhắc nhở"""
        # Lấy tất cả sự kiện chưa nhắc
        events = self.db.get_pending_reminders()

        now = datetime.now(self.tz)

        for event in events:
            try:
                # Parse start_time
                start_time_str = event['start_time']

                # Xử lý timezone
                if '+' in start_time_str or 'Z' in start_time_str:
                    start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                else:
                    start_time = datetime.fromisoformat(start_time_str)
                    start_time = self.tz.localize(start_time)

                # Tính thời gian nhắc nhở
                reminder_minutes = event.get('reminder_minutes', 15)
                reminder_time = start_time - timedelta(minutes=reminder_minutes)

                # Kiểm tra xem đã đến giờ nhắc chưa
                if now >= reminder_time:
                    # Gửi nhắc nhở
                    self._send_reminder(event)

                    # Đánh dấu đã nhắc
                    self.db.mark_as_notified(event['id'])

            except Exception as e:
                print(f"Error processing event {event['id']}: {e}")

    def _send_reminder(self, event):
        """Gửi nhắc nhở (gọi callback hoặc in ra)"""
        message = self._format_reminder_message(event)

        if self.callback:
            self.callback(event, message)
        else:
            print(f"\n{'=' * 60}")
            print("🔔 NHẮC NHỞ SỰ KIỆN")
            print(message)
            print('=' * 60)

    def _format_reminder_message(self, event):
        """Format thông điệp nhắc nhở"""
        lines = []
        lines.append(f"Sự kiện: {event['event']}")

        # Format thời gian
        try:
            start_time_str = event['start_time']
            if '+' in start_time_str or 'Z' in start_time_str:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            else:
                start_time = datetime.fromisoformat(start_time_str)

            lines.append(f"Thời gian: {start_time.strftime('%d/%m/%Y %H:%M')}")
        except:
            lines.append(f"Thời gian: {event['start_time']}")

        if event.get('location'):
            lines.append(f"Địa điểm: {event['location']}")

        reminder_minutes = event.get('reminder_minutes', 15)
        lines.append(f"Nhắc trước: {reminder_minutes} phút")

        return "\n".join(lines)