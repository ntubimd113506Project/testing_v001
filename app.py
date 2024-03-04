#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template,request
from utils import db

#-----------------------
# 產生一個Flask物件
#-----------------------
app = Flask(__name__)

def get_total_pages():
    # 連接資料庫
    connection = db.get_connection()
    cursor = connection.cursor()

    # 使用 COUNT 函數獲取總行數
    cursor.execute("SELECT COUNT(*) FROM product")
    total_rows = cursor.fetchone()[0]

    # 關閉資料庫連線
    cursor.close()
    connection.close()

    # 計算總頁數
    per_page = 10
    total_pages = (total_rows // per_page) + (1 if total_rows % per_page > 0 else 0)

    return total_pages

#-----------------------
# 定義app的路由
#-----------------------
@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/product/list/')
def product_list():
     # 獲取分頁參數
    page = int(request.args.get('page', 1))
    per_page = 10

    # 連接資料庫
    connection = db.get_connection()
    cursor = connection.cursor()

    # 執行 SQL 查詢，包括 JOIN 以獲取 product 和 protype 資料
    query = """
        SELECT p.prono, p.proname, p.price, t.typename
        FROM product p
        JOIN protype t ON p.typno = t.typno
        ORDER BY p.price ASC
        LIMIT %s OFFSET %s
    """
    offset = (page - 1) * per_page
    cursor.execute(query, (per_page, offset))
    products = cursor.fetchall()

    # 關閉資料庫連線
    cursor.close()
    connection.close()

    total_pages = get_total_pages()

    # 傳遞資料給模板並渲染
    return render_template('product_list.html', products=products, page=page, total_pages=total_pages)

@app.route('/supplier/list')
def supplier_list():
    # 連接資料庫
    connection = db.get_connection()
    cursor = connection.cursor()

    # 執行 SQL 查詢
    query = """
        SELECT supno, supname, contactor, tel, fax
        FROM supplier
        ORDER BY supno
    """
    cursor.execute(query)
    suppliers = cursor.fetchall()

    # 關閉資料庫連線
    cursor.close()
    connection.close()

    # 獲取分頁參數
    page = int(request.args.get('page', 1))
    per_page = 20

    # 計算總頁數
    total_pages = (len(suppliers) // per_page) + (1 if len(suppliers) % per_page > 0 else 0)

    # 選取要顯示的供應商資料
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    displayed_suppliers = suppliers[start_index:end_index]

    # 傳遞資料給模板並渲染
    return render_template('supplier_list.html', suppliers=displayed_suppliers, page=page, total_pages=total_pages)

#-----------------------
# 啟勳app
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)