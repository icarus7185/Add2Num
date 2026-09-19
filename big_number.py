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

    def sum(self, stn1: str, stn2: str) -> str:
        self.log = []

        # Bỏ số 0 thừa ở đầu (nhưng giữ lại ít nhất 1 chữ số)
        num1_clean = stn1.lstrip("0") or "0"
        num2_clean = stn2.lstrip("0") or "0"

        self.log.append(f"Bắt đầu cộng: {num1_clean} + {num2_clean}")

        # Đảo ngược chuỗi để duyệt từ hàng đơn vị (phải sang trái)
        a_rev = num1_clean[::-1]
        b_rev = num2_clean[::-1]

        max_len = max(len(a_rev), len(b_rev))
        a_rev = a_rev.ljust(max_len, "0")
        b_rev = b_rev.ljust(max_len, "0")

        self.log.append(
            f"Căn chỉnh hai số cho bằng độ dài ({max_len} chữ số), "
            f"đệm thêm số 0 vào bên trái số ngắn hơn."
        )

        carry = 0
        result_digits: List[str] = []

        for i in range(max_len):
            da = int(a_rev[i])
            db = int(b_rev[i])
            raw_sum = da + db
            total = raw_sum + carry
            digit = total % 10
            new_carry = total // 10

            result_digits.append(str(digit))
            current_result = "".join(reversed(result_digits))

            luu_ket_qua = f"Lưu {digit} vào kết quả"
            if new_carry:
                luu_ket_qua += f" và nhớ {new_carry}"
            luu_ket_qua += "."

            if i == 0:
                step_msg = (
                    f"Bước {i + 1}: Lấy {da} cộng với {db} được {raw_sum}. "
                    f"{luu_ket_qua}"
                )
            else:
                step_msg = f"Bước {i + 1}: Lấy {da} cộng với {db} được {raw_sum}."
                if carry:
                    step_msg += f" Cộng tiếp với nhớ {carry} được {total}."
                step_msg += f' {luu_ket_qua} Kết quả mới là {current_result}.'

            self.log.append(step_msg)
            logger.info(step_msg)

            carry = new_carry

        if carry:
            result_digits.append(str(carry))
            current_result = "".join(reversed(result_digits))
            final_carry_msg = (
                f'Hết các chữ số, vẫn còn nhớ {carry}. Viết thêm {carry} vào kết quả '
                f'được kết quả mới là "{current_result}".'
            )
            self.log.append(final_carry_msg)
            logger.info(final_carry_msg)

        result = "".join(reversed(result_digits)).lstrip("0") or "0"
        self.log.append(f"Kết quả cuối cùng: {result}")

        return result
