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

## Về Project

Personal Schedule Assistant được phát triển để giải quyết bài toán quản lý lịch trình cá nhân với giao diện tiếng Việt. Thay vì nhập từng trường (sự kiện, thời gian, địa điểm, nhắc nhở), ứng dụng cho phép người dùng nhập dạng tự do như "Nhắc tôi họp nhóm lúc 10h sáng mai ở phòng 302, nhắc trước 15 phút" và tự động trích xuất các thông tin.

Ứng dụng sử dụng một pipeline NLP hybrid gồm 5 thành phần:
1. **Preprocessor**: chuẩn hóa text, mở rộng viết tắt
2. **EntityExtractor**: nhận diện thực thể TIME, LOCATION bằng NER (underthesea)
3. **RuleExtractor**: trích xuất từ khóa sự kiện, nhắc nhở, vị trí bằng regex
4. **TimeParser**: phân tích thời gian tương đối (mai, trong X phút, thứ 2 tới) và chuẩn hóa
5. **NLPEngine**: hợp nhất kết quả, kiểm tra tính hợp lệ, tính confidence score

Database sử dụng SQLite với WAL mode để xử lý concurrent access, và hệ thống nhắc nhở chạy trong background thread để kiểm tra sự kiện mỗi 60 giây.

## Cấu trúc dự án

```
DACN/
├── app.py                           # File khởi động ứng dụng chính
├── config.py                        # Cấu hình toàn cục (timezone, database path, etc.)
├── requirements.txt                 # Danh sách Python dependencies
├── nlp/                             # Module xử lý NLP
│   ├── preprocessor.py              # Tiền xử lý text (chuẩn hóa, mở rộng viết tắt)
│   ├── entity_extractor.py          # Nhận diện thực thể (NER) bằng underthesea + regex
│   ├── rule_extractor.py            # Trích xuất theo rule (từ khóa, nhắc nhở, vị trí)
│   ├── time_parser.py               # Phân tích thời gian (tương đối & tuyệt đối)
│   └── nlp_engine.py                # Tích hợp toàn bộ pipeline NLP
├── database/                        # Module quản lý database
│   └── db_manager.py                # SQLite CRUD operations, WAL mode
├── reminder/                        # Module hệ thống nhắc nhở
│   └── reminder_service.py          # Background thread kiểm tra & phát âm báo
├── ui/                              # Module giao diện người dùng
│   └── window.py                    # GUI Tkinter (thêm, sửa, xóa, tìm kiếm sự kiện)
├── tests/                           # Module kiểm thử
│   └── test.py                      # Bộ test case kiểm tra NLP accuracy
├── data/                            # Thư mục chứa file database
│   └── events.db                    # SQLite database (được tạo tự động khi chạy)
└── docs/                            # Tài liệu bổ sung
    └── do_an_chuyen_nganh.txt       # Tài liệu yêu cầu / đề tài
```

## Các lưu ý vận hành

- Mặc định ứng dụng dùng múi giờ Asia/Ho_Chi_Minh (UTC+7). Thay đổi trong `config.py` nếu cần.
- Trên Windows ứng dụng sử dụng `winsound` để phát âm thanh nhắc nhở; bạn có thể thay đổi phần này nếu chạy trên Linux/macOS.

## Liên hệ

Phát triển bởi: Phạm Trà Trường Giang — giangphamtratuong@gmail.com

---

