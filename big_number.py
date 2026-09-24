"""
Module tái sử dụng: xử lý logic cộng hai số nguyên rất lớn
(cộng từng chữ số từ phải sang trái, có nhớ).
"""

import logging
from typing import List

logger = logging.getLogger("big-number-addition")


class MyBigNumber:
    """Đóng gói thuật toán cộng số nguyên lớn.

    Sau khi gọi `sum()`, danh sách log từng bước có thể lấy qua thuộc tính `log`.
    """

    def __init__(self) -> None:
        self.log: List[str] = []

    # Trên ngưỡng này thì không log chi tiết từng bước nữa (chỉ log tóm tắt),
    # để tránh việc log tạo ra hàng tỷ phần tử khi số quá lớn.
    LOG_STEP_LIMIT = 10_000

    def sum(self, stn1: str, stn2: str, verbose_log: bool = True) -> str:
        self.log = []

        # Chỉ chấp nhận chuỗi chữ số ASCII 0-9 (số nguyên không âm), không rỗng.
        for stn in (stn1, stn2):
            if not (isinstance(stn, str) and stn.isascii() and stn.isdigit()):
                raise ValueError(f"'{stn}' không phải là số nguyên không âm hợp lệ")

        # Bỏ số 0 thừa ở đầu (nhưng giữ lại ít nhất 1 chữ số)
        num1_clean = stn1.lstrip("0") or "0"
        num2_clean = stn2.lstrip("0") or "0"
        len1, len2 = len(num1_clean), len(num2_clean)
        max_len = max(len1, len2)

        log_steps = verbose_log and max_len <= self.LOG_STEP_LIMIT

        self.log.append(f"Bắt đầu cộng: {num1_clean} + {num2_clean}")
        if verbose_log and not log_steps:
            self.log.append(
                f"Số có tới {max_len} chữ số nên bỏ qua log chi tiết từng bước "
                f"để tránh tốn bộ nhớ/thời gian không cần thiết."
            )

        # Cấp phát sẵn buffer kết quả (dư 1 ô cho nhớ tràn ra ngoài cùng bên trái),
        # điền trực tiếp đúng vị trí cuối cùng nên không cần đảo ngược kết quả.
        result = [""] * (max_len + 1)
        carry = 0
        # Duyệt bằng chỉ số lùi từ cuối chuỗi gốc, không cần đảo chuỗi hay padding.
        i, j, k = len1 - 1, len2 - 1, max_len
        step = 0

        # 1) Cộng phần chồng lấn của cả hai số (từ hàng đơn vị).
        # python không cấp phát vùng nhớ mới cho các biến trong vòng lặp nên không cần bắt lỗi,
        #     việc khai báo biến ở người còn làm code phức tạp thêm.
        while i >= 0 and j >= 0:
            da, db = int(num1_clean[i]), int(num2_clean[j])
            carry_in = carry
            total = da + db + carry
            digit, carry = total % 10, total // 10
            result[k] = str(digit)

            if log_steps:
                step += 1
                msg = f"Bước {step}: {da} + {db}"
                if carry_in:
                    msg += " (cộng thêm nhớ)"
                msg += f" = {digit}, nhớ {carry}." if carry else f" = {digit}."
                self.log.append(msg)
                logger.info(msg)

            i, j, k = i - 1, j - 1, k - 1

        # Số nào còn dư chữ số ở phía trước thì tiếp tục xử lý số đó.
        longer, idx = (num2_clean, j) if i < 0 else (num1_clean, i)

        # 2) Cộng nốt phần dư với nhớ, dừng ngay khi hết nhớ (không cần "cộng với 0").
        while idx >= 0 and carry:
            total = int(longer[idx]) + carry
            digit, carry = total % 10, total // 10
            result[k] = str(digit)

            if log_steps:
                step += 1
                msg = f"Bước {step}: {longer[idx]} + nhớ = {digit}"
                msg += f", nhớ {carry}." if carry else "."
                self.log.append(msg)
                logger.info(msg)

            idx, k = idx - 1, k - 1

        # 3) Hết nhớ nhưng vẫn còn phần dư: gắn thẳng nguyên đoạn còn lại
        # của số dài hơn vào kết quả (một lần gán), không cộng từng chữ số nữa.
        if idx >= 0:
            result[k - idx : k + 1] = longer[: idx + 1]
            if log_steps:
                msg = f"Hết nhớ, giữ nguyên phần còn lại '{longer[: idx + 1]}' của số dài hơn."
                self.log.append(msg)
                logger.info(msg)

        start = 0
        if carry:
            result[0] = str(carry)
        else:
            start = 1  # ô đầu chưa được ghi (không tràn nhớ) nên bỏ qua

        final_result = "".join(result[start:])
        self.log.append(f"Kết quả cuối cùng: {final_result}")

        return final_result
