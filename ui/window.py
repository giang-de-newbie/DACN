"""
Giao diện chính - PHIÊN BẢN CẢI TIẾN
Xử lý lỗi tốt hơn, UX được cải thiện, âm thanh nhắc nhở
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import pytz
import winsound  # Cho âm thanh trên Windows
import sys

class MainWindow:
    def __init__(self, nlp_engine, db_manager, reminder_service):
        self.nlp_engine = nlp_engine
        self.db = db_manager
        self.reminder = reminder_service
        self.tz = pytz.timezone('Asia/Ho_Chi_Minh')

        # Tạo cửa sổ chính
        self.root = tk.Tk()
        self.root.title("Trợ lý Quản lý Lịch trình Cá nhân")
        self.root.geometry("950x750")

        # Set callback cho reminder
        self.reminder.callback = self.show_reminder_popup

        self.create_widgets()
        self.load_events()

        # Bind event đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Tạo các widget giao diện"""
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="📅 Trợ lý Quản lý Lịch trình",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=20)

        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section - CẢI TIẾN
        input_frame = tk.LabelFrame(
            main_frame,
            text="📝 Nhập sự kiện bằng tiếng Việt",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Hướng dẫn chi tiết hơn
        help_text = (
            "VD: Nhắc tôi họp nhóm lúc 10h sáng mai ở phòng 302, nhắc trước 15 phút\n"
            "     Meeting với khách hàng 14:30 thứ Hai tới tại văn phòng\n"
            "     Deadline nộp báo cáo ngày 25/11 lúc 9h"
        )
        tk.Label(
            input_frame,
            text=help_text,
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        ).pack(anchor=tk.W)

        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=3,
            font=("Arial", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.input_text.pack(fill=tk.X, pady=(5, 10))

        # Character counter
        self.char_counter = tk.Label(input_frame, text="0/500 ký tự", font=("Arial", 9), fg="gray")
        self.char_counter.pack(anchor=tk.E)
        self.input_text.bind('<KeyRelease>', self.update_char_counter)

        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(fill=tk.X)

        self.add_btn = tk.Button(
            btn_frame,
            text="➕ Thêm sự kiện",
            command=self.add_event,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Xóa",
            command=self.clear_input,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED
        )
        self.clear_btn.pack(side=tk.LEFT)

        # Status label
        self.status_label = tk.Label(
            btn_frame,
            text="✅ Sẵn sàng",
            font=("Arial", 10),
            fg="#27ae60"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Search section
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.search_events())

        tk.Button(
            search_frame,
            text="Tìm",
            command=self.search_events,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            padx=15,
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            search_frame,
            text="Hiện tất cả",
            command=self.load_events,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            padx=15,
            relief=tk.RAISED
        ).pack(side=tk.LEFT)

        # Event count
        self.event_count_label = tk.Label(
            search_frame,
            text="Tổng: 0 sự kiện",
            font=("Arial", 10),
            fg="gray"
        )
        self.event_count_label.pack(side=tk.RIGHT, padx=10)

        # Events table
        table_frame = tk.LabelFrame(
            main_frame,
            text="📋 Danh sách sự kiện",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview với style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        columns = ("ID", "Sự kiện", "Thời gian", "Địa điểm", "Nhắc trước", "Trạng thái")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Define columns
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Sự kiện", width=200)
        self.tree.column("Thời gian", width=150, anchor=tk.CENTER)
        self.tree.column("Địa điểm", width=150)
        self.tree.column("Nhắc trước", width=100, anchor=tk.CENTER)
        self.tree.column("Trạng thái", width=100, anchor=tk.CENTER)

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)

        # Bind double-click
        self.tree.bind('<Double-1>', lambda e: self.view_event_details())

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame2 = tk.Frame(main_frame)
        btn_frame2.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            btn_frame2,
            text="👁️ Xem chi tiết",
            command=self.view_event_details,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=20,
            pady=5,
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame2,
            text="❌ Xóa",
            command=self.delete_event,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=20,
            pady=5,
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame2,
            text="🔄 Làm mới",
            command=self.load_events,
            bg="#34495e",
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            padx=20,
            pady=5,
            relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame2,
            text="📥 Xuất JSON",
            command=self.export_json,
            bg="#16a085",
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            padx=20,
            pady=5,
            relief=tk.RAISED
        ).pack(side=tk.RIGHT)

    def update_char_counter(self, event=None):
        """Cập nhật bộ đếm ký tự"""
        text = self.input_text.get(1.0, tk.END).strip()
        count = len(text)

        color = "gray"
        if count > 500:
            color = "red"
        elif count > 400:
            color = "orange"

        self.char_counter.config(text=f"{count}/500 ký tự", fg=color)

    def update_status(self, message, color="#27ae60"):
        """Cập nhật status label"""
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "loading": "⏳"
        }

        icon = ""
        for key, symbol in icons.items():
            if key in message.lower():
                icon = symbol
                break

        self.status_label.config(text=f"{icon} {message}", fg=color)
        self.root.update()

    def clear_input(self):
        """Xóa input"""
        self.input_text.delete(1.0, tk.END)
        self.update_char_counter()

    def add_event(self):
        """Thêm sự kiện mới - CẢI TIẾN"""
        text = self.input_text.get(1.0, tk.END).strip()

        if not text:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập thông tin sự kiện!")
            return

        if len(text) > 500:
            messagebox.showerror("❌ Lỗi", "Nội dung quá dài! Tối đa 500 ký tự.")
            return

        # Hiển thị trạng thái đang xử lý
        self.update_status("Đang xử lý...", "#f39c12")
        self.add_btn.config(state=tk.DISABLED)

        try:
            # Xử lý NLP
            result = self.nlp_engine.extract(text)

            # Kiểm tra lỗi
            if not result['valid']:
                error_msg = "Không thể trích xuất thông tin:\n\n"
                error_msg += "\n".join(f"• {err}" for err in result.get('errors', ['Lỗi không xác định']))
                messagebox.showerror("❌ Lỗi", error_msg)
                self.update_status("Lỗi trích xuất", "#e74c3c")
                return

            # Hiển thị warnings nếu có
            if result.get('warnings'):
                warning_msg = "⚠️ Cảnh báo:\n\n"
                warning_msg += "\n".join(f"• {warn}" for warn in result['warnings'])
                warning_msg += "\n\nBạn có muốn tiếp tục?"

                if not messagebox.askyesno("⚠️ Cảnh báo", warning_msg):
                    self.update_status("Đã hủy", "#95a5a6")
                    return

            # Lưu vào database
            event_id = self.db.add_event(result)

            # Hiển thị thông báo thành công
            success_msg = f"✅ Đã thêm sự kiện:\n\n"
            success_msg += f"📌 {result['event']}\n"
            success_msg += f"🕒 {self.format_datetime(result['start_time'])}\n"
            if result['location']:
                success_msg += f"📍 {result['location']}\n"
            success_msg += f"⏰ Nhắc trước {result['reminder_minutes']} phút"

            messagebox.showinfo("✅ Thành công", success_msg)

            self.clear_input()
            self.load_events()
            self.update_status("Thêm thành công!", "#27ae60")

        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể lưu sự kiện:\n{str(e)}")
            self.update_status("Lỗi hệ thống", "#e74c3c")

        finally:
            self.add_btn.config(state=tk.NORMAL)

    def format_datetime(self, dt_str):
        """Format datetime string"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return dt_str

    def load_events(self):
        """Tải danh sách sự kiện - CẢI TIẾN"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu mới
        events = self.db.get_all_events()

        # Sắp xếp events theo thứ tự thêm gần nhất (created_at desc) - nếu không có created_at thì theo id desc
        try:
            events = sorted(
                events,
                key=lambda e: e.get('created_at') or e.get('id'),
                reverse=True
            )
        except Exception:
            # Nếu có lỗi khi sắp xếp thì giữ nguyên thứ tự lấy từ DB
            pass

        now = datetime.now(self.tz)

        for event in events:
            # Format thời gian
            time_str = self.format_datetime(event['start_time'])

            # Xác định trạng thái
            try:
                event_dt = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                if event.get('is_notified', 0) == 1:
                    status = "✅ Đã nhắc"
                    tag = 'notified'
                elif event_dt < now:
                    status = "⏰ Đã qua"
                    tag = 'past'
                else:
                    status = "📅 Sắp tới"
                    tag = 'upcoming'
            except:
                status = "❓ Không rõ"
                tag = 'unknown'

            # Insert vào tree với tag
            item_id = self.tree.insert("", tk.END, values=(
                event['id'],
                event['event'],
                time_str,
                event['location'] or "",
                f"{event['reminder_minutes']} phút",
                status
            ), tags=(tag,))

        # Cấu hình màu cho các tag
        self.tree.tag_configure('upcoming', foreground='#27ae60')
        self.tree.tag_configure('past', foreground='#95a5a6')
        self.tree.tag_configure('notified', foreground='#3498db')

        # Cập nhật số lượng
        self.event_count_label.config(text=f"Tổng: {len(events)} sự kiện")

    def view_event_details(self):
        """Xem chi tiết sự kiện"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("ℹ️ Thông báo", "Vui lòng chọn sự kiện để xem chi tiết!")
            return

        item = self.tree.item(selected[0])
        event_id = item['values'][0]

        # Lấy thông tin chi tiết từ database
        event = self.db.get_event(event_id)

        if not event:
            messagebox.showerror("❌ Lỗi", "Không tìm thấy sự kiện!")
            return

        # Tạo cửa sổ chi tiết
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Chi tiết: {event['event']}")
        detail_window.geometry("500x400")
        detail_window.transient(self.root)
        detail_window.grab_set()

        # Nội dung
        frame = tk.Frame(detail_window, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="📋 CHI TIẾT SỰ KIỆN", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        info_frame = tk.Frame(frame, bg="white", relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        info_text = f"""
📌 Sự kiện: {event['event']}

🕒 Thời gian: {self.format_datetime(event['start_time'])}

📍 Địa điểm: {event['location'] or 'Không có'}

⏰ Nhắc nhở: Trước {event['reminder_minutes']} phút

📝 Trạng thái: {'Đã nhắc' if event.get('is_notified', 0) == 1 else 'Chưa nhắc'}

📅 Tạo lúc: {self.format_datetime(event['created_at'])}

🔄 Cập nhật: {self.format_datetime(event['updated_at'])}
        """

        tk.Label(
            info_frame,
            text=info_text.strip(),
            font=("Arial", 11),
            justify=tk.LEFT,
            bg="white"
        ).pack(padx=20, pady=20)

        tk.Button(
            frame,
            text="Đóng",
            command=detail_window.destroy,
            bg="#3498db",
            fg="white",
            font=("Arial", 11),
            padx=30,
            pady=8
        ).pack()

    def search_events(self):
        """Tìm kiếm sự kiện"""
        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_events()
            return

        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tìm kiếm
        events = self.db.search_events(keyword)

        if not events:
            messagebox.showinfo("ℹ️ Thông báo", f"Không tìm thấy sự kiện nào với từ khóa '{keyword}'")
            return

        now = datetime.now(self.tz)

        for event in events:
            time_str = self.format_datetime(event['start_time'])

            try:
                event_dt = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                if event.get('is_notified', 0) == 1:
                    status = "✅ Đã nhắc"
                elif event_dt < now:
                    status = "⏰ Đã qua"
                else:
                    status = "📅 Sắp tới"
            except:
                status = "❓ Không rõ"

            self.tree.insert("", tk.END, values=(
                event['id'],
                event['event'],
                time_str,
                event['location'] or "",
                f"{event['reminder_minutes']} phút",
                status
            ))

        self.event_count_label.config(text=f"Tìm thấy: {len(events)} sự kiện")

    def delete_event(self):
        """Xóa sự kiện"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn sự kiện cần xóa!")
            return

        item = self.tree.item(selected[0])
        event_name = item['values'][1]

        # Xác nhận
        if messagebox.askyesno("❓ Xác nhận", f"Bạn có chắc muốn xóa sự kiện:\n\n'{event_name}'?"):
            event_id = item['values'][0]

            try:
                self.db.delete_event(event_id)
                messagebox.showinfo("✅ Thành công", "Đã xóa sự kiện!")
                self.load_events()
                self.update_status("Đã xóa sự kiện", "#27ae60")
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể xóa sự kiện:\n{str(e)}")

    def export_json(self):
        """Xuất dữ liệu ra JSON"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        if filepath:
            try:
                self.db.export_to_json(filepath)
                messagebox.showinfo("✅ Thành công", f"Đã xuất {len(self.db.get_all_events())} sự kiện ra:\n{filepath}")
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể xuất dữ liệu:\n{str(e)}")

    def play_reminder_sound(self):
        """Phát âm thanh nhắc nhở"""
        try:
            if sys.platform == 'win32':
                # Windows
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                # macOS/Linux - dùng bell
                self.root.bell()
        except:
            # Fallback
            self.root.bell()

    def show_reminder_popup(self, event, message):
        """Hiển thị popup nhắc nhở - CẢI TIẾN"""
        # Phát âm thanh
        self.play_reminder_sound()

        popup = tk.Toplevel(self.root)
        popup.title("🔔 Nhắc nhở sự kiện")
        popup.geometry("450x300")
        popup.configure(bg="#ecf0f1")

        # Đưa popup lên trên cùng
        popup.attributes('-topmost', True)
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="🔔 NHẮC NHỞ SỰ KIỆN",
            font=("Arial", 18, "bold"),
            bg="#ecf0f1",
            fg="#e74c3c"
        ).pack(pady=20)

        msg_frame = tk.Frame(popup, bg="white", relief=tk.SOLID, borderwidth=2)
        msg_frame.pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)

        tk.Label(
            msg_frame,
            text=message,
            font=("Arial", 12),
            bg="white",
            justify=tk.LEFT,
            anchor=tk.W
        ).pack(padx=20, pady=20)

        btn_frame = tk.Frame(popup, bg="#ecf0f1")
        btn_frame.pack(pady=(0, 20))

        tk.Button(
            btn_frame,
            text="✅ Đã hiểu",
            command=popup.destroy,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=40,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="⏰ Nhắc lại sau 5 phút",
            command=lambda: self.snooze_reminder(event, popup),
            bg="#f39c12",
            fg="white",
            font=("Arial", 11),
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        # Tự động đóng sau 30 giây
        popup.after(30000, popup.destroy)

    def snooze_reminder(self, event, popup):
        """Nhắc lại sau 5 phút"""
        popup.destroy()
        # TODO: Implement snooze logic (tùy chọn nâng cao)
        messagebox.showinfo("ℹ️ Thông báo", "Chức năng 'Nhắc lại' đang phát triển!")

    def on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        if messagebox.askokcancel("❓ Thoát", "Bạn có chắc muốn thoát ứng dụng?"):
            self.reminder.stop()
            self.root.destroy()

    def run(self):
        """Chạy ứng dụng"""
        # Khởi động reminder service
        self.reminder.start()

        # Run main loop
        self.root.mainloop()

        # Dừng reminder service khi đóng ứng dụng
        self.reminder.stop()