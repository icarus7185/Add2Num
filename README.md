# Add2Num

Web app cộng hai số nguyên rất lớn theo cách tiểu học (cộng từng chữ số từ phải sang trái, có nhớ), có ghi log chi tiết từng bước tính.

## Cấu trúc project

```
Add2Num/
├── main.py              # FastAPI app (route "/" trả HTML, "/calculate" xử lý API)
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

Unit test nằm ở `core/test.py`, có thể chạy độc lập, kết quả in ra console.

Chạy từ thư mục gốc project:

```powershell
python core/test.py
```

Hoặc chạy trực tiếp từ trong thư mục `core/`:

```powershell
cd core
python test.py
```

Kết quả mong đợi: mỗi test case hiển thị 1 dòng log riêng, kết thúc bằng `OK` nếu tất cả pass.

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
