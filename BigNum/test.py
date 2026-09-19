"""
Unit test cho module big_number.py (MyBigNumber).

Chạy độc lập:
    python test.py
"""

import sys
import unittest

from big_number import MyBigNumber

# Dữ liệu test dạng bảng: [mô tả, num1, num2, kết quả mong đợi]
ADDITION_CASES = [
    ["cong don gian khong nho", "2", "3", "5"],
    ["cong co nho mot chu so", "9", "9", "18"],
    ["cong hai so cung do dai", "123", "456", "579"],
    ["cong khac do dai", "9", "9999", "10008"],
    ["cong co nho lan truyen lien tiep", "999", "1", "1000"],
    ["cong voi so 0 - ca hai deu 0", "0", "0", "0"],
    ["cong voi so 0 - so dau la 0", "0", "123", "123"],
    ["cong voi so 0 - so sau la 0", "123", "0", "123"],
    ["cong so co so 0 thua o dau", "007", "013", "20"],
    ["cong so nguyen rat lon",
     "123456789012345678901234567890",
     "987654321098765432109876543210",
     "1111111110111111111011111111100"],
    ["cong hai so mot chu so", "1", "1", "2"],
    ["cong gay nho tran het chieu dai", "999999999", "1", "1000000000"],
    ["cong khac do dai lon", "48", "9999999999", "10000000047"],
    ["cong hai so sau chu so", "111111", "222222", "333333"],
]


class TestMyBigNumber(unittest.TestCase):
    def setUp(self) -> None:
        self.big_number = MyBigNumber()

    # test log
    def test_log_khong_rong_sau_khi_tinh(self) -> None:
        self.big_number.sum("48", "79")
        self.assertTrue(len(self.big_number.log) > 0)

    def test_log_duoc_reset_moi_lan_goi_sum(self) -> None:
        self.big_number.sum("48", "79")
        log_lan_1 = list(self.big_number.log)
        self.big_number.sum("1", "1")
        log_lan_2 = self.big_number.log
        self.assertNotEqual(log_lan_1, log_lan_2)

    def test_log_chua_ket_qua_cuoi_cung(self) -> None:
        result = self.big_number.sum("48", "79")
        self.assertTrue(any(result in line for line in self.big_number.log))


def _tao_test_phep_cong(num1: str, num2: str, expected: str):

    def test(self: TestMyBigNumber) -> None:
        self.assertEqual(self.big_number.sum(num1, num2), expected)

    return test


for _index, (_description, _num1, _num2, _expected) in enumerate(ADDITION_CASES, start=1):
    _ten_test = f"test_phep_cong_{_index:02d}_{_description.replace(' ', '_')}"
    setattr(TestMyBigNumber, _ten_test, _tao_test_phep_cong(_num1, _num2, _expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
