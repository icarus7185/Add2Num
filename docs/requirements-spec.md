# Software Requirements Specification — Add2Num

| Item | Value |
|---|---|
| Product | Add2Num — Big Integer Addition Web App |
| Document type | Software Requirements Specification (SRS) |
| Version | 1.1 |
| Date | 2026-09-24 |
| Status | Reviewed against source code — for sign-off |
| Author | Business Analysis |
| Related documents | [README.md](../README.md), [coding-rules.md](coding-rules.md) |

---

## 1. Introduction

### 1.1 Purpose

This document defines the business, functional and non-functional requirements for **Add2Num**, a web application that adds two arbitrarily large non-negative integers using the elementary-school column method (digit by digit, right to left, with carry) and shows a step-by-step log of the calculation.

It is the reference for development, testing and acceptance. Every requirement has a unique ID so it can be traced to code and test cases. Version 1.1 has been checked against the source code; see [Section 10](#10-review-log-v11).

### 1.2 Scope

**In scope**

- A single-page web UI to enter two numbers and view the sum and calculation log.
- A JSON HTTP API (`POST /calculate`) that performs the addition.
- A reusable, framework-independent calculation library (`core` package, class `MyBigNumber`).
- Input validation in the UI, the API and the library.
- Step-by-step calculation logging, with a safety limit for very large inputs.
- An automated unit test suite for the calculation library.

**Out of scope (v1.1)**

- Operations other than addition (subtraction, multiplication, division, etc.).
- Negative numbers, decimals, fractions, scientific notation, digit separators (`,` `.` `_` spaces), non-ASCII digits.
- User accounts, authentication, persistence or calculation history.
- Localization other than Vietnamese.
- Public hosting concerns: TLS, input size limits, rate limiting, CORS, monitoring (see Q-01).
- Mobile-optimized layout (see Q-04).
- Automated API and UI tests.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| Big integer | A non-negative integer whose number of digits is not limited by native numeric types. |
| Digit string | A non-empty string made only of the ASCII characters `0`–`9`. |
| Column addition | Adding digits of the same position from right to left and carrying 1 to the next position when the column total is ≥ 10. |
| Carry | The value (0 or 1) moved to the next column on the left. |
| Step | One column addition recorded in the calculation log. |
| Calculation log | The ordered list of human-readable messages describing how the result was produced. |
| `LOG_STEP_LIMIT` | The maximum number of digits for which per-step logging is produced (default 10,000). |

### 1.4 Stakeholders and users

| Stakeholder | Interest |
|---|---|
| End user (student / learner) | Enter two numbers, get the correct sum, understand how it was calculated. |
| API consumer (developer / other system) | Call the calculation over HTTP and receive a structured result. |
| Developer | Reuse `MyBigNumber` independently of the web layer; maintain code under the coding rules. |
| QA | Verify behavior against clear acceptance criteria. |

---

## 2. Overall Description

### 2.1 Product context

```
┌──────────────┐   POST /calculate (JSON)   ┌──────────────────┐   sum(a, b)   ┌────────────────────┐
│  Browser UI  │ ─────────────────────────► │  FastAPI (main)  │ ────────────► │ core.MyBigNumber   │
│ static/index │ ◄───────────────────────── │  validation, API │ ◄──────────── │ validation, algo,  │
└──────────────┘   {result, log} / error    └──────────────────┘  result, log  │ calculation log    │
                                                    │                          └────────────────────┘
                                                    └── server console log (Python logging)
```

- `core` is a Git submodule (branch `core`) and must stay independent of any web framework.
- The web layer (`main.py`) owns HTTP, request validation and error mapping.
- The UI (`static/index.html`) is plain HTML/CSS/JS served by `GET /`.

### 2.2 Operating environment

- Python 3.12 or later, FastAPI ≥ 0.110, Uvicorn ≥ 0.29, Pydantic ≥ 2.0.
- A modern evergreen desktop browser (Chrome, Edge, Firefox, Safari).
- Run locally with `uvicorn main:app --host 127.0.0.1 --port 8000` from the project root.

### 2.3 Assumptions

- A-01: Users enter numbers by typing or pasting plain text.
- A-02: The application runs on a trusted local machine; it is not exposed to the internet.
- A-03: UI text and log messages are in Vietnamese; this document is in English and quotes that text verbatim.

---

## 3. Business Rules

| ID | Rule |
|---|---|
| BR-01 | Only non-negative integers written with the ASCII digits `0`–`9` are accepted. |
| BR-02 | An empty or whitespace-only input is invalid. |
| BR-03 | Leading zeros are allowed in input and are ignored in the calculation (`007` is treated as `7`; `000` as `0`). |
| BR-04 | The result must be the exact mathematical sum, with no leading zeros, except that a zero sum is shown as `0`. |
| BR-05 | The addition must be done digit by digit from right to left with carry. Converting the whole string to a native integer type to compute the sum is not allowed. |
| BR-06 | There is no business limit on the number of digits. Detailed per-step logging is only produced when the longer number (after removing leading zeros) has at most `LOG_STEP_LIMIT` digits. |

---

## 4. Functional Requirements

Priority uses MoSCoW: **M** = Must, **S** = Should.

### 4.1 Calculation library (`core.MyBigNumber`)

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The library shall provide class `MyBigNumber` with method `sum(stn1: str, stn2: str, verbose_log: bool = True) -> str` that returns the sum of two digit strings as a digit string. | M |
| FR-02 | `sum()` shall remove leading zeros from each input before adding, keeping at least one digit (BR-03). | M |
| FR-03 | `sum()` shall add digits from right to left, carrying to the next column, and handle numbers of different lengths (BR-05). | M |
| FR-04 | When one number runs out of digits and the carry is 0, `sum()` shall copy the remaining leading part of the longer number to the result in one operation instead of adding each digit with 0. | S |
| FR-05 | When a final carry remains after the leftmost column, `sum()` shall add it as a new leading digit (e.g. `999 + 1 = 1000`). | M |
| FR-06 | `sum()` shall reset `MyBigNumber.log` to an empty list at the start of every call so logs from different calls never mix. | M |
| FR-07 | `sum()` shall reject any input that is not a digit string (BR-01, BR-02) by raising `ValueError` with the message `'<value>' không phải là số nguyên không âm hợp lệ`. It does not trim whitespace and does not use `assert`. | M |
| FR-08 | The library shall use Python `logging` (logger `big-number-addition`), not `print()`, for diagnostics. | M |

### 4.2 Calculation log

| ID | Requirement | Priority |
|---|---|---|
| FR-10 | The first log entry shall state the two normalized operands: `Bắt đầu cộng: <a> + <b>`. | M |
| FR-11 | When per-step logging is active, each column where both numbers have a digit shall produce one entry, numbered from 1: `Bước <n>: <da> + <db>[ (cộng thêm nhớ)] = <digit>[, nhớ <carry>].` The text `(cộng thêm nhớ)` appears only when a carry came **in** from the previous column; `, nhớ <carry>` appears only when a carry goes **out** to the next column. | M |
| FR-12 | Each step in the carry-propagation phase (only one number has digits left and a carry came in) shall produce `Bước <n>: <d> + nhớ = <digit>[, nhớ <carry>].` | M |
| FR-13 | When the remaining digits of the longer number are copied unchanged (FR-04), one unnumbered entry shall say so: `Hết nhớ, giữ nguyên phần còn lại '<digits>' của số dài hơn.` | S |
| FR-14 | The last log entry shall always be `Kết quả cuối cùng: <result>`. | M |
| FR-15 | If the longer normalized operand has more than `LOG_STEP_LIMIT` digits, step entries (FR-11 to FR-13) shall be skipped and a single notice added after the first entry explaining that detailed logging was skipped to save memory and time. | M |
| FR-16 | If `verbose_log=False`, the log shall contain only the start entry (FR-10) and the final entry (FR-14). This option is available in the library only, not through the API. | S |
| FR-17 | `LOG_STEP_LIMIT` shall be a class-level constant, default `10_000`, and overridable per instance for testing. | S |
| FR-18 | Each step entry (FR-11 to FR-13) shall also be written to the `big-number-addition` logger at INFO level. | S |

### 4.3 HTTP API

| ID | Requirement | Priority |
|---|---|---|
| FR-20 | The system shall expose `POST /calculate` accepting JSON `{"num1": string, "num2": string}`. | M |
| FR-21 | The server shall trim leading/trailing whitespace from `num1` and `num2`, then check that each is non-empty and matches `^\d+$`. | M |
| FR-22 | On success the API shall return HTTP 200 with `{"num1", "num2", "result", "log"}` where `num1`/`num2` are the trimmed inputs (leading zeros kept), `result` is the sum and `log` is the calculation log (array of strings). | M |
| FR-23 | When a field is missing, not a string, empty or does not match `^\d+$`, the API shall return HTTP 422 in FastAPI's standard validation format (`detail` is an array; each item has `loc` and `msg`). For the two custom checks `msg` contains `Số không được để trống` or `'<value>' không phải là số nguyên không âm hợp lệ`. | M |
| FR-24 | If `MyBigNumber.sum()` raises any exception, the API shall return HTTP 400 with `{"detail": "<exception message>"}` and log the error with stack trace on the server. Example: non-ASCII digits (e.g. `١٢٣`) pass the FR-21 pattern but are rejected by FR-07, giving HTTP 400. | M |
| FR-25 | The server shall log each request (full operands) and each result to the console at INFO level. | S |
| FR-26 | `GET /` shall return the web UI (`static/index.html`) as `text/html; charset=utf-8`. | M |

### 4.4 Web UI

| ID | Requirement | Priority |
|---|---|---|
| FR-30 | The page shall show a title, a short description of the method, two labelled input fields (`Số thứ nhất`, `Số thứ hai`) with example placeholders, and a `Tính` (Calculate) button. | M |
| FR-31 | On submit, the UI shall validate each input before calling the API, first field first: empty or whitespace-only → `<field>: không được để trống.`; any character other than `0`–`9` (including spaces) → `<field>: ký tự "<c>" ở vị trí <pos> không hợp lệ. Chỉ được nhập các chữ số 0-9.` (first invalid character, 1-based position). If a check fails, no request is sent. | M |
| FR-32 | While a request is in progress the `Tính` button shall be disabled, and re-enabled when the request completes or fails. | M |
| FR-33 | On success the UI shall show the result in a prominent block and the calculation log in a scrollable block, each log line prefixed with `›`. | M |
| FR-34 | On a client validation error, an API error with a text `detail`, or a network error, the UI shall show the message in the error box and hide the previous result. | M |
| FR-35 | Very long results shall wrap within the result block and never cause horizontal page scrolling. | M |
| FR-36 | Submitting the form (button or Enter key) shall not reload the page. | M |

> Note: the UI check (FR-31) is stricter than the API check (FR-21), so the UI never triggers an HTTP 422.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement | Priority |
|---|---|---|---|
| NFR-01 | Correctness | For all valid inputs the result shall equal the mathematically exact sum. | M |
| NFR-02 | Performance | `sum()` shall run in O(n) time and memory, n = length of the longer operand, without reversing or padding the inputs. | M |
| NFR-03 | Performance | A request with two 10,000-digit numbers shall return within 1 second on a typical developer laptop (measured: ~0.04 s). | S |
| NFR-04 | Performance | A request with two 1,000,000-digit numbers shall complete without running out of memory, because of FR-15 (measured: ~0.6 s, 3 log entries). | S |
| NFR-05 | Reusability | `core` shall not import FastAPI, Pydantic or any web-framework module. | M |
| NFR-06 | Maintainability | Code in `core` shall follow [coding-rules.md](coding-rules.md), including: no broad `except Exception` in `core`. | M |
| NFR-07 | Testability | `tests/test_core.py` shall run standalone (`python tests/test_core.py`) and print one line per test case, ending with `OK` when all pass. | M |
| NFR-08 | Testability | Addition test data shall be table-driven (description, num1, num2, expected) so new cases can be added without writing new test functions. | S |
| NFR-09 | Usability | All messages written by this application (UI, custom validation, calculation log) shall be in Vietnamese. Pydantic's built-in messages (e.g. `Field required`) stay in English. | M |
| NFR-10 | Security | The UI shall render API data as text (`textContent`), never as HTML, to prevent script injection. | M |

---

## 6. Interface Specification

### 6.1 `POST /calculate`

**Request**

```json
{ "num1": "19", "num2": "11" }
```

**Response 200**

```json
{
  "num1": "19",
  "num2": "11",
  "result": "30",
  "log": [
    "Bắt đầu cộng: 19 + 11",
    "Bước 1: 9 + 1 = 0, nhớ 1.",
    "Bước 2: 1 + 1 (cộng thêm nhớ) = 3.",
    "Kết quả cuối cùng: 30"
  ]
}
```

**Error responses**

| HTTP | When | Body example |
|---|---|---|
| 422 | Missing field, non-string value, empty or non-`\d` input | `{"detail": [{"type": "value_error", "loc": ["body", "num1"], "msg": "Value error, '-5' không phải là số nguyên không âm hợp lệ", ...}]}` |
| 400 | `MyBigNumber.sum()` raised an exception | `{"detail": "'١٢٣' không phải là số nguyên không âm hợp lệ"}` |

### 6.2 `GET /`

Returns the HTML page. No parameters.

---

## 7. Use Cases

### UC-01 — Add two numbers from the web UI

- **Actor:** End user
- **Precondition:** Server is running; user opens `http://127.0.0.1:8000`.
- **Main flow:**
  1. User enters the first and second number.
  2. User clicks `Tính` or presses Enter.
  3. UI validates both inputs (FR-31).
  4. UI disables the button and sends `POST /calculate` (FR-32).
  5. Server validates, calculates and returns result and log.
  6. UI shows the result and log (FR-33) and re-enables the button.
- **Alternative flows:**
  - 3a. Input invalid → UI shows the validation message; no request is sent.
  - 5a. Server returns an error or the network fails → UI shows the error message (FR-34).

### UC-02 — Call the calculation API

- **Actor:** API consumer
- **Main flow:** Consumer sends `POST /calculate` with JSON body → receives HTTP 200 with result and log.
- **Alternative flows:** Invalid body → HTTP 422 (FR-23); input rejected by the library → HTTP 400 (FR-24).

---

## 8. Acceptance Criteria

| ID | Given / When / Then | Covers |
|---|---|---|
| AC-01 | Given `2` and `3`, when summed, then result is `5`. | FR-01 |
| AC-02 | Given `999` and `1`, then result is `1000` and the log is: `Bước 1: 9 + 1 = 0, nhớ 1.`, `Bước 2: 9 + nhớ = 0, nhớ 1.`, `Bước 3: 9 + nhớ = 0, nhớ 1.` between the start and final entries. | FR-03, FR-05, FR-11, FR-12 |
| AC-03 | Given `0` and `0`, then result is `0`. | BR-04 |
| AC-04 | Given `0` + `123` and `123` + `0`, then result is `123` in both cases. | FR-03 |
| AC-05 | Given `007` and `013`, then result is `20` and the first log entry is `Bắt đầu cộng: 7 + 13`. | FR-02, FR-10 |
| AC-06 | Given `123456789012345678901234567890` and `987654321098765432109876543210`, then result is `1111111110111111111011111111100`. | NFR-01 |
| AC-07 | Given `999` and `1000001` with `verbose_log=False`, then result is `1001000` and the log has exactly 2 entries. | FR-04, FR-16 |
| AC-08 | Given `LOG_STEP_LIMIT = 0` and inputs `123`, `456`, then the log contains the "skipped detailed logging" notice and no `Bước` entries. | FR-15 |
| AC-09 | Given two consecutive calls on the same instance, then the log of the second call contains no entries from the first. | FR-06 |
| AC-10 | For any successful call, the last log entry contains the final result. | FR-14 |
| AC-11 | Given `19` and `11`, then the log contains `Bước 1: 9 + 1 = 0, nhớ 1.` and `Bước 2: 1 + 1 (cộng thêm nhớ) = 3.` | FR-11 |
| AC-12 | Given any of `-5`, `""`, `12a`, `" 12"`, `١٢٣` passed directly to `sum()`, then `ValueError` is raised. | FR-07 |
| AC-13 | Given API body `{"num1": " 12 ", "num2": "3"}`, then HTTP 200 with `num1 = "12"` and `result = "15"`. | FR-21, FR-22 |
| AC-14 | Given API body `{"num1": "-5", "num2": "3"}`, then HTTP 422 and `msg` contains `'-5' không phải là số nguyên không âm hợp lệ`. | FR-23 |
| AC-15 | Given API body `{"num1": "", "num2": "3"}`, then HTTP 422 and `msg` contains `Số không được để trống`. | FR-23 |
| AC-16 | Given API body `{"num1": "١٢٣", "num2": "1"}`, then HTTP 400 with `detail` = `'١٢٣' không phải là số nguyên không âm hợp lệ`. | FR-24 |
| AC-17 | Given two 20,000-digit numbers via the API, then HTTP 200 with the correct result and a log of 3 entries (start, skip notice, final). | FR-15, NFR-04 |
| AC-18 | In the UI, given `12a4` in the first field, then the message is `Số thứ nhất: ký tự "a" ở vị trí 3 không hợp lệ. Chỉ được nhập các chữ số 0-9.` and no request is sent. | FR-31 |
| AC-19 | In the UI, while a request is pending, the `Tính` button is disabled. | FR-32 |
| AC-20 | In the UI, a 1,000-digit result wraps inside the result block without horizontal page scroll. | FR-35 |

---

## 9. Traceability and Verification

| Acceptance criteria | Verified by |
|---|---|
| AC-01 | `test_phep_cong_01_cong_don_gian_khong_nho` |
| AC-02 | `test_phep_cong_02_cong_co_nho_lan_truyen_lien_tiep` (result); log checked manually |
| AC-03, AC-04 | `test_phep_cong_03..05_cong_voi_so_0_*` |
| AC-05 | `test_phep_cong_06_cong_so_co_so_0_thua_o_dau` (result); log checked manually |
| AC-06 | `test_phep_cong_07_cong_so_nguyen_rat_lon` |
| AC-07 | `test_tat_log_chi_tiet_khi_verbose_log_false` |
| AC-08 | `test_log_tom_tat_khi_vuot_nguong_do_dai` |
| AC-09 | `test_log_duoc_reset_moi_lan_goi_sum` |
| AC-10 | `test_log_chua_ket_qua_cuoi_cung`, `test_log_khong_rong_sau_khi_tinh` |
| AC-11 | `test_log_ghi_cong_them_nho_theo_nho_tu_cot_truoc` |
| AC-12 | `test_dau_vao_khong_hop_le_bi_tu_choi` |
| AC-13 to AC-17 | Manual check with FastAPI `TestClient` on 2026-09-24 — passed |
| AC-18 to AC-20 | Manual check in the browser |

---

## 10. Review Log (v1.1)

Version 1.0 was checked against the source code. The rule was: **change the spec to match the code where possible, drop requirements that are not essential, and change code only for real defects.**

### 10.1 Code changes (defects)

| # | Defect found | Why the code had to change | Change |
|---|---|---|---|
| D-01 | The step log was wrong for normal UI input: `19 + 11` logged `Bước 2: 1 + 1 = 3.`, and `5 + 5` logged `(cộng thêm nhớ)` although no carry came in. The label depended on the outgoing carry instead of the incoming carry. | The step log is the core purpose of the product; it showed wrong arithmetic to users. | `core/big_number.py`: label now depends on the incoming carry (FR-11). Test added. |
| D-02 | `MyBigNumber.sum()` did not validate input: `sum("-5", "3")` returned `-8`, `sum(" 12", "3")` returned `" 15"`. Via the API, `"١٢٣" + "1"` passed the `\d` check and returned `"١٢4"` (HTTP 200 with a wrong result). | Wrong results with no error, reachable through the public API; also required by coding-rules.md. | `core/big_number.py`: `sum()` raises `ValueError` for non-digit-string input (FR-07). The API returns 400 through the existing handler (FR-24). Test added. |

### 10.2 Spec changes (code kept as is)

| v1.0 item | Decision |
|---|---|
| FR-23 (422 message text) | Reworded to match Pydantic's output: `msg` is prefixed with `Value error, `; built-in messages are in English. |
| FR-24 / NFR-14 (broad `except Exception` in `main.py`) | Kept current behavior: every calculation error → 400. The "no broad except" rule applies to `core` only (coding-rules.md scope), which complies. |
| FR-25 / NFR-12 (truncate large values in server logs) | Dropped. Local tool (A-02); coding-rules.md applies to `core`, and `main.py` logging is acceptable as is. |
| FR-31 vs FR-21 (UI rejects spaces, API trims them) | Both behaviors documented as intended. The UI is stricter, so no user impact. |
| FR-34 / G-05 (`[object Object]` for 422 in the UI) | Not reachable from the UI because FR-31 is stricter than FR-21. Scope of FR-34 narrowed to text `detail`. |
| NFR-02 ("no unnecessary copies") | Reworded to measurable O(n) wording. |
| NFR-03, NFR-04 | Kept; measured values added. |
| NFR-11 (all messages Vietnamese) | Scoped to messages written by this application (now NFR-09). |

### 10.3 Requirements removed

| v1.0 item | Reason |
|---|---|
| NFR-05 — maximum input length / request size | Not needed for a local tool (A-02). Moved to Q-01. |
| NFR-10 — phone-width usability (missing viewport tag) | Not needed for v1.1. Moved to Q-04. |
| NFR-15 — portability across OSes | Not tested and not a business need; environment is described in 2.2. |
| G-08 — automated API/UI tests | Not essential; API criteria were verified manually (Section 9). |

---

## 11. Open Questions

| # | Question | Owner |
|---|---|---|
| Q-01 | Will the app ever be deployed publicly? If yes, add requirements for a maximum input length, request size limit, TLS, rate limiting and CORS. | Tech Lead |
| Q-02 | Should the API expose `verbose_log` so consumers can turn off detailed logs? | Product Owner |
| Q-03 | Should the log be localized (English/Vietnamese) or stay Vietnamese only? | Product Owner |
| Q-04 | Is phone use needed? If yes, add a viewport meta tag and a mobile layout requirement. | UX |
| Q-05 | Is a "copy result" button needed for very long results? | UX |

---

## 12. Approval

| Role | Name | Date | Signature |
|---|---|---|---|
| Product Owner | | | |
| Tech Lead | | | |
| QA Lead | | | |
| Business Analyst | | | |
