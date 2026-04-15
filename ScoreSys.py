# 메인 메뉴 루프
def main_menu():
    while True:
        print("\n--- [ 성적 관리 시스템 ] ---")
        print("1. 전체조회")
        print("2. 번호조회")
        print("3. 성적 추가")
        print("4. 성적 삭제")
        print("5. 성적 수정")
        print("6. 종료")
        print("---------------------------")
        
        choice = input("메뉴 선택: ")
        
        if choice == '1':
            select_all()
        elif choice == '2':
            select_one()
        elif choice == '3':
            insert_member()
        elif choice == '4':
            delete_member()
        elif choice == '5':
            update_member()
        elif choice == '6':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main_menu()