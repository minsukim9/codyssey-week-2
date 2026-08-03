from .quiz import Quiz


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