# Personal Schedule Assistant# Personal Schedule Assistant



Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).Ứng dụng quản lý lịch trình cá nhân với tính năng xử lý tiếng Việt tự nhiên (NLP).



**Status:** Production Ready | **Last Updated:** November 30, 2025**Status:** Production Ready | **Last Updated:** December 1, 2025



## Yêu cầu## Yêu cầu



- Python 3.8+- Python 3.8+

- Windows 10/11- Windows 10/11

- pip (Python package manager)- pip (Python package manager)



## Cách chạy chương trình## Cách chạy chương trình



### Bước 1: Mở PowerShell hoặc Command Prompt### Bước 1: Mở PowerShell hoặc Command Prompt



Điều hướng đến thư mục dự án:Điều hướng đến thư mục dự án:



```powershell```powershell

cd d:\Python\PycharmProjects\DACNcd d:\Python\PycharmProjects\DACN

``````



### Bước 2: Kích hoạt môi trường ảo (nếu chưa kích hoạt)### Bước 2: Kích hoạt môi trường ảo (nếu chưa kích hoạt)



```powershell```powershell

.venv\Scripts\Activate.ps1.venv\Scripts\Activate.ps1

``````



**Lưu ý:** Nếu gặp lỗi về execution policy, chạy:**Lưu ý:** Nếu gặp lỗi về execution policy, chạy:

```powershell```powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUserSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

``````



### Bước 3: Chạy các chế độ khác nhau### Bước 3: Chạy các chế độ khác nhau



#### A. Chạy bài kiểm tra NLP (Test Suite) - 30 test cases#### **A. Chạy bài kiểm tra NLP (Test Suite) - 30 test cases**



```powershell```powershell

.venv\Scripts\python.exe tests/test.py.venv\Scripts\python.exe tests/test.py

``````



**Kết quả mong đợi:****Kết quả mong đợi:**

- Chạy 30 test cases với các vào khác nhau- Chạy 30 test cases với các vào khác nhau

- Hiển thị độ chính xác (accuracy) >= 80%- Hiển thị độ chính xác (accuracy) >= 80%

- Thời gian chạy: ~2-5 giây- Thời gian chạy: ~2-5 giây



**Ví dụ output:****Ví dụ output:**

``````

========================================================================================================================

KIEM TRA DO CHINH XAC NLP ENGINEKIEM TRA DO CHINH XAC NLP ENGINE

========================================================================================================================

Tong so test cases: 30Tong so test cases: 30



[Test 1/30] Nhac toi hop nhom luc 10 gio sang mai...[Test 1/30] Nhac toi hop nhom luc 10 gio sang mai...

  PASS  PASS

......

[Test 30/30] Tong ket nam hoc vao 9 gio sang...[Test 30/30] Tong ket nam hoc vao 9 gio sang...

  PASS  PASS



TONG KET:TONG KET:

Tong tests: 30Tong tests: 30

Passed: 30Passed: 30

Failed: 0Failed: 0

Accuracy: 100.00%Accuracy: 100.00%

========================================================================================================================

KET QUA: DAT YEU CAU (>= 80%)KET QUA: DAT YEU CAU (>= 80%)

``````



#### B. Chạy ứng dụng chính (Main Application)#### **B. Chạy ứng dụng chính (Main Application)**



```powershell```powershell

.venv\Scripts\python.exe app.py.venv\Scripts\python.exe app.py

``````



**Chức năng:****Chức năng:**

- Khởi tạo NLP Engine, Database Manager, Reminder Service- Khởi tạo NLP Engine, Database Manager, Reminder Service

- Mở giao diện Tkinter để nhập lịch trình- Mở giao diện Tkinter để nhập lịch trình

- Tự động kiểm tra và gửi nhắc nhở mỗi 60 giây- Tự động kiểm tra và gửi nhắc nhở mỗi 60 giây

- Lưu trữ sự kiện vào SQLite database- Lưu trữ sự kiện vào SQLite database



#### C. Chạy tests cụ thể (nếu cần)#### **C. Chạy tests cụ thể (nếu cần)**



```powershell```powershell

.venv\Scripts\python.exe -m pytest tests/test.py -v.venv\Scripts\python.exe -m pytest tests/test.py -v

``````



### Bước 4: Dừng chương trình### Bước 4: Dừng chương trình



- **Test:** Chờ hoàn thành (tự động dừng)- **Test:** Chờ hoàn thành (tự động dừng)

- **App:** Bấm `Ctrl+C` trong PowerShell hoặc đóng cửa sổ ứng dụng- **App:** Bấm `Ctrl+C` trong PowerShell hoặc đóng cửa sổ ứng dụng



## Cài đặt lại Dependencies (nếu cần)## Cài đặt lại Dependencies (nếu cần)



Nếu gặp lỗi import modules, cài đặt lại:Nếu gặp lỗi import modules, cài đặt lại:



```powershell```powershell

pip install -r requirements.txtpip install -r requirements.txt

``````



Hoặc cài đặt thủ công:Hoặc cài đặt thủ công:



```powershell```powershell

pip install underthesea pytz python-dateutilpip install underthesea pytz python-dateutil

``````



## Cấu trúc Modules## Cấu trúc Modules



### NLP Engine (5 thành phần)### NLP Engine (5 thành phần)



1. **Preprocessor** - Chuẩn hóa text1. **Preprocessor** - Chuẩn hóa text

   - Loại bỏ khoảng trắng thừa   - Loại bỏ khoảng trắng thừa

   - Mở rộng viết tắt (k → không, dc → được)   - Mở rộng viết tắt (k → không, dc → được)

   - Chuẩn hóa định dạng thời gian (10h → 10 giờ)   - Chuẩn hóa định dạng thời gian (10h → 10 giờ)



2. **EntityExtractor** - Trích xuất thực thể2. **EntityExtractor** - Trích xuất thực thể

   - Sử dụng NER (underthesea) để nhận diện TIME, LOCATION   - Sử dụng NER (underthesea) để nhận diện TIME, LOCATION

   - Fallback regex patterns   - Fallback regex patterns



3. **RuleExtractor** - Trích xuất theo quy tắc3. **RuleExtractor** - Trích xuất theo quy tắc

   - 20+ từ khóa sự kiện (họp, thi, sinh nhật, etc.)   - 20+ từ khóa sự kiện (họp, thi, sinh nhật, etc.)

   - Regex patterns cho thời gian nhắc nhở, vị trí   - Regex patterns cho thời gian nhắc nhở, vị trí



4. **TimeParser** - Phân tích thời gian4. **TimeParser** - Phân tích thời gian

   - Xử lý thời gian tương đối (mai, hôm nay, thứ 2 tới)   - Xử lý thời gian tương đối (mai, hôm nay, thứ 2 tới)

   - Chuyển đổi sang ISO datetime format   - Chuyển đổi sang ISO datetime format

   - Timezone Asia/Ho_Chi_Minh   - Timezone Asia/Ho_Chi_Minh



5. **NLPEngine** - Hợp nhất tất cả5. **NLPEngine** - Hợp nhất tất cả

   - Xử lý toàn bộ pipeline   - Xử lý toàn bộ pipeline

   - Kiểm tra tính hợp lệ kết quả   - Kiểm tra tính hợp lệ kết quả

   - Tính độ tin cậy (confidence score)   - Tính độ tin cậy (confidence score)



### Database & Reminder### Database & Reminder



- **DatabaseManager** - SQLite CRUD operations- **DatabaseManager** - SQLite CRUD operations

- **ReminderService** - Background thread kiểm tra nhắc nhở- **ReminderService** - Background thread kiểm tra nhắc nhở



## Cấu trúc dự án## Cấu trúc dự án



``````

DACN/DACN/

├── app.py                      # File khởi động ứng dụng├── app.py                      # File khởi động ứng dụng

├── config.py                   # Cấu hình chung├── config.py                   # Cấu hình chung

├── requirements.txt            # Danh sách dependencies├── requirements.txt            # Danh sách dependencies

├── nlp/├── nlp/

│   ├── __init__.py│   ├── __init__.py

│   ├── preprocessor.py         # Component 1: Tiền xử lý│   ├── preprocessor.py         # Component 1: Tiền xử lý

│   ├── entity_extractor.py     # Component 2: Trích xuất thực thể (NER)│   ├── entity_extractor.py     # Component 2: Trích xuất thực thể (NER)

│   ├── rule_extractor.py       # Component 3: Rule-based extraction│   ├── rule_extractor.py       # Component 3: Rule-based extraction

│   ├── time_parser.py          # Component 4: Phân tích thời gian│   ├── time_parser.py          # Component 4: Phân tích thời gian

│   └── nlp_engine.py           # Component 5: Tích hợp NLP│   └── nlp_engine.py           # Component 5: Tích hợp NLP

├── database/├── database/

│   ├── __init__.py│   ├── __init__.py

│   └── db_manager.py           # Quản lý SQLite database│   └── db_manager.py           # Quản lý SQLite database

├── reminder/├── reminder/

│   ├── __init__.py│   ├── __init__.py

│   └── reminder_service.py     # Hệ thống nhắc nhở│   └── reminder_service.py     # Hệ thống nhắc nhở

├── ui/├── ui/

│   ├── __init__.py│   ├── __init__.py

│   └── window.py               # Giao diện Tkinter│   └── window.py               # Giao diện Tkinter

├── tests/├── tests/

│   ├── __init__.py│   ├── __init__.py

│   └── test.py                 # 30 test cases kiểm tra NLP│   └── test.py                 # 30 test cases kiểm tra NLP

├── data/├── data/

│   └── events.db               # SQLite database (được tạo tự động)│   └── events.db               # SQLite database (được tạo tự động)

└── docs/└── docs/

    └── do_an_chuyen_nganh.txt  # Tài liệu yêu cầu    └── do_an_chuyen_nganh.txt  # Tài liệu yêu cầu

``````



## Kiến trúc NLP## Kiến trúc NLP



Ứng dụng sử dụng kiến trúc **5-component hybrid NLP** để xử lý tiếng Việt:Ứng dụng sử dụng kiến trúc **5-component hybrid NLP** để xử lý tiếng Việt:



1. **Preprocessor**: Tiền xử lý, chuẩn hóa, phân đoạn từ1. **Preprocessor**: Tiền xử lý, chuẩn hóa, phân đoạn từ

2. **EntityExtractor**: Nhận diện TIME, LOCATION bằng NER (underthesea)2. **EntityExtractor**: Nhận diện TIME, LOCATION bằng NER (underthesea)

3. **RuleExtractor**: Trích xuất sự kiện, nhắc nhở bằng regex3. **RuleExtractor**: Trích xuất sự kiện, nhắc nhở bằng regex

4. **TimeParser**: Phân tích thời gian tương đối → datetime tuyệt đối4. **TimeParser**: Phân tích thời gian tương đối → datetime tuyệt đối

5. **NLPEngine**: Tích hợp, validation, xử lý lỗi5. **NLPEngine**: Tích hợp, validation, xử lý lỗi



### Ví dụ:### Ví dụ:



```python```python

from nlp.nlp_engine import NLPEnginefrom nlp.nlp_engine import NLPEngine



engine = NLPEngine()engine = NLPEngine()

result = engine.extract("Nhắc tôi họp nhóm lúc 10h sáng mai ở phòng 302, nhắc trước 15 phút")result = engine.extract("Nhắc tôi họp nhóm lúc 10h sáng mai ở phòng 302, nhắc trước 15 phút")



# Output:# Output:

# {# {

#     'event': 'họp nhóm',#     'event': 'họp nhóm',

#     'start_time': '2025-12-07T10:00:00+07:00',#     'start_time': '2025-12-07T10:00:00+07:00',

#     'location': 'phòng 302',#     'location': 'phòng 302',

#     'reminder_minutes': 15,#     'reminder_minutes': 15,

#     'valid': True,#     'valid': True,

#     'errors': [],#     'errors': [],

#     'warnings': []#     'warnings': []

# }# }

``````



## Chức năng## Chức năng



- Nhập sự kiện bằng tiếng Việt tự do- ✅ Nhập sự kiện bằng tiếng Việt tự do

- Trích xuất tự động: tên sự kiện, thời gian, địa điểm, nhắc nhở- ✅ Trích xuất tự động: tên sự kiện, thời gian, địa điểm, nhắc nhở

- Hỗ trợ thời gian tương đối: "trong X phút/giờ nữa"- ✅ Hỗ trợ thời gian tương đối: "trong X phút/giờ nữa"

- Quản lý sự kiện: Thêm, Sửa, Xóa, Tìm kiếm- ✅ Quản lý sự kiện: Thêm, Sửa, Xóa, Tìm kiếm

- Lưu trữ cục bộ (SQLite với WAL mode)- ✅ Lưu trữ cục bộ (SQLite với WAL mode)

- Hệ thống nhắc nhở tự động (mỗi 60 giây)- ✅ Hệ thống nhắc nhở tự động (mỗi 60 giây)

- Xuất/Nhập dữ liệu JSON- ✅ Xuất/Nhập dữ liệu JSON

- Giao diện GUI (Tkinter)- ✅ Giao diện GUI (Tkinter)

- Sắp xếp sự kiện theo thứ tự thêm mới nhất

- Xử lý các lỗi "database is locked" an toàn## Testing



## TestingDự án bao gồm 30 test cases kiểm tra độ chính xác NLP:



Dự án bao gồm 30 test cases kiểm tra độ chính xác NLP:```bash

python tests/test.py

```bash```

python tests/test.py

```Yêu cầu: **>= 80% accuracy**



Yêu cầu: **>= 80% accuracy**## Recent Fixes (Dec 6, 2025)



## Recent Fixes (Dec 6, 2025)### ✅ Database Lock Issue Fixed

- Added timeout (30 seconds) to SQLite connections

### Database Lock Issue Fixed- Enabled WAL mode for concurrent access

- Added timeout (30 seconds) to SQLite connections- Added try-finally blocks for connection cleanup

- Enabled WAL mode for concurrent access- All 7 database methods updated with proper error handling

- Added try-finally blocks for connection cleanup- **Status:** 100% pass rate on all tests

- All 7 database methods updated with proper error handling

- Status: 100% pass rate on all tests### ✅ Relative Time Input Support

- Added support for "trong X phút nữa" (in X minutes)

### Relative Time Input Support- Added support for "trong X giờ nữa" (in X hours)

- Added support for "trong X phút nữa" (in X minutes)- Reminder minutes now extracted from input instead of defaulting to 15

- Added support for "trong X giờ nữa" (in X hours)- Start time calculated as NOW + X minutes/hours

- Reminder minutes now extracted from input instead of defaulting to 15- **Status:** 18/18 test cases pass

- Start time calculated as NOW + X minutes/hours

- Status: 18/18 test cases pass### Example Inputs Now Supported:

```

### Event List Sorting (Newest-First)✅ "nhac toi di hoc trong 10 phut nua"

- Database returns events ordered by created_at DESC   → Event: di hoc, Reminder: 10 min, Start: NOW + 10 min

- GUI also sorts newest-added events first

- Status: Fully implemented and tested✅ "nham toi hop nhom trong 2 gio nua o phong 302"

   → Event: hop, Location: phong 302, Reminder: 120 min, Start: NOW + 2 hours

### Example Inputs Now Supported:

```✅ "goi ban trong 5 phut nua"

"nhac toi di hoc trong 10 phut nua"   → Event: goi ban, Reminder: 5 min, Start: NOW + 5 min

   → Event: di hoc, Reminder: 10 min, Start: NOW + 10 min```



"nham toi hop nhom trong 2 gio nua o phong 302"## Lưu ý

   → Event: hop, Location: phong 302, Reminder: 120 min, Start: NOW + 2 hours

- Ứng dụng chạy trên **Windows** (sử dụng `winsound` cho âm thanh nhắc nhở)

"goi ban trong 5 phut nua"- Để chạy trên Linux/macOS, cần chỉnh sửa phần âm thanh trong `ui/window.py`

   → Event: goi ban, Reminder: 5 min, Start: NOW + 5 min- Database SQLite tự động được tạo trong thư mục `data/`

```- Múi giờ mặc định: **Asia/Ho_Chi_Minh (UTC+7)**



## Lưu ý## Phiên bản hiện tại



- Ứng dụng chạy trên **Windows** (sử dụng `winsound` cho âm thanh nhắc nhở)**v1.0** - Phiên bản đầy đủ với NLP + UI + Database + Reminder

- Để chạy trên Linux/macOS, cần chỉnh sửa phần âm thanh trong `ui/window.py`

- Database SQLite tự động được tạo trong thư mục `data/`---

- Múi giờ mặc định: **Asia/Ho_Chi_Minh (UTC+7)**

Được phát triển như bài báo cáo chuyên ngành.

## Phiên bản hiện tại

**v1.0** - Phiên bản đầy đủ với NLP + UI + Database + Reminder

---

Được phát triển như bài báo cáo chuyên ngành.
