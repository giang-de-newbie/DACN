# Personal Schedule Assistant

Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).
**Status:** Production Ready

## Yêu cầu

- Python 3.8+
- Windows 10/11 (hoặc tương đương)
- pip (Python package manager)
## Cách chạy chương trình

1. Mở PowerShell hoặc Command Prompt và điều hướng đến thư mục dự án:

```powershell
cd d:\Python\PycharmProjects\DACN
```
2. Kích hoạt môi trường ảo (nếu có):

```powershell
.venv\Scripts\Activate.ps1
```
3. Cài dependencies nếu cần:

```powershell
pip install -r requirements.txt
```
4. Chạy ứng dụng chính:

```powershell
.venv\Scripts\python.exe app.py
```
5. Chạy bộ test (tùy chọn):

```powershell
.venv\Scripts\python.exe tests/test.py
```
## Cấu trúc dự án

```
DACN/
├── app.py
├── config.py
├── requirements.txt
├── nlp/
│   ├── preprocessor.py
│   ├── entity_extractor.py
│   ├── rule_extractor.py
│   ├── time_parser.py
│   └── nlp_engine.py
├── database/
│   └── db_manager.py
├── reminder/
│   └── reminder_service.py
├── ui/
│   └── window.py
├── tests/
│   └── test.py
├── data/
│   └── events.db (tạo khi chạy)
└── docs/
    └── do_an_chuyen_nganh.txt
```
## Kiến trúc chính

Ứng dụng sử dụng kiến trúc 5-component cho pipeline NLP:

1. Preprocessor: tiền xử lý và chuẩn hóa văn bản.
2. EntityExtractor: nhận diện thực thể (TIME, LOCATION) bằng NER và regex.
3. RuleExtractor: trích xuất theo quy tắc (từ khóa, nhắc nhở, vị trí).
4. TimeParser: phân tích thời gian (tương đối và tuyệt đối) và chuẩn hóa thành datetime.
5. NLPEngine: hợp nhất kết quả, kiểm tra tính hợp lệ và xuất cấu trúc sự kiện.

## Tính năng

- Nhập sự kiện bằng tiếng Việt tự do.
- Trích xuất tự động: tên sự kiện, thời gian, địa điểm, nhắc nhở.
- Hỗ trợ thời gian tương đối: "trong X phút/giờ nữa".
- Quản lý sự kiện: Thêm, Sửa, Xóa, Tìm kiếm.
- Lưu trữ cục bộ bằng SQLite.
- Hệ thống nhắc nhở tự động.
- Giao diện GUI đơn giản bằng Tkinter.

## Testing

Dự án có bộ test cơ bản tại `tests/test.py`. Chạy bằng Python như phần hướng dẫn ở trên.

## Lưu ý

- Ứng dụng mặc định sử dụng múi giờ Asia/Ho_Chi_Minh (UTC+7).
- Trên Windows ứng dụng sử dụng `winsound` để phát âm thanh nhắc nhở; trên Linux/macOS cần điều chỉnh phần âm thanh.
- Database SQLite được tạo trong thư mục `data/` khi ứng dụng chạy.

## Phiên bản

v1.0

---

Được phát triển bởi: Phạm Trà Trường Giang (3121410168)
# Personal Schedule Assistant# Personal Schedule Assistant



Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).



**Status:** Production Ready | **Last Updated:** November 30, 2025



## Yêu cầu## Yêu cầu



- Python 3.8+- Python 3.8+

- Windows 10/11- Windows 10/11

- pip (Python package manager)- pip (Python package manager)



## Cách chạy chương trình## Cách chạy chương trình



### Bước 1: Mở PowerShell hoặc Command Prompt



Điều hướng đến thư mục dự án:Điều hướng đến thư mục dự án:



```powershell```powershell

cd d:\Python\PycharmProjects\DACNcd d:\Python\PycharmProjects\DACN

``````



### Bước 2: Kích hoạt môi trường ảo (nếu chưa kích hoạt)### Bước 2: Kích hoạt môi trường ảo (nếu chưa kích hoạt)


# Personal Schedule Assistant

Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).

**Status:** Production Ready

## Yêu cầu

- Python 3.8+
- Windows 10/11 (hoặc tương đương)
- pip (Python package manager)

## Cách chạy chương trình

1. Mở PowerShell hoặc Command Prompt và điều hướng đến thư mục dự án:

```powershell
cd d:\Python\PycharmProjects\DACN
```

2. Kích hoạt môi trường ảo (nếu có):

```powershell
.venv\Scripts\Activate.ps1
```

3. Cài dependencies nếu cần:

```powershell
pip install -r requirements.txt
```

4. Chạy ứng dụng chính:

```powershell
.venv\Scripts\python.exe app.py
```

5. Chạy bộ test (tùy chọn):

```powershell
.venv\Scripts\python.exe tests/test.py
```

## Cấu trúc dự án

```
DACN/
├── app.py
├── config.py
├── requirements.txt
├── nlp/
│   ├── preprocessor.py
│   ├── entity_extractor.py
│   ├── rule_extractor.py
│   ├── time_parser.py
│   └── nlp_engine.py
├── database/
│   └── db_manager.py
├── reminder/
│   └── reminder_service.py
├── ui/
│   └── window.py
├── tests/
│   └── test.py
├── data/
│   └── events.db (tạo khi chạy)
└── docs/
    └── do_an_chuyen_nganh.txt
```

## Kiến trúc chính

Ứng dụng sử dụng kiến trúc 5-component cho pipeline NLP:

1. Preprocessor: tiền xử lý và chuẩn hóa văn bản.
2. EntityExtractor: nhận diện thực thể (TIME, LOCATION) bằng NER và regex.
3. RuleExtractor: trích xuất theo quy tắc (từ khóa, nhắc nhở, vị trí).
4. TimeParser: phân tích thời gian (tương đối và tuyệt đối) và chuẩn hóa thành datetime.
5. NLPEngine: hợp nhất kết quả, kiểm tra tính hợp lệ và xuất cấu trúc sự kiện.

## Tính năng

- Nhập sự kiện bằng tiếng Việt tự do.
- Trích xuất tự động: tên sự kiện, thời gian, địa điểm, nhắc nhở.
- Hỗ trợ thời gian tương đối: "trong X phút/giờ nữa".
- Quản lý sự kiện: Thêm, Sửa, Xóa, Tìm kiếm.
- Lưu trữ cục bộ bằng SQLite.
- Hệ thống nhắc nhở tự động.
- Giao diện GUI đơn giản bằng Tkinter.

## Testing

Dự án có bộ test cơ bản tại `tests/test.py`. Chạy bằng Python như phần hướng dẫn ở trên.

## Lưu ý

- Ứng dụng mặc định sử dụng múi giờ Asia/Ho_Chi_Minh (UTC+7).
- Trên Windows ứng dụng sử dụng `winsound` để phát âm thanh nhắc nhở; trên Linux/macOS cần điều chỉnh phần âm thanh.
- Database SQLite được tạo trong thư mục `data/` khi ứng dụng chạy.

## Phiên bản

v1.0

---

Được phát triển bởi: Phạm Trà Trường Giang (3121410168)

- Để chạy trên Linux/macOS, cần chỉnh sửa phần âm thanh trong `ui/window.py`

- Database SQLite tự động được tạo trong thư mục `data/`---

- Múi giờ mặc định: **Asia/Ho_Chi_Minh (UTC+7)**

Được phát triển như bài báo cáo chuyên ngành.

## Phiên bản hiện tại

**v1.0** - Phiên bản đầy đủ với NLP + UI + Database + Reminder
