from datetime import datetime


class GameRecord:
    def __init__(
        self,
        played_at,
        score,
        correct_count,
        total_count,
        hint_count
    ):
        self._validate(
            played_at,
            score,
            correct_count,
            total_count,
            hint_count
        )

        self.played_at = played_at
        self.score = score
        self.correct_count = correct_count
        self.total_count = total_count
        self.hint_count = hint_count

    def to_dict(self):
        return {
            "played_at": self.played_at,
            "score": self.score,
            "correct_count": self.correct_count,
            "total_count": self.total_count,
            "hint_count": self.hint_count
        }

    @classmethod
    def from_dict(cls, record_data):
        if not isinstance(record_data, dict):
            raise ValueError(
                "게임 기록 형식이 올바르지 않습니다."
            )

        try:
            played_at = record_data["played_at"]
            score = record_data["score"]
            correct_count = record_data["correct_count"]
            total_count = record_data["total_count"]
        except KeyError as error:
            raise ValueError(
                "게임 기록에 필요한 필드가 없습니다."
            ) from error

        hint_count = record_data.get("hint_count", 0)

        return cls(
            played_at,
            score,
            correct_count,
            total_count,
            hint_count
        )

    @staticmethod
    def _validate(
        played_at,
        score,
        correct_count,
        total_count,
        hint_count
    ):
        if not isinstance(played_at, str):
            raise ValueError(
                "게임 기록 시간이 올바르지 않습니다."
            )

        try:
            datetime.fromisoformat(played_at)
        except ValueError as error:
            raise ValueError(
                "게임 기록 시간 형식이 올바르지 않습니다."
            ) from error

        values = [
            score,
            correct_count,
            total_count,
            hint_count
        ]

        if not all(type(value) is int for value in values):
            raise ValueError(
                "게임 기록 값은 숫자여야 합니다."
            )

        if score < 0 or score > 100:
            raise ValueError(
                "게임 점수 범위가 올바르지 않습니다."
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
                "게임 기록 점수가 올바르지 않습니다."
            )