import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import os
import random
import math
from decimal import Decimal, getcontext

# Устанавливаем точность вычислений до 1100 знаков
getcontext().prec = 1100


# --- ФУНКЦИЯ ДЛЯ УСТАНОВКИ ФОНА И КРАСИВОГО СЧЁТЧИКА ОНЛАЙНА ---
def set_background_and_counter(image_file):
    style = ""
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style += f"""
        background-image: url("data:image/png;base64,{b64_encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        """

    custom_css = f"""
    <style>
    .stApp {{
        {style}
    }}
    .stTabs {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }}
    /* Закрепляем контейнер с фреймом счетчика в правом углу */
    .counter-wrapper {{
        position: fixed;
        top: 65px;
        right: 20px;
        z-index: 999999;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ffcc;
        border-radius: 8px;
        padding: 3px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Полный изолированный HTML-код счетчика, который Streamlit не сможет заблокировать
    counter_html = """
    <div style="color: #00ffcc; font-family: 'Courier New', monospace; font-size: 11px; text-align: center; width: 140px; background: transparent; padding: 5px;">
        <div style="font-weight: bold; margin-bottom: 4px; font-size: 10px;">📊 СТАТИСТИКАХАБ</div>
        <hr style="margin: 3px 0; border-color: #00ffcc;">
        <!-- Живой информер, собирающий онлайн и просмотры -->
        <script language="javascript" type="text/javascript" src="//://fc2.com"></script>
        <noscript><img src="//://fc2.com" /></noscript>
    </div>
    """

    # Встраиваем счетчик через безопасный контейнер компонентов
    st.markdown('<div class="counter-wrapper">', unsafe_allow_html=True)
    components.html(counter_html, width=150, height=55, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)


# НАСТРОЙКА ИНТЕРФЕЙСА
st.set_page_config(page_title="Bynthytn buhs & Утилиты", page_icon="🎮", layout="centered")
set_background_and_counter("background.png")

st.title("🎮 Bynthytn buhs")
st.write("Добро пожаловать на платформу `Bynthytn buhs`! Здесь собраны мои веб-приложения и полезные Python-скрипты.")

# Создаем горизонтальные вкладки
tab1, tab2, tab3 = st.tabs(["🏠 Главная", "🔍 OSINT Инструмент", "🕹 Сектор проектов"])

# --- ВКЛАДКА 1: ГЛАВНАЯ СТРАНИЦА ---
with tab1:
    st.header("🕹 О проекте Bynthytn buhs")
    st.write("Привет! Это моя личная секретная платформа, где я объединяю разработку полезного софта.")
    st.subheader("🛠 На чем всё написано:")
    st.write("- **Backend**: Python (Streamlit фреймворк)")
    st.write("- **Интерфейс**: Веб-технологии и кастомный CSS-дизайн")

# --- ВКЛАДКА 2: ВСТРОЕННЫЙ ИНСТРУМЕНТ OSINT ---
with tab2:
    st.header("🔍 Инструмент OSINT и Поиска")
    st.write("Полезная утилита для проверки номеров телефонов напрямую через API.")
    phone = st.text_input("Введите номер телефона (например, 79991112233):", key="phone_input_final")

    if st.button("Запустить анализ номера", key="btn_phone_final"):
        if phone:
            with st.spinner("Пробиваем информацию по базам..."):
                clean_phone = "".join(filter(str.isdigit, phone))
                if clean_phone:
                    try:
                        base_url = "https://htmlweb.ru"
                        query_params = {"json": 1, "tel": clean_phone}
                        response = requests.get(base_url, params=query_params, timeout=10)
                        if response.status_code == 200 and response.text.strip():
                            data = response.json()
                            if "error" in data:
                                st.warning(f"Уведомление от сервера: {data['error'].get('message', 'Лимит исчерпан')}")
                            else:
                                country = data.get("country", {}).get("name", "Неизвестно")
                                region = data.get("region", {}).get("name", "Неизвестно")
                                operator = data.get("0", {}).get("oper", "Неизвестно")
                                result_text = f"=== Анализ номера: +{clean_phone} ===\n\n📍 Страна: {country}\n🗺 Регион: {region}\n📱 Оператор: {operator}\n"
                                st.text_area("Результат работы скрипта:", value=result_text, height=300)
                        else:
                            st.error("Ошибка сети или лимит запросов.")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else:
                    st.error("Неверный номер!")
        else:
            st.error("Введите номер!")

# --- ВКЛАДКА 3: СЕКТОР ПРОЕКТОВ (НАЧАЛО) ---
with tab3:
    st.header("📁 Сектор проектов")
    st.write("Нажмите на стрелочку рядом с категорией, чтобы открыть список приложений:")

    # === 1. КАТЕГОРИЯ: Математические штучки ===
    with st.expander("📁 Математические штучки"):
        st.subheader("🧮 1. Супер-калькулятор (до 1000 знаков)")

        num1_raw = st.text_area("Введите ПЕРВОЕ гигантское число (буквы сотрутся сами):", value="",
                                placeholder="Только цифры...", key="big_num1")

        st.write("Выберите математическое действие:")
        col1, col2, col3, col4 = st.columns(4)
        operation = None

        with col1:
            if st.button("➕ Сложить", use_container_width=True, key="op_plus"): operation = "+"
        with col2:
            if st.button("➖ Вычесть", use_container_width=True, key="op_minus"): operation = "-"
        with col3:
            if st.button("✖ Умножить", use_container_width=True, key="op_mult"): operation = "*"
        with col4:
            if st.button("➗ Разделить", use_container_width=True, key="op_div"): operation = "/"

        num2_raw = st.text_area("Введите ВТОРОЕ гигантское число (буквы сотрутся сами):", value="",
                                placeholder="Только цифры...", key="big_num2")

        if operation:
            num1_clean = "".join(filter(str.isdigit, num1_raw))
            num2_clean = "".join(filter(str.isdigit, num2_raw))

            if num1_clean and num2_clean:
                try:
                    d1 = Decimal(num1_clean)
                    d2 = Decimal(num2_clean)
                    if operation == "+":
                        res = d1 + d2
                    elif operation == "-":
                        res = d1 - d2
                    elif operation == "*":
                        res = d1 * d2
                    elif operation == "/":
                        if d2 == 0:
                            st.error("Ошибка: Деление на ноль невозможно!")
                            res = None
                        else:
                            res = d1 / d2

                    if res is not None:
                        st.success(f"Результат математического действия ({operation}):")
                        st.text_area("Итоговое число:", value=str(res), height=150)
                        st.info(f"Длина числа: {len(str(res))} знаков.")
                except Exception as e:
                    st.error(f"Ошибка вычислений: {e}")
            else:
                st.error("Оба поля должны содержать хотя бы одну цифру!")
        st.markdown("---")
        st.subheader("📐 2. Продвинутый калькулятор геометрии и тригонометрии (8-9 класс)")

        math_mode = st.selectbox(
            "Что нужно рассчитать?", [
                "Квадратный корень (Алгебра)",
                "Расчет Круга (Radius, Диаметр, Длина, Площадь)",
                "Периметр и Площадь Многоугольников (Геометрия)",
                "Тригонометрия (Синус, Косинус, Тангенс, Котангенс)",
                "Теорема Пифагора"
            ],
            key="math_mode_select"
        )


        # УМНАЯ ФУНКЦИЯ СОКРАЩЕНИЯ СТРОК С КНОПКОЙ «ЕЩЕ»
        def show_compact_result(label, value):
            s = f"{value:.4f}".rstrip('0').rstrip('.') if isinstance(value, float) else str(value)

            if len(s) > 150:
                st.markdown(f"**{label}** (первые 150 знаков):")
                st.code(s[:150] + "...")
                with st.expander("🔍 Показать полностью"):
                    st.code(s)
            else:
                st.success(f"{label} = {s}")


        # Подмодуль: Квадратный корень
        if math_mode == "Квадратный корень (Алгебра)":
            root_num = st.number_input("Введите число для извлечения корня:", min_value=0.0, value=25.0)
            if st.button("Найти корень"):
                show_compact_result("√" + str(root_num), math.sqrt(root_num))

        # Подмодуль: Расчет круга
        elif math_mode == "Расчет Круга (Радиус, Диаметр, Длина, Площадь)":
            circle_input_type = st.radio("Что вам известно?", ["Радиус", "Диаметр"], horizontal=True)
            val = st.number_input("Введите значение:", min_value=0.01, value=5.0)
            if st.button("Рассчитать круг"):
                r = val if circle_input_type == "Радиус" else val / 2
                d = r * 2
                length = 2 * math.pi * r
                square = math.pi * (r ** 2)

                st.markdown("### 📍 Результаты для круга:")
                show_compact_result("Радиус (R)", r)
                show_compact_result("Диаметр (D)", d)
                show_compact_result("Длина окружности (C)", length)
                show_compact_result("Площадь круга (S)", square)

        # Подмодуль: Периметр и Площадь
        elif math_mode == "Периметр и Площадь Многоугольников (Геометрия)":
            shape = st.selectbox(
                "Выберите фигуру:",
                ["Квадрат", "Прямоугольник", "Треугольник (произвольный)"]
            )
            if shape == "Квадрат":
                side = st.number_input("Сторона квадрата (a):", min_value=0.0, value=4.0)
                if st.button("Считать квадрат"):
                    show_compact_result("Периметр", side * 4)
                    show_compact_result("Площадь", side ** 2)
            elif shape == "Прямоугольник":
                a = st.number_input("Сторона a:", min_value=0.0, value=3.0)
                b = st.number_input("Сторона b:", min_value=0.0, value=5.0)
                if st.button("Считать прямоугольник"):
                    show_compact_result("Периметр", (a + b) * 2)
                    show_compact_result("Площадь", a * b)
            elif shape == "Треугольник (произвольный)":
                t1 = st.number_input("Сторона a:", min_value=0.0, value=3.0)
                t2 = st.number_input("Сторона b:", min_value=0.0, value=4.0)
                t3 = st.number_input("Сторона c:", min_value=0.0, value=5.0)
                if st.button("Считать треугольник"):
                    p = t1 + t2 + t3
                    p_half = p / 2
                    if t1 + t2 > t3 and t1 + t3 > t2 and t2 + t3 > t1:
                        s = math.sqrt(p_half * (p_half - t1) * (p_half - t2) * (p_half - t3))
                        show_compact_result("Периметр", p)
                        show_compact_result("Площадь", s)
                    else:
                        st.error("Треугольник с такими сторонами не существует!")

        # Подмодуль: Тригонометрия
        elif math_mode == "Тригонометрия (Синус, Косинус, Тангенс, Котангенс)":
            angle = st.number_input("Введите угол в градусах:", min_value=0.0, max_value=360.0, value=45.0)
            if st.button("Найти тригонометрические функции"):
                rad = math.radians(angle)
                sin_v = math.sin(rad)
                cos_v = math.cos(rad)
                tan_v = math.tan(rad) if angle != 90 and angle != 270 else "Не существует"
                cot_v = 1 / math.tan(rad) if angle != 0 and angle != 180 and angle != 360 else "Не существует"
                st.success(f"📐 Результаты для угла {angle}°:")
                st.write(f"- **Синус (sin)** = {sin_v:.4f}")
                st.write(f"- **Косинус (cos)** = {cos_v:.4f}")
                st.write(f"- **Тангенс (tg)** = {tan_v if isinstance(tan_v, str) else f'{tan_v:.4f}'}")
                st.write(f"- **Котангенс (ctg)** = {cot_v if isinstance(cot_v, str) else f'{cot_v:.4f}'}")

        # Подмодуль: Теорема Пифагора
        elif math_mode == "Теорема Пифагора":
            pif_type = st.radio("Что ищем?", ["Гипотенузу (c)", "Катет (a или b)"], horizontal=True)
            if pif_type == "Гипотенузу (c)":
                katet1 = st.number_input("Введите первый катет:", min_value=0.01, value=3.0)
                katet2 = st.number_input("Введите второй катет:", min_value=0.01, value=4.0)
                if st.button("Найти гипотенузу"):
                    gip = math.sqrt(katet1 ** 2 + katet2 ** 2)
                    show_compact_result("Гипотенуза c", gip)
            else:
                katet = st.number_input("Введите известный катет:", min_value=0.01, value=3.0)
                gip = st.number_input("Введите известную гипотенузу:", min_value=0.01, value=5.0)
                if st.button("Найти неизвестный катет"):
                    if gip > katet:
                        res_katet = math.sqrt(gip ** 2 - katet ** 2)
                        show_compact_result("Неизвестный катет", res_katet)
                    else:
                        st.error("Гипотенуза должна быть больше катета!")

    # === 2. КАТЕГОРИЯ: Мини игры ненадолго ===
    with st.expander("📁 Мини игры ненадолго"):
        st.write("🕹 Быстрые игры, чтобы скоротать пару минут.")
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
        st.write("🛠 Автоматизации, парсеры данных, генераторы паролей и защитные утилиты.")
        st.info("Папка пуста. Ждем новые идеи!")
