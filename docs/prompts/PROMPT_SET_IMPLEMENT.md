# Bộ prompt dựng project Add2Num

## B. Triển khai

** Khung repo**

````text
Tạo khung repo theo brief và requirements-spec.md: main.py, static/index.html, thư mục core là git submodule trỏ tới branch core, requirements.txt đã ghim version, .gitignore (ignore venv/, __pycache__/).
Chưa cần viết logic.
````

** Code thư viện core**

````text
Code core/big_number.py theo requirements-spec.md (mục 4.1, 4.2) và coding-rules.md.
Cộng từng chữ số từ phải sang trái, không đổi cả chuỗi sang int, không đảo chuỗi hay pad số 0. Log từng bước đúng nguyên văn trong spec, có ngưỡng LOG_STEP_LIMIT.
core không được import FastAPI hay Pydantic.
Xong thì chạy thử vài phép cộng (999 + 1, 19 + 11, 007 + 013) và báo tôi kết quả kèm log.
````

** Code API và giao diện**

````text
Code main.py và static/index.html theo requirements-spec.md (mục 4.3, 4.4 và phần đặc tả API) và coding-rules.md.
Nên làm theo thứ tự API → giao diện để có API chạy thử trước.
Xong thì chạy uvicorn main:app, gọi thử POST /calculate với một input hợp lệ, một input sai (422) và một input chữ số không phải ASCII (400), rồi mở giao diện nhập thử và báo tôi kết quả.
````

** Unit test**

````text
Viết unit test cho core trong core/test.py, dạng bảng (mô tả, num1, num2, kết quả mong đợi) để thêm case không cần viết hàm mới. Test phải chạy độc lập bằng python core/test.py, mỗi case in một dòng, pass hết thì in OK.
Viết thêm test API bằng FastAPI TestClient trong tests/test_api.py. Acceptance criteria nào kiểm tra được bằng test tự động thì phải có test.
````

** CI và README (cổng B)**

````text
Thêm GitHub Actions: khi có PR vào main thì checkout kèm submodule, cài requirements, chạy python core/test.py và test API.
Thêm issue template cho bug, feature và spike.
Viết README.md gồm: giới thiệu, cấu trúc thư mục, cách cài (có bước lấy submodule core), cách chạy, cách test.
````

### Sửa lỗi và thay đổi

Dùng sau khi hệ thống đã chạy được. Sửa gì thì cập nhật spec và test cho khớp, để tài liệu không bị lệch so với code.

** Sửa lỗi (mẫu chung)**

````text
Tôi gặp lỗi này ở <core | API | giao diện>:
<dán log / traceback / input gây lỗi / mô tả hiện tượng>
Tìm nguyên nhân trước, giải thích cho tôi, rồi mới sửa. Viết thêm test tái hiện lỗi này, sửa xong thì test phải pass. Đừng sửa lan sang chỗ khác.
````

** Sửa lỗi: log ghi sai "(cộng thêm nhớ)"**

````text
Cộng 19 + 11 thì log ghi "Bước 2: 1 + 1 = 3." thiếu "(cộng thêm nhớ)", còn 5 + 5 lại ghi "(cộng thêm nhớ)" dù không có nhớ từ cột trước. Theo FR-11, nhãn này phụ thuộc vào nhớ đi VÀO cột hiện tại, không phải nhớ đi ra.
Sửa lại và thêm test cho cả hai trường hợp.
````

** Sửa lỗi: MyBigNumber nhận input không hợp lệ**

````text
Gọi trực tiếp MyBigNumber().sum("-5", "3") trả về "-8", còn sum(" 12", "3") trả về " 15". Qua API, "١٢٣" + "1" lọt qua regex \d và trả về kết quả sai với HTTP 200.
Theo FR-07, sum() phải raise ValueError với input không phải chuỗi chữ số ASCII. Sửa lại, kiểm tra API trả về 400 cho trường hợp này, và thêm test.
````

** Thay đổi cấu hình**

````text
Tôi muốn đổi LOG_STEP_LIMIT từ 10_000 xuống 5_000. Đổi trong code, rồi tìm và cập nhật mọi chỗ trong docs, README và test đang ghi số cũ.
````

** Thêm chức năng: bật/tắt log chi tiết qua API**

````text
Thêm field tuỳ chọn verbose_log (bool, mặc định true) vào request POST /calculate, truyền xuống MyBigNumber.sum(). Trên giao diện thêm checkbox "Hiện log từng bước", mặc định bật.
Đóng câu hỏi Q-02, cập nhật requirements-spec.md (cả FR và phần đặc tả API) và thêm test.
````

** Thay đổi giao diện**

````text
Trên giao diện:
- thêm nút "Sao chép kết quả" cạnh khối kết quả;
- hiện số chữ số của từng số đã nhập, cập nhật khi gõ;
- thêm thẻ viewport để xem được trên điện thoại (Q-04).
Giữ nguyên style hiện tại, và vẫn phải xem ổn ở theme tối lẫn màn hình rộng 375px. Làm xong chụp màn hình cho tôi xem.
````
