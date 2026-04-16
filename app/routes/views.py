from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.database import TransactionModel

# 建立名為 'views' 的 Blueprint，以便在主程式 app.py 中註冊
views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def index():
    """
    [首頁與歷程明細]
    - 取得所有歷史歷程紀錄 (TransactionModel.get_all)
    - 計算總收入、總支出與當前結餘
    - 渲染 templates/index.html 顯示資料
    """
    pass

@views.route('/add', methods=['GET'])
def add_transaction_page():
    """
    [新增記帳頁面]
    - 呈現空白的新增記帳表單
    - 渲染 templates/form.html
    """
    pass

@views.route('/add', methods=['POST'])
def add_transaction_submit():
    """
    [建立記帳紀錄]
    - 接收表單傳入的 title, amount, type, category, date
    - 進行輸入驗證 (確認資料是否存在及格式是否正確，大於零)
    - 呼叫 TransactionModel.create 存進 DB
    - 成功後重導向回首頁 /
    """
    pass

@views.route('/edit/<int:id>', methods=['GET'])
def edit_transaction_page(id):
    """
    [編輯記帳頁面]
    - 根據 URL 傳入的 id 呼叫 TransactionModel.get_by_id 取得紀錄
    - 若紀錄不存在則 abort(404)
    - 將紀錄資料傳入並渲染 templates/form.html，讓畫面填寫既有數值
    """
    pass

@views.route('/edit/<int:id>', methods=['POST'])
def edit_transaction_submit(id):
    """
    [更新記帳紀錄]
    - 接收表單更新的值 (title, amount, type, category, date)
    - 判斷目標 id 是否存在以及表單驗證
    - 執行 TransactionModel.update
    - 成功後重導向回首頁 /
    """
    pass

@views.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    """
    [刪除記帳紀錄]
    - HTTP 表單只能送 GET/POST，因此這裡透過 POST 進行刪除
    - 呼叫 TransactionModel.delete(id) 將該筆紀錄刪除
    - 成功後重導向回首頁 /
    """
    pass
