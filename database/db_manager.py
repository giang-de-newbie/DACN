"""
Database Manager - Quản lý SQLite database
"""
import sqlite3
import json
from datetime import datetime
from config import DB_PATH


class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.timeout = 30  # Timeout 30 giây
        self.init_database()

    def get_connection(self):
        """Tạo kết nối đến database với timeout"""
        conn = sqlite3.connect(self.db_path, timeout=self.timeout, check_same_thread=False)
        # Sử dụng WAL mode để tránh locking
        conn.execute('PRAGMA journal_mode=WAL')
        return conn

    def init_database(self):
        """Khởi tạo database và bảng events"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                location TEXT,
                reminder_minutes INTEGER DEFAULT 15,
                is_notified INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def add_event(self, event_data):
        """
        Thêm sự kiện mới
        event_data: dict {event, start_time, end_time, location, reminder_minutes}
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            now = datetime.now().isoformat()

            cursor.execute('''
                INSERT INTO events (event, start_time, end_time, location, reminder_minutes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data['event'],
                event_data['start_time'],
                event_data.get('end_time'),
                event_data.get('location'),
                event_data.get('reminder_minutes', 15),
                now,
                now
            ))

            event_id = cursor.lastrowid
            conn.commit()
            return event_id
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                raise Exception(f"Database bị khóa, vui lòng thử lại. Chi tiết: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def get_event(self, event_id):
        """Lấy thông tin 1 sự kiện"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(cursor, row)
        return None

    def get_all_events(self):
        """Lấy tất cả sự kiện"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Default ordering: newest added first (created_at desc)
            # Use datetime(created_at) to ensure correct lexical datetime ordering
            cursor.execute('SELECT * FROM events ORDER BY datetime(created_at) DESC')
            rows = cursor.fetchall()
            
            return [self._row_to_dict(cursor, row) for row in rows]
        finally:
            if conn:
                conn.close()

    def update_event(self, event_id, event_data):
        """Cập nhật sự kiện"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            now = datetime.now().isoformat()

            cursor.execute('''
                UPDATE events 
                SET event = ?, start_time = ?, end_time = ?, location = ?, 
                    reminder_minutes = ?, updated_at = ?
                WHERE id = ?
            ''', (
                event_data['event'],
                event_data['start_time'],
                event_data.get('end_time'),
                event_data.get('location'),
                event_data.get('reminder_minutes', 15),
                now,
                event_id
            ))

            conn.commit()
        finally:
            if conn:
                conn.close()

    def delete_event(self, event_id):
        """Xóa sự kiện"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()
        finally:
            if conn:
                conn.close()

    def search_events(self, keyword):
        """Tìm kiếm sự kiện theo từ khóa"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM events 
                WHERE event LIKE ? OR location LIKE ?
                ORDER BY start_time
            ''', (f'%{keyword}%', f'%{keyword}%'))

            rows = cursor.fetchall()
            return [self._row_to_dict(cursor, row) for row in rows]
        finally:
            if conn:
                conn.close()

    def get_pending_reminders(self):
        """Lấy các sự kiện cần nhắc nhở"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM events 
                WHERE is_notified = 0
                ORDER BY start_time
            ''')

            rows = cursor.fetchall()
            return [self._row_to_dict(cursor, row) for row in rows]
        finally:
            if conn:
                conn.close()

    def mark_as_notified(self, event_id):
        """Đánh dấu đã nhắc nhở"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('UPDATE events SET is_notified = 1 WHERE id = ?', (event_id,))
            conn.commit()
        finally:
            if conn:
                conn.close()

    def _row_to_dict(self, cursor, row):
        """Chuyển row thành dictionary"""
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    def export_to_json(self, filepath):
        """Xuất dữ liệu ra file JSON"""
        events = self.get_all_events()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        return True

    def import_from_json(self, filepath):
        """Nhập dữ liệu từ file JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            events = json.load(f)

        for event in events:
            # Bỏ qua id, created_at, updated_at
            event_data = {
                'event': event['event'],
                'start_time': event['start_time'],
                'end_time': event.get('end_time'),
                'location': event.get('location'),
                'reminder_minutes': event.get('reminder_minutes', 15)
            }
            self.add_event(event_data)

        return True