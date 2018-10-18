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


def display_students(conn):
    sql = " SELECT * FROM students"
    cur = conn.cursor()
    cur.execute(sql)
    students=cur.fetchall()
    print(students)
    conn.commit()


def add_fees(conn,details):
    sql = "INSERT INTO fees(id,type,semester,amount) VALUES(?,?,?,?)"
    cursor = conn.cursor()
    cursor.execute(sql,details)
    print('Added fee details')
    conn.commit()


def add_many_fees(conn,details):
    sql = "INSERT INTO fees(id,type,semester,amount) VALUES(?,?,?,?)"
    cursor = conn.cursor()
    cursor.executemany(sql,details)
    print('Added new fee details')
    conn.commit()


def main():
    db_file="./fcaa.db"
    conn = create_connection(db_file)
    # details=("2015BCS0019","Subbu Varma",7,4,2015)
    # add_student(conn,details)
    # fee_details1 = ('HOSTEL5','HOSTEL_FEE',5,21000)
    # fee_details2 = ('TUITION5','TUITION_FEE',5,67500)
    # fee_details3 = ('MESS5','MESS_FEE',5,24000)
    # fee_details4 = ('MISC5','MISCELLANEOUS',5,1000)
    # fee_deails=[fee_details1,fee_details2,fee_details3,fee_details4]
    # add_many_fees(conn,fee_deails)
    display_students(conn)


if __name__=="__main__":
    main()
