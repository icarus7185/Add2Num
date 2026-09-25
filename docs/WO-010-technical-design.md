# Thiết kế kỹ thuật - WO-010

## 1. Mục tiêu issue

Issue WO-010: [FEAT]: WO-010 sửa layout hiển thị

Theo mô tả trên GitHub, issue này chỉ tập trung vào việc sửa layout hiển thị của màn hình web, không sửa logic tính toán, không sửa API và không thêm dependency ngoài. Mục tiêu là cải thiện trải nghiệm người dùng khi màn hình desktop theo tỉ lệ 16:9, giảm hiện tượng phải cuộn xuống nhiều để xem log từng bước trên màn hình.

Nội dung cần ưu tiên:
- sắp xếp bố cục theo chiều ngang thay vì dàn theo chiều dọc;
- tận dụng không gian hai cột màn hình để hiển thị form nhập và kết quả/log đồng thời;
- tránh để màn hình còn nhiều khoảng trống nhưng vẫn phải scroll xuống để xem nội dung;
- vẫn giữ giao diện dễ đọc trên desktop và có thể chịu được màn hình hẹp hơn ở mức fallback.

---

## 2. Bối cảnh và ràng buộc

### 2.1 Business intent

User đang sử dụng app Add2Num trên máy tính có màn hình rộng theo tỉ lệ 16:9. Layout hiện tại đang hiển thị theo chiều dọc và buộc người dùng phải scroll xuống để xem log các bước tính. Hệ quả là không gian màn hình hai bên trái phải không được tận dụng hiệu quả và trải nghiệm hiển thị bị kém.

### 2.2 Scope

Trong phạm vi:
- chỉ sửa layout UI;
- chỉnh sửa HTML và CSS trong `/static/`;
- tương thích với các chức năng hiện có mà không làm thay đổi logic tính toán.

Ngoài phạm vi:
- không xử lý logic cộng số lớn;
- không thay đổi API;
- không thêm thư viện bên ngoài;
- không mở rộng sang các feature mới khác.

### 2.3 AI Copilot execution constraints

- Target Tech Stack: Python 3.14 / FastAPI / Pydantic v2
- Allowed Directory Scope: `/static/`
- Dependency Guardrail: Không thêm dependency ngoài nếu chưa có review kiến trúc.

---

## 3. Yêu cầu kiến trúc UI

### 3.1 Lớp UI chính

Cấu trúc hiện tại vẫn giữ nguyên các thành phần core của app:
- input cho số thứ nhất
- input cho số thứ hai
- nút tính
- khu vực hiển thị kết quả
- khu vực hiển thị log từng bước

Tuy nhiên, layout sẽ được tái cấu trúc theo dạng:
- panel trái: form nhập liệu và điều khiển
- panel phải: kết quả và log

### 3.2 Mô hình bố cục đề xuất

```text
+---------------------------------------------------------------+
| Header / Title                                                 |
+---------------------------------------------------------------+
| [Input panel] | [Result / Log panel]                           |
|               |                                               |
| - Số thứ nhất  | Kết quả cuối cùng                          |
| - Số thứ hai   | Log từng bước (scroll nếu dài)             |
| - Nút Tính     |                                               |
| - Error box    |                                               |
+---------------------------------------------------------------+
```

### 3.3 Cách bố trí trên desktop

- Sử dụng CSS Grid hoặc Flexbox với 2 cột trên màn hình rộng.
- Tỉ lệ đề xuất: khoảng 40% cho panel nhập, 60% cho panel kết quả/log.
- Không để một panel quá rộng nhưng lại trống nhiều khoảng cách.
- Panel log nên có chiều cao cố định hoặc một vùng scroll nội bộ để không kéo dài toàn trang.

### 3.4 Cách xử lý khi màn hình hẹp

- Khi viewport nhỏ hơn ngưỡng định nghĩa, chuyển về bố cục 1 cột.
- Giữ ý tưởng: form trước, kết quả/log sau, thay vì lộn ngược thứ tự.
- Tránh phải scroll quá mức xuống dưới để đọc log.

---

## 4. Layout redesign details

### 4.1 Mục tiêu trực quan

- Tận dụng màn hình ngang 16:9.
- Giảm nguy cơ màn hình trống dọc trong khi vẫn phải cuộn xuống.
- Làm nổi bật vùng nhập và vùng output.
- Tạo cảm giác dễ đọc và có cấu trúc hơn cho người dùng học tập.

### 4.2 Yêu cầu bố cục chi tiết

1. Header
   - hiển thị tiêu đề chính rõ ràng;
   - có mô tả ngắn về mục đích app;
   - giữ không quá cao để tối ưu không gian.

2. Form panel
   - hiển thị 2 trường nhập tương ứng với số thứ nhất và số thứ hai;
   - nút tính ở dưới hoặc bên cạnh trường nhập tùy layout;
   - giữ vùng lỗi và trạng thái loading rõ ràng.

3. Output panel
   - đặt ngay bên cạnh panel nhập nếu màn hình rộng;
   - hiển thị kết quả bằng block lớn, dễ nhận diện;
   - log từng bước hiển thị trong vùng có scroll riêng; tránh kéo dài toàn page.

4. Scroll behavior
   - chỉ log panel mới cần scroll nếu nội dung dài;
   - màn hình không nên bị cuộn xuống nhiều do bố cục dàn theo chiều dọc.

---

## 5. Thiết kế CSS hướng đến issue

### 5.1 Nguyên tắc thiết kế

- Dùng layout container có `max-width` hợp lý, không mở rộng quá mức.
- Dùng `display: grid` hoặc `display: flex` để chia 2 cột.
- Dùng `min-height` cho khu vực hiển thị log để đồng nhất chiều cao.
- Dùng `overflow: auto` cho log panel để tránh đẩy phần trên xuống.
- Không thêm animation phức tạp hoặc library mới.

### 5.2 CSS focus

Các yếu tố cần ưu tiên trong CSS:
- spacing hợp lý giữa các block;
- khoảng cách sát nhau nhưng không chật quá;
- border radius, shadow, background để tách biệt panel;
- typography rõ ràng, chuyên biệt giữa title, input và log;
- `word-break: break-word` hoặc wrapping cho output dài.

### 5.3 Responsive strategy

- Desktop: 2 cột ngang
- Tablet: có thể chuyển về 1 cột hoặc 2 cột chật hơn
- Mobile: ưu tiên 1 cột hoàn toàn, nhưng vẫn giữ thứ tự logic

---

## 6. Không làm thay đổi logic

Theo issue và giới hạn scope, thiết kế này không thay đổi:
- logic cộng số lớn;
- request/response API;
- backend validation;
- tính toán hoặc format log từ Python.

Chỉ có phần UI / CSS sẽ được sửa để hiển thị tốt hơn và hợp với tỉ lệ màn hình 16:9.

---

## 7. Giải pháp kỹ thuật đề xuất

### 7.1 HTML

Cần tối ưu cấu trúc HTML để layout rõ ràng:
- wrapper tổng chứa title và panel chính;
- một section cho form;
- một section cho output/log;
- các container có class rõ ràng như `app-shell`, `input-panel`, `result-panel`, `log-panel`.

### 7.2 CSS

- dùng CSS variables cho spacing/color để dễ chỉnh sửa;
- ưu tiên `grid-template-columns` cho desktop;
- dùng media query để fallback mobile;
- đảm bảo output box có `overflow-wrap: anywhere;` nếu có số rất dài.

### 7.3 JS

Không cần thay đổi logic nghiệp vụ mạnh. Chỉ cần giữ hoặc điều chỉnh các chế độ hiện có như:
- disable nút tính trong lúc xử lý;
- hiển thị lỗi và kết quả;
- render log dưới dạng text, không dùng HTML từ dữ liệu đầu vào.

Nếu cần cải tuy chỉnh cho layout, JavaScript chỉ nên xử lý thêm class state hoặc cập nhật UI, không thay đổi logic tính toán.

---

## 8. Kiểm thử chấp nhận

Acceptance criteria từ issue:
- [ ] Màn hình hiển thị theo phương ngang, hạn chế trường hợp màn hình vẫn còn nhiều khoảng trống mà vẫn phải scroll để xem nội dung.

Các kiểm tra thực tế nên bao gồm:
1. Mở app trên màn hình desktop 16:9.
2. Kiểm tra form nhập và result/log ở cùng một viewport trong hai cột.
3. Đảm bảo không còn tình trạng phần lớn space trống dọc.
4. Kiểm tra scroll chỉ xuất hiện ở panel log khi nội dung dài.
5. Kiểm tra giao diện không làm xấu chức năng đang có.

---

## 9. Rủi ro và cách kiểm soát

### Rủi ro 1: Layout quá chật trên màn hình nhỏ
- Giải pháp: áp dụng media query, chuyển sang 1 cột khi không đủ rộng.

### Rủi ro 2: log panel quá dài khiến page kéo dài
- Giải pháp: giới hạn chiều cao panel log và cho phép scroll nội bộ.

### Rủi ro 3: layout phá vỡ do mã HTML hiện có
- Giải pháp: thay đổi đúng trong file static, không chỉnh backend, chỉ tập trung vào cấu trúc và CSS wrapper.

### Rủi ro 4: thêm dependency không cần thiết
- Giải pháp: giữ nguyên stack hiện có, không thêm framework CSS bên ngoài.

---

## 10. Kết luận

WO-010 là một issue thuộc nhóm UI layout, không phải issue business logic. Thiết kế kỹ thuật cần tập trung vào việc re-layout giao diện theo hướng ngang, tận dụng không gian màn hình desktop 16:9, giảm tình trạng scroll dọc không cần thiết và tối ưu trải nghiệm khi xem log các bước tính. Mục tiêu chính là improve visual efficiency trong phạm vi file HTML/CSS của `/static/`, đồng thời không làm ảnh hưởng tới logic app hiện có.

---

## 11. Nguồn tham khảo

- Issue GitHub: https://github.com/icarus7185/Add2Num/issues/2
- Mô tả issue (đã kiểm tra từ API GitHub):
  - Title: [FEAT]: WO-010 sửa layout hiển thị
  - Scope: chỉ sửa layout, file html và css
  - Non-goal: xử lý logic
