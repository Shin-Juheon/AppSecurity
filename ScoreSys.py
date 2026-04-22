import pymysql
import sys

DB_HOST = "192.168.100.20"
DB_USER = "cjulib"
DB_PASS = "security"
DB_PORT = 3306
DB_NAME = "cju"

def main_menu():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,        
            password=DB_PASS,
            port=DB_PORT,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"성공적으로 '{DB_NAME}' 데이터베이스에 접속했습니다!\n")
        
        while True:
            print("--- [ 성적 관리 시스템 ] ---")
            print("1. 전체조회")
            print("2. 번호조회")
            print("3. 성적 추가")
            print("4. 성적 삭제")
            print("5. 성적 수정")
            print("6. 종료")
            print("---------------------------")
            
            choice = input("메뉴 선택: ")
            cursor = conn.cursor()
       
            if choice == '1':
                sql = """
                SELECT g.id_grade, m.name, m.id, g.subject, g.score, g.term, DATE(g.reg_date) as reg_date
                FROM grades g
                JOIN member m ON g.member_seq = m.seq
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                print("\n--- [ 성적 전체 목록 ] ---")
                print(f"{'번호':<4} | {'이름(ID)':<12} | {'과목명':<16} | {'점수':<4} | {'학기':<6} | {'등록일'}")
                print("-" * 75)
                for r in results:
                    name_id = f"{r['name']}({r['id']})"
                    print(f"{r['id_grade']:<4} | {name_id:<12} | {r['subject']:<16} | {r['score']:<4} | {r['term']:<6} | {r['reg_date']}")
                print("-" * 75)
                print("\n")

            elif choice == '2':

                seq = input("조회할 학생 번호(seq) 입력: ")

                cursor.execute("SELECT name, id FROM member WHERE seq = %s", (seq,))
                student = cursor.fetchone()
                
                if student:
                    sql = "SELECT subject, score, term FROM grades WHERE member_seq = %s"
                    cursor.execute(sql, (seq,))
                    grades = cursor.fetchall()

                    print(f"\n--- [ {student['name']} 학생의 성적 리포트 ] ---")
                    print(f"- 아이디: {student['id']}")
                    if grades:
                        print(f"- 학기: {grades[0]['term']}")
                        print("-" * 27)
                        total = 0
                        for i, g in enumerate(grades, 1):
                            print(f"{i}. {g['subject']}: {g['score']}점")
                            total += g['score']
                        print("-" * 27)
                        print(f"평균 점수: {total / len(grades):.1f}점")
                    else:
                        print("등록된 성적이 없습니다.")
                else:
                    print("[알림] 해당 번호의 학생이 존재하지 않습니다.")

            elif choice == '3':
                
                print("\n--- [ 성적 데이터 추가 ] ---")
                seq = input("- 학생 번호(seq) 입력: ")
                subject = input("- 과목명 입력: ")
                score = input("- 점수 입력: ")
                term = input("- 학기 입력(예: 2026-1): ")
                
                cursor.execute("SELECT name FROM member WHERE seq = %s", (seq,))
                student = cursor.fetchone()
                
                if student:
                    sql = "INSERT INTO grades (member_seq, subject, score, term) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (seq, subject, score, term))
                    conn.commit()
                    print(f"\n[시스템] '{student['name']}' 학생의 '{subject}' 성적이 등록되었습니다.")
                else:
                    print("[오류] 존재하지 않는 학생 번호입니다.")

            elif choice == '4':              
                id_grade = input("삭제할 성적의 고유 ID(id_grade) 입력: ")
                cursor.execute("SELECT subject FROM grades WHERE id_grade = %s", (id_grade,))
                result = cursor.fetchone()
                
                if result:
                    delete = input(f"정말로 삭제하시겠습니까? (y/n): ").lower()
                    if delete == 'y':
                        cursor.execute("DELETE FROM grades WHERE id_grade = %s", (id_grade,))
                        conn.commit()
                        print(f"\n[시스템] {id_grade}번 데이터가 삭제되었습니다. (대상: {result['subject']})")
                else:
                    print("[알림] 해당 ID의 데이터가 없습니다.")

            elif choice == '5':               
                id_grade = input("수정할 성적의 고유 ID(id_grade) 입력: ")
                cursor.execute("SELECT subject, score FROM grades WHERE id_grade = %s", (id_grade,))
                result = cursor.fetchone()
                
                if result:
                    print(f"--- 현재 정보: {result['subject']} ({result['score']}점) ---")
                    new_score = input("- 수정할 점수 입력: ")
                    cursor.execute("UPDATE grades SET score = %s WHERE id_grade = %s", (new_score, id_grade))
                    conn.commit()
                    print(f"\n[시스템] 수정 완료되었습니다. ({result['score']}점 -> {new_score}점)")
                else:
                    print("[알림] 해당 ID의 데이터가 없습니다.")

            elif choice == '6':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 입력해주세요.")

    except Exception as e:
        print(f"오류 발생: {e}")
        conn.rollback()
    except pymysql.MySQLError as e:
        print(f"데이터베이스 접속 또는 쿼리 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main_menu()