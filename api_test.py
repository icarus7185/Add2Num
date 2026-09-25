"""
Unit test cho API trong main.py (GET /, POST /calculate).

Chạy độc lập từ thư mục gốc project:
    python api_test.py
"""

import logging
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

# Tắt log của server và của httpx (TestClient) để output gọn, mỗi test case một dòng
logging.getLogger("big-number-addition").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.WARNING)

LOI_SO_KHONG_HOP_LE = "không phải là số nguyên không âm hợp lệ"

# Dữ liệu test dạng bảng: [mô tả, num1, num2, kết quả mong đợi]
SUCCESS_CASES = [
    ["cong don gian khong nho", "2", "3", "5"],
    ["cong co nho lan truyen lien tiep", "999", "1", "1000"],
    ["cong hai so 0", "0", "0", "0"],
    ["cong so co so 0 thua o dau", "007", "013", "20"],
    ["cong so nguyen rat lon",
     "123456789012345678901234567890",
     "987654321098765432109876543210",
     "1111111110111111111011111111100"],
]

# Dữ liệu test dạng bảng: [mô tả, body, field bị lỗi, đoạn msg mong đợi (None = không kiểm tra)]
VALIDATION_ERROR_CASES = [
    ["so am", {"num1": "-5", "num2": "3"}, "num1", f"'-5' {LOI_SO_KHONG_HOP_LE}"],
    ["chuoi rong", {"num1": "", "num2": "3"}, "num1", "Số không được để trống"],
    ["chi co khoang trang", {"num1": "3", "num2": "   "}, "num2", "Số không được để trống"],
    ["co chu cai", {"num1": "12a4", "num2": "3"}, "num1", f"'12a4' {LOI_SO_KHONG_HOP_LE}"],
    ["so thap phan", {"num1": "1.5", "num2": "3"}, "num1", f"'1.5' {LOI_SO_KHONG_HOP_LE}"],
    ["khoang trang o giua", {"num1": "1 2", "num2": "3"}, "num1", f"'1 2' {LOI_SO_KHONG_HOP_LE}"],
    ["thieu field", {"num1": "1"}, "num2", None],
    ["sai kieu - so thay vi chuoi", {"num1": 12, "num2": "3"}, "num1", None],
    ["sai kieu - null", {"num1": None, "num2": "3"}, "num1", None],
]


class TestCalculateApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def post(self, body: dict):
        return self.client.post("/calculate", json=body)

    # test response thanh cong
    def test_response_co_du_cac_field(self) -> None:
        response = self.post({"num1": "19", "num2": "11"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"num1", "num2", "result", "log"})

    def test_log_tra_ve_dung_tung_buoc(self) -> None:
        response = self.post({"num1": "19", "num2": "11"})
        self.assertEqual(
            response.json()["log"],
            [
                "Bắt đầu cộng: 19 + 11",
                "Bước 1: 9 + 1 = 0, nhớ 1.",
                "Bước 2: 1 + 1 (cộng thêm nhớ) = 3.",
                "Kết quả cuối cùng: 30",
            ],
        )

    def test_cat_khoang_trang_hai_dau(self) -> None:
        response = self.post({"num1": " 12 ", "num2": "3"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["num1"], "12")
        self.assertEqual(response.json()["result"], "15")

    def test_giu_nguyen_so_0_o_dau_trong_input_tra_ve(self) -> None:
        body = self.post({"num1": "007", "num2": "013"}).json()
        self.assertEqual((body["num1"], body["num2"]), ("007", "013"))
        self.assertEqual(body["log"][0], "Bắt đầu cộng: 7 + 13")

    def test_so_rat_dai_bo_qua_log_chi_tiet(self) -> None:
        num = "9" * 20_000
        response = self.post({"num1": num, "num2": num})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["result"], "1" + "9" * 19_999 + "8")
        self.assertEqual(len(body["log"]), 3)
        self.assertIn("bỏ qua log chi tiết", body["log"][1])

    # test loi tu thu vien -> HTTP 400
    def test_chu_so_khong_phai_ascii_tra_ve_400(self) -> None:
        response = self.post({"num1": "١٢٣", "num2": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], f"'١٢٣' {LOI_SO_KHONG_HOP_LE}")

    def test_loi_bat_ky_tu_thu_vien_tra_ve_400(self) -> None:
        with patch("main.MyBigNumber") as mock_class:
            mock_class.return_value.sum.side_effect = RuntimeError("lỗi giả lập")
            response = self.post({"num1": "1", "num2": "2"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "lỗi giả lập"})

    # test body khong phai JSON
    def test_body_khong_phai_json_tra_ve_422(self) -> None:
        response = self.client.post(
            "/calculate", content="abc", headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 422)


class TestIndexPage(unittest.TestCase):
    def test_trang_chu_tra_ve_html(self) -> None:
        response = TestClient(app).get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        self.assertIn("<html", response.text.lower())


def _tao_test_thanh_cong(num1: str, num2: str, expected: str):

    def test(self: TestCalculateApi) -> None:
        response = self.post({"num1": num1, "num2": num2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], expected)
        self.assertEqual(response.json()["log"][-1], f"Kết quả cuối cùng: {expected}")

    return test


def _tao_test_loi_validate(body: dict, field: str, expected_msg):

    def test(self: TestCalculateApi) -> None:
        response = self.post(body)
        self.assertEqual(response.status_code, 422)
        errors = response.json()["detail"]
        error = next((e for e in errors if e["loc"] == ["body", field]), None)
        self.assertIsNotNone(error, f"không có lỗi cho field {field}: {errors}")
        if expected_msg is not None:
            self.assertIn(expected_msg, error["msg"])

    return test


for _index, (_description, _num1, _num2, _expected) in enumerate(SUCCESS_CASES, start=1):
    _ten_test = f"test_thanh_cong_{_index:02d}_{_description.replace(' ', '_')}"
    setattr(TestCalculateApi, _ten_test, _tao_test_thanh_cong(_num1, _num2, _expected))

for _index, (_description, _body, _field, _msg) in enumerate(VALIDATION_ERROR_CASES, start=1):
    _ten_test = f"test_loi_422_{_index:02d}_{_description.replace(' ', '_').replace('-', '')}"
    setattr(TestCalculateApi, _ten_test, _tao_test_loi_validate(_body, _field, _msg))


if __name__ == "__main__":
    unittest.main(verbosity=2)
