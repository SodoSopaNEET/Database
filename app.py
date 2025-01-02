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
        status = request.form.get('Status')  # 獲取新的狀態

        # 更新資料庫中的記錄
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
        country = request.form.get('country')
        continent = request.form.get('continent')
        rank = request.form.get('rank')
        is_ally = request.form.get('is_ally')

        # 員工統計
        if query_type == 'employee_count':
            cursor.execute("SELECT COUNT(*) AS employee_count FROM employee WHERE Status='正常'")
            result = cursor.fetchone()
            result = f"員工總數為 {result['employee_count']} 人。"

        elif query_type == 'employee_average_age_salary':
            cursor.execute("""
                SELECT AVG(TIMESTAMPDIFF(YEAR, BirthDate, CURDATE())) AS avg_age,
                       AVG(Salary) AS avg_salary
                FROM employee
                WHERE Status='正常'
            """)
            result = cursor.fetchone()
            result = f"平均年齡為 {result['avg_age']:.2f} 歲，平均薪資為 {result['avg_salary']:.2f} 元。"

        elif query_type == 'employee_rank_group':
            cursor.execute("""
                SELECT `Rank`, COUNT(*) AS rank_count
                FROM employee
                WHERE Status='正常'
                GROUP BY `Rank`
            """)
            results = cursor.fetchall()
            result = "依職等分群統計：<br>" + "<br>".join([f"{row['Rank']} 職等：{row['rank_count']} 人" for row in results])

        elif query_type == 'employee_total_salary':
            cursor.execute("""
                SELECT SUM(Salary) AS total_salary,
                       SUM(Salary) / 12 AS monthly_salary,
                       SUM(Salary) / 52 AS weekly_salary
                FROM employee
                WHERE Status='正常'
            """)
            result = cursor.fetchone()
            result = (f"全年總薪資為 {result['total_salary']:.2f} 元，"
                      f"每月平均薪資為 {result['monthly_salary']:.2f} 元，"
                      f"每周平均薪資為 {result['weekly_salary']:.2f} 元。")

        # 國家統計
        elif query_type == 'ally_count':
            cursor.execute("""
                SELECT SUM(IsAlly) AS ally_count, COUNT(*) - SUM(IsAlly) AS non_ally_count
                FROM country
            """)
            result = cursor.fetchone()
            result = f"邦交國共有 {result['ally_count']} 個，非邦交國共有 {result['non_ally_count']} 個。"

        elif query_type == 'continent_ally':
            cursor.execute("""
                SELECT SUM(IsAlly) AS ally_count, COUNT(*) - SUM(IsAlly) AS non_ally_count
                FROM country
                WHERE Continent=%s
            """, (continent,))
            result = cursor.fetchone()
            result = f"{continent} 洲中邦交國共有 {result['ally_count']} 個，非邦交國共有 {result['non_ally_count']} 個。"

        elif query_type == 'population_by_ally':
            if is_ally == '1':
                cursor.execute("""
                    SELECT SUM(Population) AS population
                    FROM country
                    WHERE IsAlly = 1
                """)
                result = cursor.fetchone()
                result = f"所有邦交國的總國民人數為 {result['population']} 人。"
            else:
                cursor.execute("""
                    SELECT SUM(Population) AS population
                    FROM country
                    WHERE IsAlly = 0
                """)
                result = cursor.fetchone()
                result = f"所有非邦交國的總國民人數為 {result['population']} 人。"

        # 派駐統計
        elif query_type == 'country_employee_count':
            cursor.execute("""
                SELECT CountryName, COUNT(*) AS employee_count
                FROM assignment a
                JOIN country c ON a.CountryCode = c.CountryCode
                WHERE a.Status='正常'
                GROUP BY c.CountryName
            """)
            results = cursor.fetchall()
            result = "每個國家派駐員工總數如下：<br>" + "<br>".join(
                [f"{row['CountryName']}：{row['employee_count']} 人" for row in results])


        # 眷屬統計
        elif query_type == 'average_dependent_age_gender':
            cursor.execute("""
                SELECT AVG(TIMESTAMPDIFF(YEAR, BirthDate, CURDATE())) AS avg_age,
                       AVG(CASE WHEN Gender='男' THEN TIMESTAMPDIFF(YEAR, BirthDate, CURDATE()) END) AS avg_male_age,
                       AVG(CASE WHEN Gender='女' THEN TIMESTAMPDIFF(YEAR, BirthDate, CURDATE()) END) AS avg_female_age
                FROM dependent
                WHERE Status='正常'
            """)
            result = cursor.fetchone()
            result = (f"眷屬平均年齡為 {result['avg_age']:.2f} 歲，"
                      f"男眷屬平均年齡為 {result['avg_male_age']:.2f} 歲，"
                      f"女眷屬平均年齡為 {result['avg_female_age']:.2f} 歲。")

        elif query_type == 'dependent_gender_count':
            cursor.execute("""
                SELECT SUM(Gender='男') AS male_count, SUM(Gender='女') AS female_count
                FROM dependent
                WHERE Status='正常'
            """)
            result = cursor.fetchone()
            result = (f"男眷屬人數為 {result['male_count']} 人，"
                      f"女眷屬人數為 {result['female_count']} 人。")

    return render_template('statistics.html', result=result)





# 首頁
@app.route('/')
def index():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(host='10.147.19.10', port=5000, debug=True)
    

