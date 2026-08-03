import json


STATE_FILE = "state.json"


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

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, quiz_data):
        question = quiz_data["question"]
        choices = quiz_data["choices"]
        answer = quiz_data["answer"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("퀴즈 문제가 올바르지 않습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")

        if not all(
            isinstance(choice, str) and choice.strip()
            for choice in choices
        ):
            raise ValueError("선택지가 올바르지 않습니다.")

        if not isinstance(answer, int) or answer < 1 or answer > 4:
            raise ValueError("정답은 1부터 4 사이의 숫자여야 합니다.")

        return cls(question, choices, answer)


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


def save_state(quizzes, best_result):
    state = {
        "quizzes": [
            quiz.to_dict()
            for quiz in quizzes
        ],
        "best_result": best_result
    }

    try:
        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=4
            )
    except OSError as error:
        print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            state = json.load(file)

        quiz_data_list = state["quizzes"]
        best_result = state.get("best_result")

        if not isinstance(quiz_data_list, list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        quizzes = [
            Quiz.from_dict(quiz_data)
            for quiz_data in quiz_data_list
        ]

        if best_result is not None:
            validate_best_result(best_result)

        print(
            f"📂 저장된 데이터를 불러왔습니다. "
            f"(퀴즈 {len(quizzes)}개)"
        )

        return quizzes, best_result

    except FileNotFoundError:
        print("📂 저장된 파일이 없어 기본 퀴즈를 사용합니다.")
        return create_default_quizzes(), None

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError
    ):
        print("⚠️ 저장 파일이 손상되어 기본 데이터로 복구합니다.")
        return create_default_quizzes(), None

    except OSError as error:
        print(f"⚠️ 저장 파일을 읽지 못했습니다: {error}")
        print("기본 데이터를 사용합니다.")

        return create_default_quizzes(), None


def validate_best_result(best_result):
    if not isinstance(best_result, dict):
        raise ValueError("최고 점수 형식이 올바르지 않습니다.")

    score = best_result["score"]
    correct_count = best_result["correct_count"]
    total_count = best_result["total_count"]

    if not all(
        isinstance(value, int)
        for value in [score, correct_count, total_count]
    ):
        raise ValueError("최고 점수 값이 올바르지 않습니다.")

    if score < 0 or score > 100:
        raise ValueError("점수 범위가 올바르지 않습니다.")

    if correct_count < 0 or correct_count > total_count:
        raise ValueError("정답 개수가 올바르지 않습니다.")

    if total_count <= 0:
        raise ValueError("전체 문제 수가 올바르지 않습니다.")


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


def play_quizzes(quizzes, best_result):
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return best_result

    correct_count = 0
    total_count = len(quizzes)

    print()
    print(f"📝 퀴즈를 시작합니다! (총 {total_count}문제)")

    for index, quiz in enumerate(quizzes, start=1):
        print()
        print("-" * 40)
        print(f"[문제 {index}]")

        quiz.display()

        user_answer = get_number_input(
            "정답 입력: ",
            1,
            4
        )

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            correct_count += 1
        else:
            print(
                f"❌ 오답입니다. "
                f"정답은 {quiz.answer}번입니다."
            )

    score = int(correct_count / total_count * 100)

    print()
    print("=" * 40)
    print(
        f"🏆 결과: {total_count}문제 중 "
        f"{correct_count}문제 정답! ({score}점)"
    )

    if best_result is None or score > best_result["score"]:
        best_result = {
            "score": score,
            "correct_count": correct_count,
            "total_count": total_count
        }

        print("🎉 새로운 최고 점수입니다!")

    print("=" * 40)

    return best_result


def add_quiz(quizzes):
    print()
    print("📌 새로운 퀴즈를 추가합니다.")

    question = get_text_input("문제를 입력하세요: ")
    choices = []

    for index in range(1, 5):
        choice = get_text_input(f"선택지 {index}: ")
        choices.append(choice)

    answer = get_number_input(
        "정답 번호 (1-4): ",
        1,
        4
    )

    new_quiz = Quiz(
        question,
        choices,
        answer
    )

    quizzes.append(new_quiz)

    print()
    print("✅ 퀴즈가 추가되었습니다!")
    print(
        f"현재 등록된 퀴즈는 "
        f"총 {len(quizzes)}개입니다."
    )


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


def show_best_score(best_result):
    print()

    if best_result is None:
        print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
        return

    print("=" * 40)
    print(
        f"🏆 최고 점수: {best_result['score']}점 "
        f"({best_result['total_count']}문제 중 "
        f"{best_result['correct_count']}문제 정답)"
    )
    print("=" * 40)


def main():
    quizzes, best_result = load_state()

    try:
        while True:
            print_menu()
            choice = get_menu_choice()

            if choice == 1:
                best_result = play_quizzes(
                    quizzes,
                    best_result
                )

                save_state(quizzes, best_result)

            elif choice == 2:
                add_quiz(quizzes)
                save_state(quizzes, best_result)

            elif choice == 3:
                show_quiz_list(quizzes)

            elif choice == 4:
                show_best_score(best_result)

            else:
                save_state(quizzes, best_result)
                print("퀴즈 게임을 종료합니다.")
                break

    except (KeyboardInterrupt, EOFError):
        print()
        print("⚠️ 프로그램 종료 요청을 확인했습니다.")

        save_state(quizzes, best_result)

        print("데이터를 저장하고 안전하게 종료합니다.")


if __name__ == "__main__":
    main()