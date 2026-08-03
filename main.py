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


def create_default_quizzes():
    return [
        Quiz(
            "Python에서 여러 값을 순서대로 저장하는 자료형은 무엇인가요?",
            ["int", "list", "bool", "str"],
            2
        ),
        Quiz(
            "Python에서 조건문을 작성할 때 사용하는 키워드는 무엇인가요?",
            ["if", "for", "def", "class"],
            1
        ),
        Quiz(
            "Python에서 함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            ["func", "method", "def", "return"],
            3
        ),
        Quiz(
            "Python에서 반복 횟수가 정해져 있을 때 주로 사용하는 반복문은 무엇인가요?",
            ["if", "try", "while", "for"],
            4
        ),
        Quiz(
            "Python 클래스의 생성자 역할을 하는 메서드는 무엇인가요?",
            ["__main__", "__init__", "__start__", "__class__"],
            2
        )
    ]


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


def get_number_input(message, min_value, max_value):
    while True:
        user_input = input(message).strip()

        if not user_input:
            print("⚠️ 값을 입력해 주세요.")
            continue

        try:
            number = int(user_input)
        except ValueError:
            print(
                f"⚠️ {min_value}부터 {max_value} 사이의 "
                "숫자를 입력해 주세요."
            )
            continue

        if number < min_value or number > max_value:
            print(
                f"⚠️ {min_value}부터 {max_value} 사이의 "
                "숫자를 입력해 주세요."
            )
            continue

        return number


def get_text_input(message):
    while True:
        user_input = input(message).strip()

        if not user_input:
            print("⚠️ 빈 값은 입력할 수 없습니다.")
            continue

        return user_input


def get_menu_choice():
    return get_number_input("선택: ", 1, 5)


def play_quizzes(quizzes):
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return

    score = 0
    total_count = len(quizzes)

    print()
    print(f"📝 퀴즈를 시작합니다! (총 {total_count}문제)")

    for index, quiz in enumerate(quizzes, start=1):
        print()
        print("-" * 40)
        print(f"[문제 {index}]")

        quiz.display()

        user_answer = get_number_input("정답 입력: ", 1, 4)

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    percentage = int(score / total_count * 100)

    print()
    print("=" * 40)
    print(
        f"🏆 결과: {total_count}문제 중 "
        f"{score}문제 정답! ({percentage}점)"
    )
    print("=" * 40)


def add_quiz(quizzes):
    print()
    print("📌 새로운 퀴즈를 추가합니다.")

    question = get_text_input("문제를 입력하세요: ")

    choices = []

    for index in range(1, 5):
        choice = get_text_input(f"선택지 {index}: ")
        choices.append(choice)

    answer = get_number_input("정답 번호 (1-4): ", 1, 4)

    new_quiz = Quiz(question, choices, answer)
    quizzes.append(new_quiz)

    print()
    print("✅ 퀴즈가 추가되었습니다!")
    print(f"현재 등록된 퀴즈는 총 {len(quizzes)}개입니다.")


def show_quiz_list(quizzes):
    print()

    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return

    print(f"📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)

    for index, quiz in enumerate(quizzes, start=1):
        print(f"[{index}] {quiz.question}")

    print("-" * 40)


def main():
    quizzes = create_default_quizzes()

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            play_quizzes(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            show_quiz_list(quizzes)
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