import sqlite3
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        if conn:
            print("connected!")
        return conn
    except Error as e:
        print(e)

    return None

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


def main():
    db_file="./fcaa.db"
    conn = create_connection(db_file)
    # details=("2016BCS0018","Mannem Srinivas",5,3,2016)
    # add_student(conn,details)
    display_student(conn,'2015BCS0020')
    # remove_student(conn,'2015BCS0019')

    # fee_details1 = ('HOSTEL_FEE',5,21000)
    # fee_details2 = ('TUITION_FEE',5,67500)
    # fee_details3 = ('MESS_FEE',5,24000)
    # fee_details4 = ('MISCELLANEOUS',5,1000)
    # fee_deails=[fee_details1,fee_details2,fee_details3,fee_details4]
    # add_many_fees(conn,fee_deails)
    #
    # display_students(conn)
    #
    # transaction=('HOSTEL_FEE','2015BCS0019',7,21000,'7th Semester hostel fee','2000 balance')
    # add_transaction(conn,transaction)
    #
    # transaction1=('HOSTEL_FEE','2016BCS0018',5,21000,'5th Semester hostel fee',' ')
    # transaction2=('TUITION_FEE','2015BCS0019',7,45000,'7th Semester tuition fee','')
    # transaction3=('MESS_FEE','2015BCS0019',7,21000,'7th Semester mess fee','')
    # transaction4=('MISCELLANEOUS','2015BCS0019',7,1000,'7th Semester miscellaneous fee','')
    # transaction=[transaction2,transaction3,transaction4]
    # add_many_transactions(conn,transaction)


if __name__=="__main__":
    main()
