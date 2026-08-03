class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print()
        print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        return self.answer == user_answer


def print_menu():
    print()
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
    while True:
        user_input = input("선택: ").strip()

        if not user_input:
            print("⚠️ 값을 입력해 주세요.")
            continue

        try:
            choice = int(user_input)
        except ValueError:
            print("⚠️ 1부터 5 사이의 숫자를 입력해 주세요.")
            continue

        if choice < 1 or choice > 5:
            print("⚠️ 1부터 5 사이의 숫자를 입력해 주세요.")
            continue

        return choice


def main():
    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            print("📝 퀴즈 풀기 기능은 준비 중입니다.")
        elif choice == 2:
            print("📌 퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("📋 퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("🏆 점수 확인 기능은 준비 중입니다.")
        else:
            print("퀴즈 게임을 종료합니다.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 안전하게 종료합니다.")