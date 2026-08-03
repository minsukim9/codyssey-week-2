from .quiz import Quiz


def create_default_quizzes():
    return [
        Quiz(
            "Python에서 여러 값을 순서대로 저장하는 자료형은 무엇인가요?",
            ["int", "list", "bool", "str"],
            2,
            "대괄호 []를 사용하는 자료형입니다."
        ),
        Quiz(
            "Python에서 조건문을 작성할 때 사용하는 키워드는 무엇인가요?",
            ["if", "for", "def", "class"],
            1,
            "영어로 '만약'이라는 뜻의 키워드입니다."
        ),
        Quiz(
            "Python에서 함수를 정의할 때 사용하는 키워드는 무엇인가요?",
            ["func", "method", "def", "return"],
            3,
            "define의 앞 세 글자를 생각해 보세요."
        ),
        Quiz(
            "Python에서 반복 횟수가 정해져 있을 때 주로 사용하는 반복문은 무엇인가요?",
            ["if", "try", "while", "for"],
            4,
            "정해진 범위를 순회할 때 자주 사용합니다."
        ),
        Quiz(
            "Python 클래스의 생성자 역할을 하는 메서드는 무엇인가요?",
            ["__main__", "__init__", "__start__", "__class__"],
            2,
            "객체 생성 시 처음 호출되는 특수 메서드입니다."
        )
    ]