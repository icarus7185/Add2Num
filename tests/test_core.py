"""
Unit test cho module big_number.py (MyBigNumber).

Chạy độc lập từ thư mục gốc project:
    python tests/test_core.py
"""

import sys
import unittest
from pathlib import Path

# Thêm thư mục gốc project vào sys.path để import được package core
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.big_number import MyBigNumber

# Dữ liệu test dạng bảng: [mô tả, num1, num2, kết quả mong đợi]
ADDITION_CASES = [
    ["cong don gian khong nho", "2", "3", "5"],
    ["cong co nho lan truyen lien tiep", "999", "1", "1000"],
    ["cong voi so 0 - ca hai deu 0", "0", "0", "0"],
    ["cong voi so 0 - so dau la 0", "0", "123", "123"],
    ["cong voi so 0 - so sau la 0", "123", "0", "123"],
    ["cong so co so 0 thua o dau", "007", "013", "20"],
    ["cong so nguyen rat lon",
     "123456789012345678901234567890",
     "987654321098765432109876543210",
     "1111111110111111111011111111100"],
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

    def test_log_ghi_cong_them_nho_theo_nho_tu_cot_truoc(self) -> None:
        self.big_number.sum("19", "11")
        self.assertIn("Bước 1: 9 + 1 = 0, nhớ 1.", self.big_number.log)
        self.assertIn("Bước 2: 1 + 1 = 3.", self.big_number.log)

    # test du lieu dau vao khong hop le
    def test_dau_vao_khong_hop_le_bi_tu_choi(self) -> None:
        for num1, num2 in [("-5", "3"), ("", "3"), ("12a", "3"), (" 12", "3"), ("١٢٣", "1")]:
            with self.subTest(num1=num1, num2=num2):
                with self.assertRaises(ValueError):
                    self.big_number.sum(num1, num2)

    # test tat log chi tiet (verbose_log=False / vuot nguong LOG_STEP_LIMIT)
    def test_tat_log_chi_tiet_khi_verbose_log_false(self) -> None:
        # So nay khien vong lap chong lan, vong lap con du va buoc gan thang
        # phan con lai deu chay, nhung khong duoc ghi log tung buoc.
        result = self.big_number.sum("999", "1000001", verbose_log=False)
        self.assertEqual(result, "1001000")
        self.assertEqual(len(self.big_number.log), 2)

    def test_log_tom_tat_khi_vuot_nguong_do_dai(self) -> None:
        # Ep nguong ve 0 de mo phong so qua lon, kich hoat nhanh log tom tat
        self.big_number.LOG_STEP_LIMIT = 0
        self.big_number.sum("123", "456")
        self.assertTrue(
            any("bỏ qua log chi tiết" in line for line in self.big_number.log)
        )


def _tao_test_phep_cong(num1: str, num2: str, expected: str):

    def test(self: TestMyBigNumber) -> None:
        self.assertEqual(self.big_number.sum(num1, num2), expected)

    return test


for _index, (_description, _num1, _num2, _expected) in enumerate(ADDITION_CASES, start=1):
    _ten_test = f"test_phep_cong_{_index:02d}_{_description.replace(' ', '_')}"
    setattr(TestMyBigNumber, _ten_test, _tao_test_phep_cong(_num1, _num2, _expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
