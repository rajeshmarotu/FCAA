import sqlite3

'''
    Database connection
'''
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        if conn:
            print("connected!")
        return conn
    except Error as e:
        print(e)

    return None


'''
    Student module
'''

def add_student(conn,details):
    sql = "INSERT INTO students(student_id,name,semester,year,year_of_joining) VALUES(?,?,?,?,?)";
    cursor = conn.cursor()
    cursor.execute(sql,details)
    print('Added new student details')
    conn.commit()

def remove_student(conn,regno):
    sql = "DELETE FROM students WHERE student_id=?"
    cursor = conn.cursor()
    cursor.execute(sql,(regno,))
    print('Removed student with regno %s',(regno))
    conn.commit()

def display_student(conn,regno):
    sql = "SELECT * FROM students WHERE student_id=?"
    cursor = conn.cursor()
    cursor.execute(sql,(regno,))
    details = cursor.fetchone()
    print(details)
    conn.commit()

def display_students(conn):
    sql = " SELECT * FROM students"
    cursor = conn.cursor()
    cursor.execute(sql)
    students=cursor.fetchall()
    print(students)
    conn.commit()


'''
    Fee module
'''
def add_fees(conn,details):
    sql = "INSERT INTO fees(type,semester,amount) VALUES(?,?,?)"
    cursor = conn.cursor()
    cursor.execute(sql,details)
    print('Added fee details')
    conn.commit()


def add_many_fees(conn,details):
    sql = "INSERT INTO fees(type,semester,amount) VALUES(?,?,?)"
    cursor = conn.cursor()
    cursor.executemany(sql,details)
    print('Added new fee details')
    conn.commit()


'''
    Transaction module
'''

def add_transaction(conn,details):
    sql = "INSERT INTO transactions(fee_type,student_id,semester,amount,description,remarks) VALUES(?,?,?,?,?,?)"
    cursor = conn.cursor()
    cursor.execute(sql,details)
    print('Added new transaction')
    conn.commit()

def add_many_transactions(conn,details):
    sql = "INSERT INTO transactions(fee_type,student_id,semester,amount,description,remarks) VALUES(?,?,?,?,?,?)"
    cursor = conn.cursor()
    cursor.executemany(sql,details)
    print('Added new transactions')
    conn.commit()

'''
    Query functions
'''
def know_who_paid_type(conn,fee_type,semester):
    sql = "SELECT students.student_id,students.name,students.semester FROM students INNER JOIN ( SELECT transactions.student_id as student_id FROM transactions INNER JOIN fees ON transactions.fee_type = fees.type AND transactions.semester = fees.semester WHERE transactions.fee_type=? AND transactions.semester =? AND (fees.amount-transactions.amount)==0) as fee_transaction ON fee_transaction.student_id = students.student_id"
    cursor = conn.cursor()
    cursor.execute(sql,(fee_type,semester,))
    details = cursor.fetchall()
    print("Semester %s tudents who have paid %s"%(semester,fee_type))
    print(details)

def know_who_not_paid_type(conn,fee_type,semester):
    sql = "SELECT students.name,fee_transaction.balance FROM students INNER JOIN ( SELECT transactions.student_id as student_id, (fees.amount-transactions.amount) as balance FROM transactions INNER JOIN fees ON transactions.fee_type = fees.type AND transactions.semester = fees.semester WHERE transactions.fee_type=? AND transactions.semester =? AND (fees.amount-transactions.amount)!=0) as fee_transaction ON fee_transaction.student_id = students.student_id"
    cursor = conn.cursor()
    cursor.execute(sql,(fee_type,semester,))
    details = cursor.fetchall()
    print("Semester %s tudents who have not paid %s yet"%(semester,fee_type))
    print(details)

def people_paid_whole_fee(conn,semester):
    sql = "SELECT student_list.student_id, student_list.name, student_list.amount as balance FROM (SELECT semester, SUM(amount) as amount FROM fees GROUP BY semester ORDER BY semester) as fees INNER JOIN  (SELECT students.student_id, students.semester as semester,students.name, amount FROM students INNER JOIN (SELECT semester, student_id, SUM(amount) as amount FROM transactions WHERE semester=? GROUP BY semester,student_id)as transactions ON students.student_id=transactions.student_id) as student_list ON fees.semester=student_list.semester WHERE fees.amount=student_list.amount"
    cursor = conn.cursor()
    cursor.execute(sql,(semester,))
    details = cursor.fetchall()
    print("People who have paid full fee in semester %d "%(semester,))
    print(details)

def people_with_balance_fee(conn,semester):
    sql = "SELECT student_list.student_id, student_list.name,(fees.amount-student_list.amount) as balance FROM (SELECT semester, SUM(amount) as amount FROM fees GROUP BY semester ORDER BY semester) as fees INNER JOIN  (SELECT students.student_id, students.semester as semester,students.name, amount FROM students INNER JOIN (SELECT semester, student_id, SUM(amount) as amount FROM transactions WHERE semester=? GROUP BY semester,student_id)as transactions ON students.student_id=transactions.student_id) as student_list ON fees.semester=student_list.semester WHERE fees.amount!=student_list.amount"
    cursor = conn.cursor()
    cursor.execute(sql,(semester,))
    details = cursor.fetchall()
    print("People with balance fees in semester %d "%(semester,))
    print(details) 

def main():
    db_file="./fcaa.db"
    conn = create_connection(db_file)
    details=("2016BCS0018","Mannem Srinivas",5,3,2016)
    add_student(conn,details)
    display_student(conn,'2015BCS0020')
    remove_student(conn,'2015BCS0019')

    fee_details1 = ('HOSTEL_FEE',5,21000)
    fee_details2 = ('TUITION_FEE',5,67500)
    fee_details3 = ('MESS_FEE',5,24000)
    fee_details4 = ('MISCELLANEOUS',5,1000)
    fee_deails=[fee_details1,fee_details2,fee_details3,fee_details4]
    add_many_fees(conn,fee_deails)

    display_students(conn)

    transaction=('HOSTEL_FEE','2015BCS0019',7,21000,'7th Semester hostel fee','2000 balance')
    add_transaction(conn,transaction)

    transaction1=('HOSTEL_FEE','2016BCS0018',5,21000,'5th Semester hostel fee',' ')
    transaction2=('TUITION_FEE','2015BCS0019',7,45000,'7th Semester tuition fee','')
    transaction3=('MESS_FEE','2015BCS0019',7,21000,'7th Semester mess fee','')
    transaction4=('MISCELLANEOUS','2015BCS0019',7,1000,'7th Semester miscellaneous fee','')
    transaction=[transaction2,transaction3,transaction4]
    add_many_transactions(conn,transaction)

    know_who_paid_type(conn,'HOSTEL_FEE',5)
    know_who_not_paid_type(conn,'TUITION_FEE',7)
    people_paid_whole_fee(conn,7)
    people_with_balance_fee(conn,7)


if __name__=="__main__":
    main()
