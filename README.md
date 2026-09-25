# Add2Num

Web app cộng hai số nguyên rất lớn theo cách tiểu học (cộng từng chữ số từ phải sang trái, có nhớ), có ghi log chi tiết từng bước tính.

## Cấu trúc project

```
Add2Num/
├── .github/workflows/
│   └── unit-test.yml     # GitHub Actions chạy unit test khi có PR vào main
├── main.py              # FastAPI app (route "/" trả HTML, "/calculate" xử lý API)
├── api_test.py          # Unit test cho API trong main.py
├── requirements.txt      # Thư viện cần cài
├── static/
│   └── index.html         # Giao diện web (HTML + CSS + JS)
└── core/                  # Đây là submodule link tới branch 'core'
    ├── big_number.py       # Logic cộng số lớn (class MyBigNumber)
    └── test.py              # Unit test cho big_number.py
```

## 1. Cài đặt requirements

Yêu cầu Python (gợi ý 3.12).

Khuyến khích tạo virtual environment trước khi cài:

```powershell
python -m venv venv
venv\Scripts\activate
```

Cài các thư viện cần thiết:

```powershell
pip install -r requirements.txt
```

## 2. Chạy Unit Test

Project có 2 bộ unit test, đều chạy độc lập và in kết quả ra console:

| File | Kiểm tra |
|---|---|
| `core/test.py` | Logic cộng số lớn (`MyBigNumber`) |
| `api_test.py` | API trong `main.py`: `GET /` và `POST /calculate` (kết quả, log, lỗi 400/422) |

### 2.1. Test phần core

Chạy từ thư mục gốc project:

```powershell
python core/test.py
```

Hoặc chạy trực tiếp từ trong thư mục `core/`:

```powershell
cd core
python test.py
```

### 2.2. Test phần API

Test dùng `TestClient` của FastAPI (cần thư viện `httpx`, đã có trong `requirements.txt`), không cần bật server.

Phải chạy từ thư mục gốc project, vì `api_test.py` import `main`:

```powershell
python api_test.py
```

### 2.3. Chạy tất cả test

```powershell
python core/test.py
python api_test.py
```

Kết quả mong đợi: mỗi test case hiển thị 1 dòng log riêng, kết thúc bằng `OK` nếu tất cả pass.

### 2.4. Chạy test tự động trên GitHub Actions

Workflow [`.github/workflows/unit-test.yml`](.github/workflows/unit-test.yml) tự chạy cả 2 bộ test (Python 3.12, checkout kèm submodule `core`) khi:

- mở hoặc cập nhật pull request vào `main`;
- push lên `main`;
- bấm chạy tay trong tab **Actions** (`workflow_dispatch`).

Để chặn merge khi test fail, vào **Settings → Branches → Branch protection rules** của `main`, bật **Require status checks to pass before merging** và chọn check `test`.

## 3. Deploy / chạy web app

Chạy server bằng Uvicorn từ thư mục gốc project (`main.py` import `core.big_number`, nên phải chạy tại đây):

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000
```

Sau đó mở trình duyệt tại:

```
http://127.0.0.1:8000
```

Nhập hai số nguyên không âm và bấm **Tính** để xem kết quả cùng log từng bước cộng.

Log xử lý (từng bước cộng) sẽ được in ra console của server, đồng thời trả về kèm trong response API `/calculate`.
