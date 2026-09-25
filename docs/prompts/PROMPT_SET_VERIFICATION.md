# Bộ prompt dựng project Add2Num

## C. Kiểm tra

** Viết unit test**

````text
Viết test cho core (core/test.py) và API (tests/test_api.py), dựa vào acceptance criteria trong requirements-spec.md. Đừng dựa vào code, vì mục đích là kiểm tra code có làm đúng spec không.
Ưu tiên các trường hợp dễ sai: 0 + 0, số có 0 ở đầu, nhớ lan truyền liên tiếp (999 + 1), hai số dài khác nhau, chuỗi rỗng, khoảng trắng, số âm, chữ số không phải ASCII, số vượt LOG_STEP_LIMIT, gọi sum() hai lần liên tiếp.
Kiểm tra cả nội dung log, không chỉ kết quả.
Chạy python core/test.py và python -m pytest -q. Test nào fail vì code làm khác spec thì giữ nguyên test, đừng sửa code, báo tôi.
````

** Review theo coding rules**

````text
Review code theo docs/coding-rules.md và báo lỗi theo dạng `Rule ID — file:line — mô tả`.
Đi qua checklist MUST, rồi sửa các lỗi MUST và chạy lại test.
````

** Chạy thử end-to-end **

````text
Chạy uvicorn main:app rồi kiểm tra:
- trên giao diện, 19 + 11 ra 30 và log đúng nguyên văn AC-11;
- nhập "12a4" thì báo đúng ký tự và vị trí, không gửi request;
- nút Tính bị khoá trong lúc chờ API;
- kết quả 1.000 chữ số xuống dòng, không làm trang cuộn ngang;
- gọi API với hai số 20.000 chữ số thì trả 200, log đúng 3 dòng;
- gọi API với "-5", "" và "١٢٣" thì trả đúng 422, 422, 400;
- console server có log request và kết quả.
Gửi tôi bảng PASS/FAIL theo mã AC.
````

** Đối chiếu tài liệu với code (cổng C)**

````text
Lấy code hiện tại làm chuẩn, rồi đọc lại toàn bộ tài liệu trong docs/, core/README.md và README.md để tìm chỗ nào đã lỗi thời hoặc không khớp với code (kể cả câu thông báo tiếng Việt và bảng truy vết AC → test).
Tài liệu sai thì sửa tài liệu. Còn nếu code sai thì đừng sửa, báo tôi.
Quyết định nào mới chốt thì ghi thêm vào brief.
````

### Kiểm tra theo từng tình huống

Dùng sau mỗi lần sửa lỗi hay thay đổi, hoặc khi nghi có vấn đề ở một chỗ cụ thể. Chỉ báo cáo trước, chưa sửa, trừ khi tôi bảo sửa.

** Review thay đổi trước khi commit (mẫu chung)**

````text
Review giúp tôi các thay đổi chưa commit (git diff, kể cả trong submodule core). Tìm bug, trường hợp biên bị bỏ sót, và chỗ làm khác spec. Kiểm tra xem test và tài liệu đã được cập nhật theo chưa.
Báo theo dạng file:line — vấn đề — mức độ. Chưa sửa gì cả.
````

** Rà soát validate đầu vào ở cả 3 lớp**

````text
So sánh cách validate đầu vào ở giao diện (JS), API (Pydantic) và MyBigNumber.sum(). Lập bảng với các input: "", "   ", " 12 ", "007", "-5", "+5", "1.5", "1e3", "1_000", "١٢٣", "１２３", số 1 triệu chữ số.
Với từng input, ghi mỗi lớp chấp nhận hay từ chối, thông báo gì, mã HTTP gì. Chỉ ra chỗ nào không nhất quán hoặc khác spec, kèm cách sửa đề xuất.
````

** Kiểm tra hiệu năng với số rất lớn**

````text
Đo thời gian và bộ nhớ của MyBigNumber.sum() và POST /calculate với số 10^3, 10^4, 10^5, 10^6 chữ số, cả có và không có nhớ lan truyền. Kiểm tra độ phức tạp có đúng O(n) như NFR-02 không, và NFR-03, NFR-04 có còn đạt không.
Chỉ ra chỗ nào tạo bản sao chuỗi hoặc list không cần thiết.
````

** Kiểm tra bảo mật cơ bản**

````text
Rà soát nhanh bảo mật: dữ liệu từ API có được hiển thị bằng textContent không (NFR-10), request rất lớn có làm treo server không, log server có ghi nguyên số cực dài không, và JSON sai kiểu (số thay vì chuỗi, null, mảng).
Ứng dụng chạy local nên chưa cần auth, chỉ cần chỉ ra rủi ro và mức độ nếu sau này deploy public (Q-01).
````

** Kiểm tra giao diện**

````text
Mở giao diện trong browser, rồi kiểm tra: theme sáng và tối, màn hình rộng 375px, dùng bàn phím (Tab, Enter) để nhập và tính, kết quả rất dài, log rất dài, và thông báo lỗi. Chụp màn hình từng trường hợp, rồi ghi ra chỗ nào bị vỡ layout, khó đọc hoặc không bấm được.
````

** Kiểm tra cài đặt trên máy sạch**

````text
Làm theo đúng README trong một thư mục clone mới và virtualenv mới: lấy submodule core, cài thư viện, chạy test, chạy server. Bước nào README ghi thiếu, ghi sai, hoặc phải tự đoán mới làm tiếp được thì ghi lại. Đây cũng là cách để kiểm tra CI có chạy được không.
````
