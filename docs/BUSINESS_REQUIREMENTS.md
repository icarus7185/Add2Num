# Tài liệu yêu cầu nghiệp vụ - Add2Num

## 1. Vấn đề

Học sinh khi học phép cộng số nguyên theo cách tiểu học (cộng từng cột từ phải sang trái, có nhớ) thường gặp khó khăn khi:

- Số cần cộng có rất nhiều chữ số, vượt quá khả năng xử lý chính xác của máy tính cầm tay hoặc công cụ tính toán thông thường.
- Các công cụ tính toán hiện có chỉ đưa ra kết quả cuối cùng mà không giải thích cách tính, khiến học sinh không hiểu được bản chất của phép cộng có nhớ theo cột.
- Giáo viên không có công cụ trực quan để minh hoạ từng bước cộng cho học sinh trong giờ học.

## 2. Mục tiêu

- Xây dựng một ứng dụng web đơn giản, giúp học sinh nhập hai số nguyên lớn và xem được tổng chính xác.
- Minh hoạ trực quan từng bước cộng theo cột, có nhớ, đúng như cách làm trên giấy mà học sinh được dạy ở trường.
- Đảm bảo ứng dụng dễ sử dụng, thông báo lỗi rõ ràng, dễ hiểu đối với người dùng phổ thông (không yêu cầu kiến thức kỹ thuật).
- Đảm bảo phần lõi tính toán có thể tái sử dụng cho các mục đích khác ngoài web app này.

## 3. Các bên liên quan

| Bên liên quan | Vai trò / Lợi ích |
|---|---|
| Học sinh | Người dùng chính, sử dụng ứng dụng để xem kết quả và hiểu cách cộng số lớn theo từng bước. |
| Giáo viên | Sử dụng ứng dụng làm công cụ minh hoạ, hỗ trợ giảng dạy trên lớp. |
| Người quản lý dự án | Theo dõi tiến độ, đảm bảo ứng dụng đáp ứng đúng mục tiêu giáo dục đề ra. |
| Đội phát triển | Xây dựng và bảo trì ứng dụng theo yêu cầu nghiệp vụ. |

## 4. Phạm vi

### 4.1. Trong phạm vi (sẽ làm)

- Cho phép nhập hai số nguyên không âm, không giới hạn số lượng chữ số.
- Tính tổng chính xác của hai số, không bị giới hạn hay sai số như các công cụ tính toán thông thường.
- Hiển thị log diễn giải từng bước cộng theo cột (cột nào cộng với cột nào, có phát sinh nhớ hay không) đối với các số có độ dài ở mức vừa phải.
- Với số có độ dài rất lớn, vẫn trả về kết quả chính xác nhưng bỏ qua việc hiển thị log từng bước, nhằm tránh làm chậm hoặc treo ứng dụng.
- Kiểm tra và báo lỗi khi người dùng nhập sai dữ liệu (chứa chữ cái, số âm, hoặc để trống), thông báo lỗi phải chỉ rõ vị trí hoặc ký tự gây ra lỗi.
- Toàn bộ thông báo hiển thị cho người dùng đều bằng tiếng Việt.
- Phần tính toán (thư viện cộng số lớn) được xây dựng độc lập, có thể tái sử dụng ở các dự án khác không liên quan đến giao diện web.

### 4.2. Ngoài phạm vi (chưa làm)

- Các phép tính khác ngoài phép cộng (trừ, nhân, chia...).
- Hỗ trợ số âm và số thập phân.
- Chức năng đăng nhập người dùng hoặc lưu lại lịch sử các lần tính toán.
- Triển khai (deploy) ứng dụng lên môi trường internet công cộng.

## 5. Tiêu chí thành công

- Ứng dụng cộng đúng kết quả với hai số nguyên có hàng nghìn chữ số trở lên.
- Với số ở độ dài vừa phải, log từng bước cộng hiển thị đầy đủ, đúng thứ tự, đúng với cách tính cộng có nhớ theo cột trên giấy.
- Khi người dùng nhập dữ liệu không hợp lệ, ứng dụng luôn hiển thị thông báo lỗi bằng tiếng Việt, dễ hiểu và chỉ rõ nguyên nhân.
- Với số có độ dài rất lớn, ứng dụng vẫn phản hồi kết quả trong thời gian hợp lý, không bị treo hoặc quá tải.
- Giáo viên có thể sử dụng ứng dụng để minh hoạ trực tiếp trong giờ học mà không cần hướng dẫn kỹ thuật phức tạp.

## 6. Rủi ro

- Số nhập vào quá lớn có thể khiến việc hiển thị log từng bước làm chậm hoặc treo trình duyệt nếu không giới hạn hợp lý.
- Người dùng có thể nhập dữ liệu sai định dạng (khoảng trắng, ký tự đặc biệt, số âm) theo nhiều cách khác nhau, cần kiểm tra đầy đủ để tránh bỏ sót.
- Do chưa hỗ trợ đăng nhập hay lưu lịch sử, người dùng sẽ mất kết quả tính toán khi tải lại trang, có thể gây bất tiện khi sử dụng trong giờ học.
- Vì chưa deploy public, ứng dụng chỉ phục vụ được trong phạm vi nội bộ (máy cá nhân hoặc mạng nội bộ), hạn chế khả năng tiếp cận rộng rãi.
