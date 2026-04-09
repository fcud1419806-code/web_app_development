# 系統架構文件 (Architecture) - 個人記帳簿

## 1. 技術架構說明
本系統定位為輕量化且快速響應的個人記帳應用。為降低開發與部署門檻，我們採用傳統且成熟的伺服器端渲染 (Server-Side Rendering) 架構，不在此階段採用前後端分離，而是利用後端直接處理畫面呈現。

- **後端：Python + Flask**
  選擇 Flask 是因為它是極度輕量、靈活的 Web 框架，十分適合建置簡易的工具類別系統，也能讓我們快速針對 PRD 中的核心 5 大需求進行開發。
- **模板引擎：Jinja2**
  負責將後端處理好的資料（如：總體收支、帳目明細）渲染進寫好的 HTML 檔案中，實現頁面動態資料的展示。
- **資料庫：SQLite**
  因為這是 [個人記帳簿] 且面向學生，無需高頻繁的並行寫入。透過內建的 SQLite，資料可被保存在單一檔案（通常是 `database.db`）中，能大幅減少系統架設的複雜度，也讓日後備份和轉移非常容易。

### Flask MVC 模式說明
- **Model (模型)**：主要包含與資料庫對接的邏輯與 Schema 層，如「帳務紀錄」的讀取、寫入、更新和分類項目管理。
- **View (視圖)**：主要是 `templates` 資料夾內的 Jinja2 HTML 檔案。負責將畫面及整理後的報表資料呈現給使用者觀看。
- **Controller (控制器)**：也就是 Flask 中的 Route (路由)。負責接收使用者從瀏覽器發送過來的請求（例如提交新帳目的表單），接著調用 Model 來進行資料寫入/修改，最後再發送資料給 View 去組合 HTML 並回傳結果。

## 2. 專案資料夾結構

以下為我們即將採用的專案資料夾架構：

```text
web_app_development/
│
├── app/                  # 主要的應用程式邏輯區域
│   ├── __init__.py       # app 初始化（建立 application instance、載入設定）
│   ├── models/           # [Model] 資料庫模型
│   │   └── database.py   # 定義 SQLite 的連線行為與 CRUD 函式
│   ├── routes/           # [Controller] Flask 路由控制
│   │   └── views.py      # 主要路由（首頁、新增、編輯記帳等 API endpoints）
│   ├── templates/        # [View] Jinja2 模板
│   │   ├── base.html     # 各頁面共用的基底設計（導覽列、頁尾）
│   │   ├── index.html    # 首頁（含當週明細與簡易統計）
│   │   └── form.html     # 記帳的輸入表單頁面（新增與編輯共用）
│   └── static/           # 靜態資源
│       ├── css/
│       │   └── style.css # 共用樣式表（含顏色佈景與字體設定等響應式設計）
│       └── js/
│           └── script.js # 前端互動腳本（如表單驗證、操作確認）
│
├── instance/             # 環境配置或本地特有資料（不加入 git 版本控制）
│   └── database.db       # SQLite 資料庫檔案
│
├── docs/                 # 開發文件管理
│   ├── PRD.md            # 產品需求文件
│   └── ARCHITECTURE.md   # 本架構文件
│
├── requirements.txt      # Python 套件依賴清單
└── app.py                # 應用程式的進入點（啟動伺服器用）
```

## 3. 元件關係圖

以下展示從使用者存取網站到背後資料讀寫的數據流向：

```mermaid
flowchart LR
    User[使用者 (瀏覽器)]
    
    subgraph 伺服器端
    Route[Flask 路由\n(Controller)]
    Tpl[Jinja2 模板\n(View)]
    Model[資料存取邏輯\n(Model)]
    end
    
    DB[(SQLite 資料庫)]
    
    User -- "HTTP Request\n(新增、編輯、查閱)" --> Route
    Route -- "調用函式" --> Model
    Model -- "執行 SQL 查詢/更新" --> DB
    DB -- "回傳資料" --> Model
    Model -- "回傳轉換後的資料" --> Route
    Route -- "傳送變數給模板" --> Tpl
    Tpl -- "渲染後的 HTML" --> Route
    Route -- "HTTP Response" --> User
```

## 4. 關鍵設計決策

1. **單體式架構 (Monolithic Structure)**
   - **原因**：對於單一且規模不大的記帳網頁，不須強行拆分前端專案（如 React/Vue）與後端 API。單體式開發能有效減少跨網域問題、加快初期開發速度，使專案更容易管理。
2. **SQLite 作為唯一持久化存儲**
   - **原因**：為了減輕部署困擾，選擇無需安裝任何額外伺服器的 SQLite。使用者的每一筆紀錄都記錄在單一檔案內，讀取統計的速度也完全足以應付日常個人記帳情況。
3. **基礎的 MVC 邏輯分離**
   - **原因**：雖然這個專案較為簡單，但透過將「路由邏輯」、「資料庫連結」與「HTML視圖」拆分成三個區塊，就算未來的記帳本需要擴增功能（例如：年度報表、分類長條圖匯出等），也能清楚找到對應要修改的地方。
