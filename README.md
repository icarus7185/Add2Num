# Add2Num – Cộng hai số nguyên lớn

Thư viện Python để cộng hai số nguyên không âm rất lớn được biểu diễn dưới dạng chuỗi. Thuật toán cộng từng chữ số từ phải sang trái và có nhớ, giống cách cộng tay trên giấy. Vì vậy, độ dài của số không bị giới hạn bởi kiểu số nguyên của ngôn ngữ.

Mỗi lần gọi `sum()`, thư viện còn ghi lại log từng bước tính để có thể theo dõi hoặc minh họa quá trình cộng.

## Yêu cầu

- Python 
- Không cần cài thêm thư viện ngoài (chỉ dùng thư viện chuẩn)

## Cấu trúc thư mục

```
Add2Num/
├── big_number.py      # Lớp MyBigNumber – logic cộng số lớn
└── README.md
```

## API

### `MyBigNumber`

| Thành phần | Mô tả |
|---|---|
| `sum(stn1: str, stn2: str) -> str` | Cộng hai số nguyên không âm dạng chuỗi và trả về kết quả dạng chuỗi. Số 0 thừa ở đầu được bỏ qua (`"007" + "013"` → `"20"`). |
| `log: List[str]` | Danh sách log từng bước của lần gọi `sum()` gần nhất. Được reset mỗi lần gọi. |

Lưu ý: đầu vào phải là chuỗi chỉ gồm các chữ số `0-9`. Số âm, số thập phân và chuỗi rỗng hoặc chứa ký tự khác không được hỗ trợ và không được kiểm tra hợp lệ.

## Chạy test

Unit test của module này nằm ở `tests/test_core.py` trong repo chính (branch `main`). Chạy từ thư mục gốc repo chính:

```bash
python tests/test_core.py
```

## Coverage

```bash
coverage run --branch --source=core tests/test_core.py
coverage report -m
```