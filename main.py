
import logging
import re
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator

from core.big_number import MyBigNumber

STATIC_DIR = Path(__file__).parent / "static"

# ----------------------------------------------------------------------
# Cấu hình logging: in log ra console của server
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("big-number-addition")

app = FastAPI(title="Cộng số nguyên lớn")

NUMBER_PATTERN = re.compile(r"^\d+$")  # chỉ chấp nhận số nguyên không âm


# ----------------------------------------------------------------------
# Schemas
# ----------------------------------------------------------------------
class AddRequest(BaseModel):
    num1: str
    num2: str

    @field_validator("num1", "num2")
    @classmethod
    def validate_number(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Số không được để trống")
        if not NUMBER_PATTERN.match(v):
            raise ValueError(f"'{v}' không phải là số nguyên không âm hợp lệ")
        return v


class AddResponse(BaseModel):
    num1: str
    num2: str
    result: str
    log: List[str]


# ----------------------------------------------------------------------
# API endpoint
# ----------------------------------------------------------------------
@app.post("/calculate", response_model=AddResponse)
def calculate(payload: AddRequest):
    logger.info(f"Nhận yêu cầu cộng: num1={payload.num1}, num2={payload.num2}")
    try:
        big_number = MyBigNumber()
        result = big_number.sum(payload.num1, payload.num2)
        log = big_number.log
    except Exception as e:
        logger.exception("Lỗi khi tính toán")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Kết quả: {result}")
    return AddResponse(num1=payload.num1, num2=payload.num2, result=result, log=log)


# ----------------------------------------------------------------------
# Trang giao diện (HTML + CSS + JS được đặt trong static/index.html)
# ----------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")
