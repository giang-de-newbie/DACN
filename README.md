# Personal Schedule Assistant

Personal Schedule Assistant là một ứng dụng desktop nhỏ giúp người dùng quản lý lịch cá nhân bằng tiếng Việt. Ứng dụng trích xuất tên sự kiện, thời gian, địa điểm và thiết lập nhắc nhở bằng một pipeline NLP kết hợp rule-based và NER.

**Status:** Production Ready

## Tóm tắt

- Ngôn ngữ: Python 3.8+
- Mục đích: Quản lý sự kiện & nhắc nhở cá nhân với đầu vào tiếng Việt tự do
- Giao diện: Tkinter (desktop)
- Lưu trữ: SQLite (file trong `data/`)

## Tính năng chính

- Nhập sự kiện bằng tiếng Việt tự do
- Trích xuất: tên sự kiện, thời gian, địa điểm, nhắc nhở
- Hỗ trợ thời gian tương đối: "trong X phút/giờ nữa"
- Thêm / Sửa / Xóa / Tìm kiếm sự kiện
- Hệ thống nhắc nhở chạy nền

## Lấy mã nguồn

Bạn có thể lấy mã nguồn bằng 1 trong 2 cách:

1) Clone bằng Git (khuyến nghị nếu bạn muốn cập nhật dễ dàng):

```bash
git clone https://github.com/giang-de-newbie/DACN.git
cd DACN
```

2) Tải ZIP từ trang GitHub: mở https://github.com/giang-de-newbie/DACN → Code → Download ZIP → giải nén.

## Yêu cầu

- Python 3.8 hoặc mới hơn
- pip
- (Tùy chọn) Git

Lưu ý: một số package NLP (ví dụ `underthesea`) có thể cần công cụ biên dịch (build tools). Trên Windows, cài Visual C++ Build Tools nếu cần.

## Cài đặt (bước-dần theo mọi hệ điều hành)

Hướng dẫn sau phù hợp cho người dùng Windows/macOS/Linux.

1) Tạo môi trường ảo (khuyến nghị)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Cập nhật pip và cài dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3) (Nếu cần) Nếu `underthesea` hoặc package khác báo lỗi biên dịch, cài đặt các build tools tương ứng:

- Windows: Visual C++ Build Tools
- Ubuntu/Debian: `sudo apt-get install build-essential` + các header Python

## Chạy ứng dụng

Trong môi trường ảo đã kích hoạt:

```bash
python app.py
```

Ứng dụng mở cửa sổ GUI để quản lý sự kiện. File database sẽ được tạo tự động trong thư mục `data/`.

## Chạy bộ test cơ bản

```bash
python tests/test.py
```

## Cấu trúc dự án

```
DACN/
├── app.py
├── config.py
├── requirements.txt
├── nlp/
├── database/
├── reminder/
├── ui/
├── tests/
└── data/
```

## Các lưu ý vận hành

- Mặc định ứng dụng dùng múi giờ Asia/Ho_Chi_Minh (UTC+7). Thay đổi trong `config.py` nếu cần.
- Trên Windows ứng dụng sử dụng `winsound` để phát âm thanh nhắc nhở; bạn có thể thay đổi phần này nếu chạy trên Linux/macOS.

## Liên hệ

Phát triển bởi: Phạm Trà Trường Giang — giangphamtratuong@gmail.com

---

