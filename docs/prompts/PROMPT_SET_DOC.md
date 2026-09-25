# Bộ prompt dựng project Add2Num

## A. Viết tài liệu

** Gợi ý cách viết brief**

````text
Hãy gợi ý tôi cách viết brief để triển khai ý tưởng:
web app cộng hai số nguyên rất lớn theo cách tiểu học, gồm:
- thư viện tính toán cộng từng chữ số từ phải sang trái, có nhớ
- API nhận hai số và trả về kết quả
- giao diện web nhập số và xem log từng bước tính
````

** Tài liệu yêu cầu nghiệp vụ**

````text
Tôi đang làm một web app nhỏ để minh hoạ phép cộng số nguyên lớn cho học sinh.

Vấn đề hiện tại:
- Máy tính thông thường không cộng được số có hàng nghìn chữ số, hoặc chỉ ra kết quả mà không giải thích cách tính.
- Học sinh cần thấy từng bước cộng theo cột, có nhớ, giống cách làm trên giấy.

Ứng dụng cần làm được:
- Nhập hai số nguyên không âm, không giới hạn số chữ số, bấm nút là ra tổng chính xác.
- Hiện log từng bước: cột nào cộng với cột nào, có nhớ hay không.
- Nhập sai (chữ cái, số âm, để trống) thì báo lỗi dễ hiểu, chỉ rõ ký tự sai ở đâu.
- Số quá dài thì vẫn tính được, nhưng không cần in log từng bước để tránh treo máy.
- Phần tính toán phải dùng lại được ở project khác, không phụ thuộc vào web.
- Mọi thông báo cho người dùng bằng tiếng Việt.

Chưa làm các phần sau:
- các phép tính khác ngoài cộng; số âm, số thập phân;
- đăng nhập, lưu lịch sử tính;
- deploy public lên internet.

Dựa vào mô tả trên, viết giúp tôi docs/BUSINESS_REQUIREMENTS.md. Người đọc là giáo viên và người quản lý dự án, nên viết bằng ngôn ngữ nghiệp vụ, đừng đưa chi tiết kỹ thuật vào.
Tài liệu cần có: vấn đề, mục tiêu, các bên liên quan, phạm vi làm và không làm, tiêu chí thành công, rủi ro.
Tài liệu viết bằng tiếng Anh.
````

** Spec yêu cầu phần mềm (SRS)**

````text
Viết docs/requirements-spec.md dựa trên docs/BUSINESS_REQUIREMENTS.md.
Hệ thống có 3 phần: thư viện core (class MyBigNumber, là git submodule branch core), API FastAPI trong main.py, và giao diện static/index.html.
Cần có: business rules (BR-xx), yêu cầu chức năng chia theo từng phần (FR-xx), yêu cầu phi chức năng có đo được (NFR-xx), đặc tả API, use case, acceptance criteria dạng Given/When/Then (AC-xx), bảng truy vết AC → test, và câu hỏi còn mở.
Phần đặc tả API liệt kê mọi endpoint của main.py (GET /, POST /calculate). Mỗi endpoint ghi rõ: request, các mã trạng thái có thể trả về (200, 400, 422), và ví dụ JSON cho từng mã. Ví dụ phải lấy từ kết quả chạy thật, đừng tự bịa.
Mọi câu thông báo và dòng log tiếng Việt thì trích nguyên văn.
````

** Coding rules**

````text
Viết lại docs/coding-rules.md cho code Python của repo này (core/ và main.py). Mỗi quy tắc có mã riêng (PY-001...) và mức MUST/SHOULD để AI review theo được.
Cần bao gồm: tách core khỏi web framework, đặt tên, type hint, validate đầu vào, xử lý lỗi, logging, hiệu năng với số rất lớn, test.
Thêm một phần ngắn cho static/index.html (JS/CSS): không dùng innerHTML với dữ liệu từ API, không để trang bị cuộn ngang.
Cuối tài liệu thêm checklist các quy tắc MUST. Giữ các quy tắc hiện có, chỉ đánh mã và bổ sung.
````

** Rà soát tài liệu **

````text
Đọc lại toàn bộ tài liệu trong docs/ và README.md, so với brief và so chéo giữa các tài liệu với nhau. Tìm: chỗ thiếu, mã FR/AC hoặc câu thông báo tiếng Việt không khớp, link sai, acceptance criteria mơ hồ.
Chỗ nào sai thì sửa luôn, rồi gửi tôi danh sách những gì đã sửa.
````

** Cập nhật tài liệu sau khi đổi code (mẫu chung)**

````text
Tôi vừa sửa <mô tả thay đổi, hoặc dán git diff / số commit>.
Tìm mọi tài liệu (docs/, core/README.md, README.md) đang mô tả phần này và cập nhật cho khớp với code mới. Đừng viết lại những phần không liên quan.
Gửi tôi danh sách chỗ đã sửa.
````

** Thêm yêu cầu mới vào spec trước khi code**

````text
Tôi muốn thêm chức năng: nút "Sao chép kết quả" trên giao diện cho kết quả rất dài (câu hỏi Q-05 trong requirements-spec.md).
Viết trước phần spec: thêm FR mới vào requirements-spec.md (có acceptance criteria), đóng Q-05, cập nhật phần đặc tả API nếu cần. Chưa code gì cả.
Chỗ nào chưa rõ (thông báo sau khi sao chép, trình duyệt không cho truy cập clipboard...) thì hỏi tôi.
````

** Viết lại tài liệu từ code**

````text
requirements-spec.md đã cũ, không còn khớp với code. Đọc code hiện tại (core/big_number.py, main.py, static/index.html) rồi viết lại, giữ nguyên khung và mã FR/AC cũ. FR nào không còn thì đánh dấu removed chứ đừng xoá mã, FR mới thì đánh mã tiếp theo trong nhóm của nó.
Chỗ nào code có vẻ làm sai so với spec cũ thì đừng tự chọn bên nào đúng, ghi ra cho tôi.
````

** Cập nhật README**

````text
Cập nhật README.md:
- thêm cấu trúc thư mục đầy đủ, kể cả docs/;
- thêm hướng dẫn clone kèm submodule core (git clone --recurse-submodules, hoặc git submodule update --init nếu đã clone);
- thêm ví dụ gọi POST /calculate bằng curl.
Lệnh nào cũng ghi cho cả Bash và PowerShell.
````

** Dịch tài liệu**

````text
Dịch README.md sang tiếng Anh. Giữ nguyên các lệnh, đường dẫn, tên class, tên field (num1, num2, result, log) và các câu log tiếng Việt như "Bước 1: 9 + 1 = 0, nhớ 1." vì đó là output thật của chương trình. Viết tự nhiên như người viết tài liệu kỹ thuật, đừng dịch sát từng chữ.
````

** Ghi lại một quyết định kỹ thuật**

````text
Chúng tôi vừa quyết định <ví dụ: giữ core là git submodule trỏ tới branch core của chính repo này, thay vì tách ra package pip riêng>.
Viết một ghi chú ngắn vào docs/decisions/, gồm: bối cảnh, quyết định, lý do, và ảnh hưởng. Tài liệu nào đang mô tả ngược với quyết định này thì sửa luôn.
````
