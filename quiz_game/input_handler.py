def read_number(message, min_value, max_value):
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


def read_text(message):
    while True:
        user_input = input(message).strip()

        if not user_input:
            print("⚠️ 빈 값은 입력할 수 없습니다.")
            continue

        return user_input