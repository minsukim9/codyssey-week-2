class Quiz:
    CHOICE_COUNT = 4

    def __init__(
        self,
        question,
        choices,
        answer,
        hint=None
    ):
        self._validate(
            question,
            choices,
            answer,
            hint
        )

        self.question = question.strip()
        self.choices = [
            choice.strip()
            for choice in choices
        ]
        self.answer = answer
        self.hint = hint.strip() if hint is not None else None

    def is_correct(self, user_answer):
        return self.answer == user_answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, quiz_data):
        if not isinstance(quiz_data, dict):
            raise ValueError(
                "퀴즈 데이터 형식이 올바르지 않습니다."
            )

        try:
            question = quiz_data["question"]
            choices = quiz_data["choices"]
            answer = quiz_data["answer"]
        except KeyError as error:
            raise ValueError(
                "퀴즈 데이터에 필요한 필드가 없습니다."
            ) from error

        hint = quiz_data.get("hint")

        return cls(
            question,
            choices,
            answer,
            hint
        )

    @classmethod
    def _validate(
        cls,
        question,
        choices,
        answer,
        hint
    ):
        if not isinstance(question, str) or not question.strip():
            raise ValueError(
                "퀴즈 문제가 올바르지 않습니다."
            )

        if not isinstance(choices, list):
            raise ValueError(
                "선택지는 리스트여야 합니다."
            )

        if len(choices) != cls.CHOICE_COUNT:
            raise ValueError(
                f"선택지는 {cls.CHOICE_COUNT}개여야 합니다."
            )

        if not all(
            isinstance(choice, str) and choice.strip()
            for choice in choices
        ):
            raise ValueError(
                "선택지 내용이 올바르지 않습니다."
            )

        if type(answer) is not int:
            raise ValueError(
                "정답은 숫자여야 합니다."
            )

        if answer < 1 or answer > cls.CHOICE_COUNT:
            raise ValueError(
                f"정답은 1부터 "
                f"{cls.CHOICE_COUNT} 사이여야 합니다."
            )

        if hint is not None:
            if not isinstance(hint, str) or not hint.strip():
                raise ValueError(
                    "힌트 내용이 올바르지 않습니다."
                )