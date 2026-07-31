import streamlit as st
import requests
import base64
import os
import random
from decimal import getcontext

# --- КОНФИГУРАЦИЯ И СТИЛИ ---
getcontext().prec = 1100  # Точность вычислений
st.set_page_config(page_title="Bynthytn buhs & Утилиты", page_icon="🎮", layout="centered")


def set_background(image_file):
    """Установка фонового изображения и стилей"""
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stTabs {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 25px;
            border-radius: 15px;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)


set_background("background.png")

st.title("🎮 Bynthytn buhs")
st.write("Добро пожаловать! Инструменты, проекты и утилиты.")

# Вкладки приложения
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Главная", "🔍 OSINT", "🕹 Генератор", "💬 Контакт"])

# --- ВКЛАДКА 1: ГЛАВНАЯ ---
with tab1:
    st.header("О проекте")
    st.write("Личная платформа: разработка и полезные скрипты.")

    # Счетчик
    if 'page_views' not in st.session_state:
        st.session_state.page_views = random.randint(10, 50)
    st.metric(label="Просмотры", value=st.session_state.page_views)

# --- ВКЛАДКА 2: OSINT ---
with tab2:
    st.header("🔍 OSINT Инструмент")
    phone = st.text_input("Введите номер (например, 79991112233):")

    if st.button("Анализ", key="osint_btn"):
        if phone:
            with st.spinner("Анализ..."):
                try:
                    # Упрощенный запрос к API
                    data = requests.get(f"https://htmlweb.ru{phone}", timeout=5).json()
                    if "error" in data:
                        st.warning("Ошибка или лимит.")
                    else:
                        st.success(f"Регион: {data.get('region', {}).get('name', 'N/A')}")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
# --- ВКЛАДКА 4: ПУБЛИЧНЫЕ ПОЖЕЛАНИЯ И ОТЗЫВЫ ---
with tab4:
    st.header("💬 Книга пожеланий сайта Bynthytn buhs")
    user_name = st.text_input("Ваше имя или никнейм:", value="Аноним", max_chars=30)
    user_text = st.text_area("Ваше пожелание или отзыв:", max_chars=300)

    if st.button("🚀 Отправить пожелание", key="send_feedback_btn"):
        if user_text.strip():
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"👤 {user_name.strip()}: {user_text.strip()}\n")
            st.success("🎉 Спасибо! Ваш отзыв опубликован.")
            st.balloons()
        else:
            st.error("Введите текст!")

    st.markdown("### 📜 Что пишут пользователи:")
    if os.path.exists("feedback.txt"):
        with open("feedback.txt", "r", encoding="utf-8") as f:
            for comment in reversed(f.readlines()):
                if comment.strip(): st.info(comment.strip())
    else:
        st.write("🕊 Пока здесь пусто.")

# --- ВКЛАДКА 3: СЕКТОР ПРОЕКТОВ ---
with tab3:
    st.header("📁 Сектор проектов")

    with st.expander("📁 Математические штучки", expanded=True):
        st.subheader("🧮 1. Супер-калькулятор")
        num1_raw = st.text_area("Первое число:", key="big_num1")
        col1, col2, col3, col4 = st.columns(4)
        operation = None
        if col1.button("➕", use_container_width=True): operation = "+"
        if col2.button("➖", use_container_width=True): operation = "-"
        if col3.button("✖", use_container_width=True): operation = "*"
        if col4.button("➗", use_container_width=True): operation = "/"
        num2_raw = st.text_area("Второе число:", key="big_num2")

        if operation:
            n1 = "".join(filter(str.isdigit, num1_raw))
            n2 = "".join(filter(str.isdigit, num2_raw))
            if n1 and n2:
                try:
                    from decimal import Decimal

                    d1, d2 = Decimal(n1), Decimal(n2)
                    res = {'+': d1 + d2, '-': d1 - d2, '*': d1 * d2, '/': d1 / d2 if d2 != 0 else "Error"}[operation]
                    st.success(f"Результат ({operation}):")
                    st.code(str(res))
                except Exception as e:
                    st.error(f"Ошибка: {e}")
            else:
                st.error("Введите числа!")

        st.markdown("---")
        st.subheader("📐 2. Геометрия (8-9 класс)")
        math_mode = st.selectbox("Расчет:", ["Корень", "Круг", "Фигуры", "Тригонометрия", "Пифагор"])
        import math

        if math_mode == "Корень":
            n = st.number_input("Число:", value=25.0)
            if st.button("√x"): st.success(math.sqrt(n))
        elif math_mode == "Круг":
            r = st.number_input("Радиус:", value=5.0)
            if st.button("Расчет"):
                st.write(f"Окружность: {2 * math.pi * r:.2f}, Площадь: {math.pi * r ** 2:.2f}")
        elif math_mode == "Фигуры":
            sh = st.selectbox("Фигура", ["Квадрат", "Прямоугольник"])
            a = st.number_input("Сторона a", value=4.0)
            b = st.number_input("Сторона b", value=4.0)
            if st.button("Считать"):
                st.success(f"Периметр: {(a + b) * 2}, Площадь: {a * b}")
        elif math_mode == "Тригонометрия":
            angle = st.number_input("Угол (°)", value=45.0)
            if st.button("sin/cos"):
                rad = math.radians(angle)
                st.success(f"sin: {math.sin(rad):.4f}, cos: {math.cos(rad):.4f}")
        elif math_mode == "Пифагор":
            a = st.number_input("Катет a", value=3.0)
            b = st.number_input("Катет b", value=4.0)
            if st.button("Гипотенуза"): st.success(math.sqrt(a ** 2 + b ** 2))
    # === 2. КАТЕГОРИЯ: Mini игры ненадолго ===
    with st.expander("📁 Mini игры ненадолго"):
        st.markdown("### 🔢 Игра: Угадай число")
        if 'secret_number' not in st.session_state:
            st.session_state.secret_number = random.randint(1, 20)

        user_guess = st.number_input("Введите число от 1 до 20:", min_value=1, max_value=20, step=1, key="game_guess")
        if st.button("Проверить число", key="btn_game"):
            if user_guess < st.session_state.secret_number:
                st.warning("📉 Загаданное число больше!")
            elif user_guess > st.session_state.secret_number:
                st.warning("📈 Загаданное число меньше!")
            else:
                st.success("🎉 Ура! Вы угадали число!")
                st.session_state.secret_number = random.randint(1, 20)
                st.balloons()

    # === 3. КАТЕГОРИЯ: Полезные скрипты ===
    with st.expander("📁 Полезные скрипты"):
        st.subheader("🔑 1. Генератор неуязвимых хакерских паролей")

        pass_len = st.slider("Выберите длину пароля:", min_value=6, max_value=32, value=12)

        # Новый блок настроек символов для пароля
        st.write("Настройка состава пароля:")
        use_lowercase = st.checkbox("Только строчные буквы (abc...)", value=False)
        use_uppercase = st.checkbox("Добавить заглавные буквы (ABC...)", value=True)
        use_digits = st.checkbox("Добавить цифры (123...)", value=True)
        use_specials = st.checkbox("Добавить спецсимволы (!@#...)", value=False)

        if st.button("Сгенерировать пароль", key="gen_pass_btn"):
            # Создаем базу символов на основе выбора пользователя
            chars = ""
            if use_lowercase or (not use_uppercase and not use_digits and not use_specials):
                chars += "abcdefghijklmnopqrstuvwxyz"
            if use_uppercase:
                chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if not use_lowercase and not chars:  # Защита от пустой строки
                    chars += "abcdefghijklmnopqrstuvwxyz"
            if use_digits:
                chars += "1234567890"
            if use_specials:
                chars += "!@#$%^&*"

            # Генерация пароля
            new_password = "".join(random.choice(chars) for _ in range(pass_len))
            st.success("🔒 Ваш безопасный пароль:")
            st.code(new_password)

            # Оценка надежности
            if pass_len < 8:
                st.warning("⚠ Этот пароль взломают за 5 секунд! Сделайте длиннее.")
            elif pass_len < 12:
                st.info("👍 Хороший пароль. На взлом уйдёт около 2 лет.")
            else:
                st.success("😎 Сверхнадёжный суперпароль!")

        st.markdown("---")
        st.subheader("🌦 2. Живой информер погоды")
        city = st.text_input("Введите название города на английском (например, Yaroslavl, Moscow, London):",
                             value="Yaroslavl")

        if st.button("Узнать погоду", key="weather_btn"):
            with st.spinner("Запрашиваем данные у метеослужбы..."):
                try:
                    weather_url = f"https://wttr.in{city}?format=3"
                    weather_res = requests.get(weather_url, timeout=5)
                    if weather_res.status_code == 200:
                        st.info(f"🌍 Погода сейчас: {weather_res.text.strip()}")
                    else:
                        st.error("Не удалось найти такой город. Проверьте правильность написания.")
                except Exception as e:
                    st.error("Метеосервер временно перегружен, попробуйте чуть позже.")
