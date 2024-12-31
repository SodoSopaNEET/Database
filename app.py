from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import IntegrityError

app = Flask(__name__)

# 資料庫連接
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'testdb',
    'port': '3307'
}
db = mysql.connector.connect(**db_config)

# 員工管理頁面
@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    cursor = db.cursor(dictionary=True)
    error_message = None  # 用於顯示錯誤訊息

    if request.method == 'POST':
        # 新增員工
        employee_id = request.form['EmployeeId']
        name = request.form['Name']
        rank = request.form['Rank']
        salary = request.form['Salary']
        phone = request.form['Phone']
        gender = request.form['Gender']
        birth_date = request.form['BirthDate']
        hire_date = request.form['HireDate']
        address = request.form['Address']

        # 檢查是否已存在相同身分證字號的記錄
        cursor.execute("SELECT * FROM employee WHERE EmployeeID = %s", (employee_id,))
        existing_employee = cursor.fetchone()

        if existing_employee:
            # 如果存在，顯示錯誤訊息
            error_message = f"身分證字號 {employee_id} 已存在，無法重複新增！"
        else:
            try:
                # 插入新員工記錄
                cursor.execute(
                    "INSERT INTO employee (EmployeeID, Name, `Rank`, Salary, Phone, Gender, BirthDate, HireDate, Address) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (employee_id, name, rank, salary, phone, gender, birth_date, hire_date, address)
                )
                db.commit()
                return redirect(url_for('manage_employees'))
            except Exception as e:
                # 捕捉任何其他異常
                error_message = f"新增員工時發生錯誤：{str(e)}"

    # 查詢功能
    query_field = request.args.get('query_field')
    query_value = request.args.get('query_value')

    if query_field and query_value:
        # 使用 LIKE 支持模糊查詢
        query = f"SELECT * FROM employee WHERE {query_field} LIKE %s AND status='正常'"
        cursor.execute(query, (f"%{query_value}%",))
    else:
        # 顯示所有正常的員工
        cursor.execute("SELECT * FROM employee WHERE status='正常'")

    employees = cursor.fetchall()
    return render_template('employees.html', employees=employees, error_message=error_message)


@app.route('/employees/edit/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        # 獲取表單數據
        name = request.form.get('Name')
        rank = request.form.get('Rank')
        salary = request.form.get('Salary')
        phone = request.form.get('Phone')
        gender = request.form.get('Gender')
        birth_date = request.form.get('BirthDate')
        hire_date = request.form.get('HireDate')
        address = request.form.get('Address')
        status = request.form.get('Status')

        # 更新數據
        cursor.execute("""
            UPDATE employee
            SET Name = %s, `Rank` = %s, Salary = %s, Phone = %s, Gender = %s,
                BirthDate = %s, HireDate = %s, Address = %s, Status = %s
            WHERE EmployeeID = %s
        """, (name, rank, salary, phone, gender, birth_date, hire_date, address, status, employee_id))
        db.commit()
        return redirect(url_for('manage_employees'))

    # 查詢員工數據
    cursor.execute("SELECT * FROM employee WHERE EmployeeID = %s", (employee_id,))
    employee = cursor.fetchone()
    return render_template('edit_employee.html', employee=employee)

@app.route('/employees/delete/<employee_id>', methods=['POST'])
def delete_employee(employee_id):
    cursor = db.cursor()
    # 將員工狀態設為「離職」而非實際刪除
    cursor.execute("UPDATE employee SET Status = '離職' WHERE EmployeeID = %s", (employee_id,))
    db.commit()
    return redirect(url_for('manage_employees'))


@app.route('/countries', methods=['GET', 'POST'])
def manage_countries():
    cursor = db.cursor(dictionary=True)
    error_message = None  # 用於顯示錯誤訊息

    if request.method == 'POST':
        # 新增國家資料
        country_code = request.form['CountryCode']
        country_name = request.form['CountryName']
        continent = request.form['Continent']
        head_of_state = request.form['HeadOfState']
        foreign_minister = request.form['ForeignMinister']
        contact_person = request.form['ContactPerson']
        population = request.form['Population']
        area = request.form['Area']
        phone = request.form['Phone']
        is_ally = request.form['IsAlly']
        status = '正常'

        # 檢查是否已存在相同國家代碼的記錄
        cursor.execute("SELECT * FROM country WHERE CountryCode = %s", (country_code,))
        existing_country = cursor.fetchone()

        if existing_country:
            # 如果存在，顯示錯誤訊息
            error_message = f"國家代碼 {country_code} 已存在，無法重複新增！"
        else:
            try:
                # 插入新國家記錄
                cursor.execute(
                    "INSERT INTO country (CountryCode, CountryName, Continent, HeadOfState, ForeignMinister, ContactPerson, Population, Area, Phone, IsAlly, Status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (country_code, country_name, continent, head_of_state, foreign_minister, contact_person, population, area, phone, is_ally, status)
                )
                db.commit()
                return redirect(url_for('manage_countries'))
            except Exception as e:
                # 捕捉任何其他異常
                error_message = f"新增國家時發生錯誤：{str(e)}"

    # 查詢功能
    query_field = request.args.get('query_field')
    query_value = request.args.get('query_value')

    if query_field and query_value:
        # 使用 LIKE 支持模糊查詢
        query = f"SELECT * FROM country WHERE {query_field} LIKE %s AND Status='正常'"
        cursor.execute(query, (f"%{query_value}%",))
    else:
        # 顯示所有正常的國家
        cursor.execute("SELECT * FROM country WHERE Status='正常'")

    countries = cursor.fetchall()
    return render_template('countries.html', countries=countries, error_message=error_message)



@app.route('/countries/edit/<country_code>', methods=['GET', 'POST'])
def edit_country(country_code):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        # 獲取更新數據
        country_name = request.form.get('CountryName')
        continent = request.form.get('Continent')
        head_of_state = request.form.get('HeadOfState')
        foreign_minister = request.form.get('ForeignMinister')
        contact_person = request.form.get('ContactPerson')
        population = request.form.get('Population')
        area = request.form.get('Area')
        phone = request.form.get('Phone')
        is_ally = request.form.get('IsAlly') == '是'
        status = request.form.get('Status')

        # 更新數據庫
        cursor.execute("""
            UPDATE country
            SET CountryName = %s, Continent = %s, HeadOfState = %s, ForeignMinister = %s,
                ContactPerson = %s, Population = %s, Area = %s, Phone = %s, IsAlly = %s, Status = %s
            WHERE CountryCode = %s
        """, (country_name, continent, head_of_state, foreign_minister, contact_person,
              population, area, phone, is_ally, status, country_code))
        db.commit()
        return redirect(url_for('manage_countries'))

    # 查詢需要修改的國家數據
    cursor.execute("SELECT * FROM country WHERE CountryCode = %s", (country_code,))
    country = cursor.fetchone()
    return render_template('edit_country.html', country=country)

@app.route('/countries/delete/<country_code>', methods=['POST'])
def delete_country(country_code):
    cursor = db.cursor()
    cursor.execute("DELETE FROM country WHERE CountryCode = %s", (country_code,))
    db.commit()
    return redirect(url_for('manage_countries'))


@app.route('/dependents', methods=['GET', 'POST'])
def manage_dependents():
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # 新增眷屬資料
        employee_id = request.form['EmployeeID']
        dependent_id = request.form['DependentID']
        dependent_name = request.form['DependentName']
        gender = request.form['Gender']
        relation = request.form['Relation']
        birth_date = request.form['BirthDate']
        status = '正常'
        cursor.execute(
            "INSERT INTO dependent (EmployeeID, DependentID, DependentName, Gender, Relation, BirthDate, Status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (employee_id, dependent_id, dependent_name, gender, relation, birth_date, status)
        )
        db.commit()
        return redirect(url_for('manage_dependents'))

    # 查詢功能
    query_field = request.args.get('query_field')
    query_value = request.args.get('query_value')

    if query_field and query_value:
        # 使用 LIKE 支持模糊查詢
        query = f"SELECT * FROM dependent WHERE {query_field} LIKE %s AND Status='正常'"
        cursor.execute(query, (f"%{query_value}%",))
    else:
        # 顯示所有正常的眷屬資料
        cursor.execute("SELECT * FROM dependent WHERE Status='正常'")

    dependents = cursor.fetchall()
    return render_template('dependents.html', dependents=dependents)


@app.route('/dependents/edit/<employee_id>/<dependent_id>', methods=['GET', 'POST'])
def edit_dependent(employee_id, dependent_id):
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # 提交表單後更新數據
        dependent_name = request.form.get('DependentName')
        gender = request.form.get('Gender')
        relation = request.form.get('Relation')
        birth_date = request.form.get('BirthDate')
        status = request.form.get('Status')

        cursor.execute("""
            UPDATE dependent
            SET DependentName = %s, Gender = %s, Relation = %s, BirthDate = %s, Status = %s
            WHERE EmployeeID = %s AND DependentID = %s
        """, (dependent_name, gender, relation, birth_date, status, employee_id, dependent_id))
        db.commit()
        return redirect(url_for('manage_dependents'))

    # 加載需要修改的數據
    cursor.execute("""
        SELECT * FROM dependent WHERE EmployeeID = %s AND DependentID = %s
    """, (employee_id, dependent_id))
    dependent = cursor.fetchone()

    # 傳遞正確的變數名稱
    return render_template('edit_dependent.html', dependent=dependent)


@app.route('/dependents/delete/<employee_id>/<dependent_id>', methods=['POST'])
def delete_dependent(employee_id, dependent_id):
    cursor = db.cursor()
    # 將眷屬狀態設為「已刪除」而非實際刪除
    cursor.execute("""
        UPDATE dependent SET Status = '已刪除' WHERE EmployeeID = %s AND DependentID = %s
    """, (employee_id, dependent_id))
    db.commit()
    return redirect(url_for('manage_dependents'))


@app.route('/assignments', methods=['GET', 'POST'])
def manage_assignments():
    cursor = db.cursor(dictionary=True)
    error_message = None

    if request.method == 'POST':
        # 從表單獲取數據
        employee_id = request.form.get('EmployeeID')
        country_code = request.form.get('CountryCode')
        start_date = request.form.get('StartDate')
        ambassador = request.form.get('Ambassador')
        status = request.form.get('Status')

        # 檢查該員工是否已被派駐至其他國家且狀態為“正常”
        cursor.execute("""
            SELECT * FROM assignment
            WHERE EmployeeID = %s AND Status = '正常'
        """, (employee_id,))
        existing_assignment = cursor.fetchone()

        if existing_assignment:
            # 如果找到符合條件的派駐記錄，返回錯誤訊息
            error_message = f"員工 {employee_id} 已被派駐至國家代碼 {existing_assignment['CountryCode']}，無法同時派駐多個國家！"
        else:
            try:
                # 插入新派駐記錄
                cursor.execute("""
                    INSERT INTO assignment (EmployeeID, CountryCode, StartDate, Ambassador, Status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (employee_id, country_code, start_date, ambassador, status))
                db.commit()
                return redirect(url_for('manage_assignments'))
            except IntegrityError as e:
                # 捕獲 IntegrityError 並檢查是否是重複鍵錯誤
                if e.errno == 1062:  # Duplicate entry
                    error_message = "該員工已經被派駐至其他國家，無法同時派駐多個國家！"

    # 獲取所有派駐資料
    cursor.execute("""
        SELECT a.EmployeeID, e.Name AS EmployeeName, a.CountryCode, a.StartDate, a.Ambassador, a.Status
        FROM assignment a
        JOIN employee e ON a.EmployeeID = e.EmployeeID
        WHERE a.Status = '正常'
    """)
    assignments = cursor.fetchall()

    return render_template('assignments.html', assignments=assignments, error_message=error_message)

@app.route('/employees/options', methods=['GET'])
def get_employee_options():
    cursor = db.cursor(dictionary=True)
    # 獲取所有正常的員工身份證字號和姓名
    cursor.execute("SELECT EmployeeID, Name FROM employee WHERE Status = '正常'")
    employees = cursor.fetchall()
    return jsonify(employees)

@app.route('/assignments/edit/<employee_id>/<country_code>', methods=['GET', 'POST'])
def edit_assignment(employee_id, country_code):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        start_date = request.form['StartDate']
        ambassador = request.form['Ambassador']
        status = request.form['Status']
        cursor.execute(
            "UPDATE assignment SET StartDate=%s, Ambassador=%s, Status=%s "
            "WHERE EmployeeID=%s AND CountryCode=%s",
            (start_date, ambassador, status, employee_id, country_code)
        )
        db.commit()
        return redirect(url_for('manage_assignments'))

    cursor.execute("SELECT * FROM assignment WHERE EmployeeID=%s AND CountryCode=%s", (employee_id, country_code))
    assignment = cursor.fetchone()
    return render_template('edit_assignment.html', assignment=assignment)

@app.route('/assignments/delete/<employee_id>/<country_code>', methods=['POST'])
def delete_assignment(employee_id, country_code):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE assignment SET Status='刪除' WHERE EmployeeID=%s AND CountryCode=%s",
        (employee_id, country_code)
    )
    db.commit()
    return redirect(url_for('manage_assignments'))


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    cursor = db.cursor(dictionary=True)
    result = None

    if request.method == 'POST':
        query_type = request.form.get('query_type')

        if query_type == 'country_30_above':
            country = request.form.get('country')
            cursor.execute("""
                SELECT COUNT(*) AS employee_count
                FROM employee e
                JOIN assignment a ON e.EmployeeID = a.EmployeeID
                WHERE a.CountryCode = (SELECT CountryCode FROM country WHERE CountryName = %s)
                  AND TIMESTAMPDIFF(YEAR, e.BirthDate, CURDATE()) > 30
                  AND a.Status = '正常'
            """, (country,))
            result = cursor.fetchone()
            result = f"派駐於 {country} 且年齡超過30歲的員工人數為 {result['employee_count']} 人。"

        elif query_type == 'continent_employee_count':
            continent = request.form.get('continent')
            cursor.execute("""
                SELECT COUNT(DISTINCT a.EmployeeID) AS employee_count
                FROM employee e
                JOIN assignment a ON e.EmployeeID = a.EmployeeID
                JOIN country c ON a.CountryCode = c.CountryCode
                WHERE c.Continent = %s
                  AND a.Status = '正常'
            """, (continent,))
            result = cursor.fetchone()
            result = f"派駐於 {continent} 洲的員工總數為 {result['employee_count']} 人。"

        elif query_type == 'average_dependent_age':
            cursor.execute("""
                SELECT AVG(TIMESTAMPDIFF(YEAR, d.BirthDate, CURDATE())) AS avg_age
                FROM dependent d
                JOIN employee e ON d.EmployeeID = e.EmployeeID
                WHERE TIMESTAMPDIFF(YEAR, e.BirthDate, CURDATE()) > 30
                  AND d.Status = '正常'
            """)
            result = cursor.fetchone()
            result = f"30歲以上員工的平均眷屬年齡為 {result['avg_age']:.2f} 歲。"

        elif query_type == 'average_dependent_count':
            cursor.execute("""
                SELECT AVG(dependent_count) AS avg_dependents
                FROM (
                    SELECT COUNT(d.DependentID) AS dependent_count
                    FROM dependent d
                    JOIN employee e ON d.EmployeeID = e.EmployeeID
                    WHERE TIMESTAMPDIFF(YEAR, e.BirthDate, CURDATE()) > 30
                      AND d.Status = '正常'
                    GROUP BY d.EmployeeID
                ) AS subquery
            """)
            result = cursor.fetchone()
            result = f"30歲以上員工的平均眷屬人數為 {result['avg_dependents']:.2f} 人。"

    return render_template('statistics.html', result=result)


    return render_template('statistics.html', result=result)
@app.route('/statistics/query/continent', methods=['GET'])
def query_continent():
    # 獲取查詢參數
    continent = request.args.get('continent')
    cursor = db.cursor(dictionary=True)  # 修改為 dictionary 模式
    # 執行 SQL 查詢
    cursor.execute("""
        SELECT COUNT(DISTINCT a.EmployeeID) AS EmployeeCount
        FROM assignment a
        JOIN country c ON a.CountryCode = c.CountryCode
        WHERE c.Continent = %s AND a.Status = '正常'
    """, (continent,))
    result = cursor.fetchone()
    # 返回查詢結果
    if result and result['EmployeeCount'] is not None:
        return render_template('statistics.html', result=f"派駐於 {continent} 的員工總數為 {result['EmployeeCount']} 人。")
    else:
        return render_template('statistics.html', result=f"查無派駐於 {continent} 的員工數據。")


# 首頁
@app.route('/')
def index():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(host='10.147.19.10', port=5000, debug=True)
    

