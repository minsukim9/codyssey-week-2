import json
from pathlib import Path

from .game_record import GameRecord
from .quiz import Quiz


class StateDataError(Exception):
    pass


class StateRepository:
    def __init__(self, file_path=None):
        if file_path is None:
            project_root = Path(__file__).resolve().parent.parent
            file_path = project_root / "state.json"

        self.file_path = Path(file_path)

    def save(
        self,
        quizzes,
        best_result,
        score_history
    ):
        state = {
            "quizzes": [
                quiz.to_dict()
                for quiz in quizzes
            ],
            "best_result": best_result,
            "score_history": [
                record.to_dict()
                for record in score_history
            ]
        }

        with self.file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load(self):
        try:
            with self.file_path.open(
                "r",
                encoding="utf-8"
            ) as file:
                state = json.load(file)

            return self._parse_state(state)

        except FileNotFoundError:
            raise

        except OSError:
            raise

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError
        ) as error:
            raise StateDataError(
                "저장 데이터 형식이 올바르지 않습니다."
            ) from error

    def _parse_state(self, state):
        if not isinstance(state, dict):
            raise ValueError(
                "저장 데이터는 객체 형태여야 합니다."
            )

        quiz_data_list = state["quizzes"]
        best_result = state.get("best_result")
        score_history_data = state.get(
            "score_history",
            []
        )

        if not isinstance(quiz_data_list, list):
            raise ValueError(
                "퀴즈 목록 형식이 올바르지 않습니다."
            )

        if not isinstance(score_history_data, list):
            raise ValueError(
                "점수 기록 형식이 올바르지 않습니다."
            )

        quizzes = [
            Quiz.from_dict(quiz_data)
            for quiz_data in quiz_data_list
        ]

        score_history = [
            GameRecord.from_dict(record_data)
            for record_data in score_history_data
        ]

        self._validate_best_result(best_result)

        return (
            quizzes,
            best_result,
            score_history
        )

    def _validate_best_result(self, best_result):
        if best_result is None:
            return

        if not isinstance(best_result, dict):
            raise ValueError(
                "최고 점수 형식이 올바르지 않습니다."
            )

        try:
            score = best_result["score"]
            correct_count = best_result["correct_count"]
            total_count = best_result["total_count"]
        except KeyError as error:
            raise ValueError(
                "최고 점수 데이터에 필요한 필드가 없습니다."
            ) from error

        hint_count = best_result.get("hint_count", 0)

        values = [
            score,
            correct_count,
            total_count,
            hint_count
        ]

        if not all(type(value) is int for value in values):
            raise ValueError(
                "최고 점수 값은 숫자여야 합니다."
            )

        if score < 0 or score > 100:
            raise ValueError(
                "점수 범위가 올바르지 않습니다."
            )

        if total_count <= 0:
            raise ValueError(
                "전체 문제 수가 올바르지 않습니다."
            )

        if correct_count < 0 or correct_count > total_count:
            raise ValueError(
                "정답 개수가 올바르지 않습니다."
            )

        if hint_count < 0 or hint_count > total_count:
            raise ValueError(
                "힌트 사용 횟수가 올바르지 않습니다."
            )

        original_score = int(
            correct_count / total_count * 100
        )

        if score > original_score:
            raise ValueError(
                "저장된 점수가 올바르지 않습니다."
            )