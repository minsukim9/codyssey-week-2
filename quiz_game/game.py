import random

from .default_quizzes import create_default_quizzes
from .input_handler import read_answer, read_number, read_text
from .quiz import Quiz
from .state_repository import StateDataError, StateRepository


class QuizGame:
    HINT_PENALTY = 5

    def __init__(self, repository=None):
        self.repository = repository or StateRepository()
        self.quizzes = []
        self.best_result = None

        self._load_state()

    def run(self):
        try:
            while True:
                self._print_menu()

                choice = read_number(
                    "선택: ",
                    1,
                    5
                )

                if choice == 1:
                    self.play_quizzes()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                else:
                    self._save_state()
                    print("퀴즈 게임을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            print()
            print("⚠️ 프로그램 종료 요청을 확인했습니다.")

            self._save_state()

            print("데이터를 저장하고 안전하게 종료합니다.")

    def play_quizzes(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        quiz_count = self._select_quiz_count()

        selected_quizzes = random.sample(
            self.quizzes,
            k=quiz_count
        )

        correct_count = 0
        hint_count = 0
        total_count = len(selected_quizzes)

        print()
        print(f"📝 퀴즈를 시작합니다! (총 {total_count}문제)")
        print("🔀 문제 순서는 무작위로 출제됩니다.")
        print(
            f"💡 힌트를 사용하려면 h를 입력하세요. "
            f"(힌트 1회당 {self.HINT_PENALTY}점 차감)"
        )

        for quiz_index, quiz in enumerate(
            selected_quizzes,
            start=1
        ):
            self._print_quiz(quiz_index, quiz)

            user_answer, hint_used = self._read_quiz_answer(
                quiz
            )

            if hint_used:
                hint_count += 1

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(
                    f"❌ 오답입니다. "
                    f"정답은 {quiz.answer}번입니다."
                )

        score = self._calculate_score(
            correct_count,
            total_count,
            hint_count
        )

        self._print_result(
            correct_count,
            total_count,
            hint_count,
            score
        )

        is_new_best = self._update_best_result(
            correct_count,
            total_count,
            hint_count,
            score
        )

        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")

        print("=" * 40)

        self._save_state()

    def add_quiz(self):
        print()
        print("📌 새로운 퀴즈를 추가합니다.")

        question = read_text("문제를 입력하세요: ")
        choices = self._read_choices()

        answer = read_number(
            "정답 번호 (1-4): ",
            1,
            Quiz.CHOICE_COUNT
        )

        hint = read_text("힌트를 입력하세요: ")

        new_quiz = Quiz(
            question,
            choices,
            answer,
            hint
        )

        self.quizzes.append(new_quiz)
        self._save_state()

        print()
        print("✅ 퀴즈가 추가되었습니다!")
        print(
            f"현재 등록된 퀴즈는 "
            f"총 {len(self.quizzes)}개입니다."
        )

    def show_quiz_list(self):
        print()

        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(
            f"📋 등록된 퀴즈 목록 "
            f"(총 {len(self.quizzes)}개)"
        )
        print("-" * 40)

        for index, quiz in enumerate(
            self.quizzes,
            start=1
        ):
            print(f"[{index}] {quiz.question}")

        print("-" * 40)

    def show_best_score(self):
        print()

        if self.best_result is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
            return

        score = self.best_result["score"]
        correct_count = self.best_result["correct_count"]
        total_count = self.best_result["total_count"]
        hint_count = self.best_result.get("hint_count", 0)

        print("=" * 40)
        print(
            f"🏆 최고 점수: {score}점 "
            f"({total_count}문제 중 "
            f"{correct_count}문제 정답)"
        )
        print(f"💡 힌트 사용: {hint_count}회")
        print("=" * 40)

    def _load_state(self):
        try:
            self.quizzes, self.best_result = (
                self.repository.load()
            )

            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개)"
            )

        except FileNotFoundError:
            print(
                "📂 저장된 파일이 없어 "
                "기본 퀴즈를 사용합니다."
            )

            self._reset_to_default_state()

        except StateDataError:
            print(
                "⚠️ 저장 파일이 손상되어 "
                "기본 데이터로 복구합니다."
            )

            self._reset_to_default_state()

        except OSError as error:
            print(f"⚠️ 저장 파일을 읽지 못했습니다: {error}")
            print("기본 데이터를 사용합니다.")

            self._reset_to_default_state()

    def _save_state(self):
        try:
            self.repository.save(
                self.quizzes,
                self.best_result
            )
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")

    def _reset_to_default_state(self):
        self.quizzes = create_default_quizzes()
        self.best_result = None

    def _select_quiz_count(self):
        total_quiz_count = len(self.quizzes)

        print()
        print(
            f"📚 현재 등록된 퀴즈는 "
            f"총 {total_quiz_count}개입니다."
        )

        return read_number(
            f"몇 문제를 풀겠습니까? "
            f"(1-{total_quiz_count}): ",
            1,
            total_quiz_count
        )

    def _read_quiz_answer(self, quiz):
        hint_used = False

        while True:
            user_input = read_answer(
                "정답 입력 (1-4, h: 힌트): ",
                1,
                Quiz.CHOICE_COUNT
            )

            if user_input != "h":
                return user_input, hint_used

            if hint_used:
                print("⚠️ 이미 이 문제의 힌트를 사용했습니다.")
                continue

            if quiz.hint is None:
                print("⚠️ 이 문제에는 등록된 힌트가 없습니다.")
                continue

            print(f"💡 힌트: {quiz.hint}")
            hint_used = True

    def _read_choices(self):
        choices = []

        for index in range(
            1,
            Quiz.CHOICE_COUNT + 1
        ):
            choice = read_text(f"선택지 {index}: ")
            choices.append(choice)

        return choices

    def _print_menu(self):
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

    def _print_quiz(self, quiz_index, quiz):
        print()
        print("-" * 40)
        print(f"[문제 {quiz_index}]")
        print()
        print(quiz.question)

        for choice_index, choice in enumerate(
            quiz.choices,
            start=1
        ):
            print(f"{choice_index}. {choice}")

    def _calculate_score(
        self,
        correct_count,
        total_count,
        hint_count
    ):
        original_score = int(
            correct_count / total_count * 100
        )

        hint_penalty = (
            hint_count * self.HINT_PENALTY
        )

        return max(
            0,
            original_score - hint_penalty
        )

    def _print_result(
        self,
        correct_count,
        total_count,
        hint_count,
        score
    ):
        print()
        print("=" * 40)
        print(
            f"🏆 결과: {total_count}문제 중 "
            f"{correct_count}문제 정답!"
        )

        if hint_count > 0:
            penalty = hint_count * self.HINT_PENALTY

            print(
                f"💡 힌트 사용: {hint_count}회 "
                f"(-{penalty}점)"
            )

        print(f"최종 점수: {score}점")

    def _update_best_result(
        self,
        correct_count,
        total_count,
        hint_count,
        score
    ):
        if (
            self.best_result is not None
            and score <= self.best_result["score"]
        ):
            return False

        self.best_result = {
            "score": score,
            "correct_count": correct_count,
            "total_count": total_count,
            "hint_count": hint_count
        }

        return True