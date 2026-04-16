# 路由設計文件 (ROUTES) - 個人記帳簿

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁與歷史明細 | GET | `/` | `templates/index.html` | 顯示所有記帳明細列表與總結餘、總收支 |
| 新增記帳頁面 | GET | `/add` | `templates/form.html` | 顯示新增記帳項目表單 |
| 建立記帳紀錄 | POST | `/add` | — | 接收新增表單，存入 `transactions` 資料表，成功後重導向至首頁 |
| 編輯記帳頁面 | GET | `/edit/<int:id>` | `templates/form.html` | 顯示編輯表單，並帶入該筆原始資料 |
| 更新記帳紀錄 | POST | `/edit/<int:id>` | — | 接收編輯表單，更新資料庫，成功後重導向至首頁 |
| 刪除記帳紀錄 | POST | `/delete/<int:id>` | — | 刪除對應 ID 的紀錄，完成後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (`GET /`)
- **輸入**：無。
- **處理邏輯**：
  1. 呼叫 `TransactionModel.get_all()` 取得所有歷程紀錄。
  2. 計算所有收入 (`income`) 與支出 (`expense`) 總和，推導出結餘。
- **輸出**：渲染 `index.html`，傳入總結餘、總收入、總支出與歷史紀錄清單。
- **錯誤處理**：若資料庫連線異常，回傳基本的錯誤頁面或文字訊息。

### 新增記帳頁面 (`GET /add`)
- **輸入**：無。
- **處理邏輯**：準備新建立表單所需呈現的基本資訊。
- **輸出**：渲染 `form.html`。
- **錯誤處理**：無特殊錯誤，直接顯示空表單。

### 建立記帳紀錄 (`POST /add`)
- **輸入**：
  - `title` (文字)
  - `amount` (數字)
  - `type` (收入或支出字串)
  - `category` (分類字串)
  - `date` (YYYY-MM-DD 日期字串)
- **處理邏輯**：
  1. 驗證資料是否完整、Amount 是否 >= 0。
  2. 呼叫 `TransactionModel.create()` 將資料存入。
- **輸出**：302 重導向至 `/`。
- **錯誤處理**：若欄位不符規定或驗證失敗，依據 Flash 訊息回傳給原表單頁 `form.html`，並保留原輸入。

### 編輯記帳頁面 (`GET /edit/<int:id>`)
- **輸入**：URL 上的 `id` 參數。
- **處理邏輯**：呼叫 `TransactionModel.get_by_id(id)` 抓出該紀錄的資料。
- **輸出**：渲染 `form.html` 並在欄位中帶入預設值。
- **錯誤處理**：若查無此 `id`，直接 `abort(404)`。

### 更新記帳紀錄 (`POST /edit/<int:id>`)
- **輸入**：URL 上的 `id` 與表單資料 (`title`, `amount`, `type`, `category`, `date`)。
- **處理邏輯**：
  1. 驗證資料必填與數值範圍。
  2. 呼叫 `TransactionModel.update()` 更新指定 ID 紀錄。
- **輸出**：302 重導向至 `/`。
- **錯誤處理**：檢查必填與格式，若錯誤則攜帶失敗訊息渲染同頁表單；若 `id` 不存在，則 `abort(404)`。

### 刪除記帳紀錄 (`POST /delete/<int:id>`)
- **輸入**：URL 上的 `id`。
- **處理邏輯**：呼叫 `TransactionModel.delete(id)` 進行刪除。
- **輸出**：302 重導向至 `/`。
- **錯誤處理**：若刪除對象不存在，不影響系統或返回首頁並提示刪除失敗。

## 3. Jinja2 模板清單

這部分預計放置在 `app/templates/`。

- `base.html`
  - 角色：整個網站共用的外框 (包含 HTML `<head>` 區塊、共同樣式表載入、導覽列與頁尾)。
- `index.html` (繼承 `base.html`)
  - 角色：首頁與總覽，呈現結餘卡片與交易明細清單，並包含每筆明細的編輯與刪除按鈕。
- `form.html` (繼承 `base.html`)
  - 角色：新增與編輯共用的表單頁。透過 Jinja2 控制若傳入特定變數（如 `transaction`）即為編輯狀態，否則為新增狀態。

## 4. 路由骨架程式碼
請參考 `app/routes/views.py`。
