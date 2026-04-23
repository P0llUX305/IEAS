import streamlit as st
import pandas as pd
import random
from google import genai

# --- Page Configuration ---
st.set_page_config(page_title="БББЖ (IEAS) Прототипі", layout="wide", initial_sidebar_state="expanded")

# --- Fake Data Generation ---
# We simulate a student's performance dropping over 10 weeks
weeks = [f"{i}-апта" for i in range(1, 11)]
pass_probability = [95, 92, 88, 85, 80, 75, 60, 50, 42, 35]  # Notice the sharp drop
data = pd.DataFrame({
    "Апта": weeks,
    "Өту ықтималдығы (%)": pass_probability
})

# --- Sidebar: Student Profile (The "Platonus" Replacement) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)  # Generic profile icon
    st.header("Студент профилі")
    st.write("**Аты-жөні:** Әліхан Нұрмаханов")
    st.write("**ID:** 2026-CS-042")
    st.write("**Мамандық:** Компьютерлік ғылымдар (Computer Science)")
    st.write("**Ағымдағы курс:** Жетілдірілген алгоритмдер")

# --- Tabs for App Navigation ---
tab1, tab2, tab3 = st.tabs(["📊 Басқару тақтасы", "🧠 Адаптивті тест", "📝 ЖИ (AI) эссе бағалаушы"])

with tab1:
    # --- Main Dashboard ---
    st.title("🎓 Білім берудегі бағалаудың білікті жүйесі (БББЖ/IEAS)")
    st.markdown("*Жаңа буын болжамдық талдау басқару тақтасы (Прототип)*")

    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Ағымдағы курс бағасы", value="68%", delta="-12%", delta_color="inverse")
    col2.metric(label="Белсенділік көрсеткіші", value="Төмен", delta="Назар аудару қажет", delta_color="inverse")
    col3.metric(label="Болжамды қорытынды нәтиже", value="Сәтсіздік қаупі", delta="Жоғары дабыл", delta_color="inverse")

    st.divider()

    # Predictive Chart
    st.subheader("📈 Болжамдық траектория: Өту ықтималдығы")
    st.markdown(
        "Тек өткен бағаларды көрсететін дәстүрлі жүйелерден айырмашылығы, БББЖ (IEAS) терең білімді бақылау (Deep Knowledge Tracing) арқылы болашақ нәтижелерді болжайды.")
    st.line_chart(data.set_index("Апта"))

    # Autonomous Intervention Alert
    st.subheader("⚠️ ЖИ (AI) автономды араласуы")
    # Using a warning box to simulate an alert popping up for the professor
    st.warning(
        "**ШҰҒЫЛ ЕСКЕРТУ:** Әліханның өту ықтималдығы 40% шегінен төмен түсті. Когнитивті қозғалтқыш 'Динамикалық бағдарламалау' (Dynamic Programming) тақырыбындағы түбегейлі түсінбеушілікті анықтады.")

    # Explainability Section (Crucial for the AI Ethics/2026 Law point!)
    with st.expander("🔍 ЖИ (AI) шешім логикасын көру (Түсіндірмелілік деңгейі)"):
        st.markdown("""
        **ЖИ (AI) неге бұл студентті белгіледі?**
        * **1:** Динамикалық бағдарламалау бойынша соңғы екі тесттен өте алмады.
        * **2:** БҚЖ (LMS) материалдарын оқу уақыты соңғы 3 аптада 65%-ға төмендеді.
        * **Педагогикалық әрекет:** Жүйе Әліханға 'Мемоизация' тақырыбы бойынша жекелендірілген негізгі модульді автоматты түрде жіберіп, оқытушы ассистентке хабарлады.
        """)

        if st.button("ЖИ (AI) араласу жоспарын мақұлдау"):
            st.success("Араласу жоспары мақұлданды!")
            st.balloons()

with tab2:
    st.header("🧠 Үздіксіз ТЖТ (IRT) бағалау жүйесі (Математика демо)")
    st.markdown(
        "Бұл модуль нағыз тапсырмаға жауап беру теориясын (IRT) қолданады. Ол студенттің қабілетін 1-100 шкаласы бойынша үздіксіз бағалайды, олардың дәл когнитивті шегіне сәйкес сұрақтарды алгоритмдік түрде таңдайды.")

    # --- Initialize Continuous AI Memory ---
    if 'quiz_step' not in st.session_state:
        st.session_state.quiz_step = 1
        st.session_state.ability_score = 50.0  # Start exactly in the middle
        st.session_state.asked_questions = []
        st.session_state.quiz_complete = False
        st.session_state.current_q_data = None

    # --- The 80-Question Continuous Math Bank ---
    # Difficulty ranges from 10 (Very Easy) to 99 (Very Hard)
    question_bank = [
        # --- Күрделілік 10 (Өте жеңіл арифметика) ---
        {'q': "15 + 27 нешеге тең?", 'opts': ["32", "42", "52", "45"], 'ans': "42", 'diff': 10},
        {'q': "9 + 13 нешеге тең?", 'opts': ["20", "22", "21", "23"], 'ans': "22", 'diff': 10},
        {'q': "50 - 18 нешеге тең?", 'opts': ["32", "28", "38", "42"], 'ans': "32", 'diff': 10},
        # --- Күрделілік 15 ---
        {'q': "8-ді 7-ге көбейтсе нешеге тең?", 'opts': ["54", "56", "64", "48"], 'ans': "56", 'diff': 15},
        {'q': "6-ны 9-ға көбейтсе нешеге тең?", 'opts': ["45", "52", "54", "63"], 'ans': "54", 'diff': 15},
        {'q': "12-ні 5-ке көбейтсе нешеге тең?", 'opts': ["50", "55", "60", "65"], 'ans': "60", 'diff': 15},
        # --- Күрделілік 20 ---
        {'q': "144-ті 12-ге бөлсе нешеге тең?", 'opts': ["10", "11", "12", "14"], 'ans': "12", 'diff': 20},
        {'q': "81-ді 9-ға бөлсе нешеге тең?", 'opts': ["7", "8", "9", "10"], 'ans': "9", 'diff': 20},
        {'q': "256-ны 16-ға бөлсе нешеге тең?", 'opts': ["14", "15", "16", "18"], 'ans': "16", 'diff': 20},
        # --- Күрделілік 25 ---
        {'q': "150-нің 20%-ы нешеге тең?", 'opts': ["20", "25", "30", "35"], 'ans': "30", 'diff': 25},
        {'q': "200-дің 25%-ы нешеге тең?", 'opts': ["40", "45", "50", "55"], 'ans': "50", 'diff': 25},
        {'q': "450-нің 10%-ы нешеге тең?", 'opts': ["40", "45", "50", "55"], 'ans': "45", 'diff': 25},
        # --- Күрделілік 30 ---
        {'q': "x-ті табыңыз: 2x + 5 = 15", 'opts': ["x = 5", "x = 10", "x = 4", "x = 6"], 'ans': "x = 5", 'diff': 30},
        {'q': "x-ті табыңыз: 4x - 3 = 13", 'opts': ["x = 3", "x = 4", "x = 5", "x = 6"], 'ans': "x = 4", 'diff': 30},
        {'q': "x-ті табыңыз: x + 12 = 25", 'opts': ["x = 11", "x = 12", "x = 13", "x = 14"], 'ans': "x = 13", 'diff': 30},
        # --- Күрделілік 35 ---
        {'q': "Табаны 10, биіктігі 4 болатын үшбұрыштың ауданы қанша?", 'opts': ["40", "20", "14", "24"],
         'ans': "20", 'diff': 35},
        {'q': "Ұзындығы 8, ені 5 болатын тіктөртбұрыштың периметрі қанша?", 'opts': ["26", "30", "40", "13"],
         'ans': "26", 'diff': 35},
        {'q': "Ұзындығы 7, ені 3 болатын тіктөртбұрыштың ауданы қанша?", 'opts': ["10", "20", "21", "24"],
         'ans': "21", 'diff': 35},
        # --- Күрделілік 40 ---
        {'q': "196-ның квадрат түбірі нешеге тең?", 'opts': ["12", "14", "16", "18"], 'ans': "14", 'diff': 40},
        {'q': "225-тің квадрат түбірі нешеге тең?", 'opts': ["13", "14", "15", "16"], 'ans': "15", 'diff': 40},
        {'q': "7-нің квадраты нешеге тең?", 'opts': ["42", "47", "49", "56"], 'ans': "49", 'diff': 40},
        # --- Күрделілік 45 ---
        {'q': "x-ті табыңыз: 3(x - 2) = 12", 'opts': ["x = 4", "x = 6", "x = 8", "x = 2"], 'ans': "x = 6", 'diff': 45},
        {'q': "x-ті табыңыз: 5x + 3 = 2x + 18", 'opts': ["x = 3", "x = 5", "x = 7", "x = 15"], 'ans': "x = 5", 'diff': 45},
        {'q': "24 пен 36-ның ең үлкен ортақ бөлгіші нешеге тең?", 'opts': ["6", "8", "12", "18"], 'ans': "12", 'diff': 45},
        # --- Күрделілік 50 ---
        {'q': "Екі стандартты сүйекпен лақтырғанда қосындысы 7 болу ықтималдығы қанша?",
         'opts': ["1/6", "1/7", "1/12", "1/36"], 'ans': "1/6", 'diff': 50},
        {'q': "{3, 7, 7, 2, 6} жиынының орта мәні (арифметикалық орта) нешеге тең?", 'opts': ["4", "5", "6", "7"], 'ans': "5", 'diff': 50},
        {'q': "{12, 3, 7, 9, 5} жиынының медианасы нешеге тең?", 'opts': ["5", "7", "9", "12"], 'ans': "7", 'diff': 50},
        # --- Күрделілік 55 ---
        {'q': "pi санының екі ондық белгіге дейінгі мәні қанша?", 'opts': ["3.12", "3.14", "3.16", "3.18"], 'ans': "3.14",
         'diff': 55},
        {'q': "Жазық бұрышта неше градус бар?", 'opts': ["90", "120", "180", "360"], 'ans': "180", 'diff': 55},
        {'q': "Радиусы 7 болатын шеңбердің ұзындығы қанша? (pi = 22/7 деп алыңыз)",
         'opts': ["22", "44", "88", "154"], 'ans': "44", 'diff': 55},
        # --- Күрделілік 60 ---
        {'q': "x^2 функциясының x бойынша бірінші туындысы неге тең?", 'opts': ["x", "2x", "x^2", "2"], 'ans': "2x",
         'diff': 60},
        {'q': "5x^3 функциясының бірінші туындысы неге тең?", 'opts': ["5x^2", "15x^2", "15x^3", "3x^2"], 'ans': "15x^2",
         'diff': 60},
        {'q': "f(x) = 3x + 7 болса, f(4) нешеге тең?", 'opts': ["12", "15", "19", "21"], 'ans': "19", 'diff': 60},
        # --- Күрделілік 65 ---
        {'q': "Квадрат теңдеуді шешіңіз: x^2 - 5x + 6 = 0", 'opts': ["x=1, 6", "x=2, 3", "x=-2, -3", "x=0, 6"],
         'ans': "x=2, 3", 'diff': 65},
        {'q': "Квадрат теңдеуді шешіңіз: x^2 - 9 = 0", 'opts': ["x=3, -3", "x=9, -9", "x=0, 9", "x=1, -9"],
         'ans': "x=3, -3", 'diff': 65},
        {'q': "x^2 + 4x + 4 = 0 теңдеуінің дискриминанты нешеге тең?", 'opts': ["-4", "0", "4", "16"], 'ans': "0", 'diff': 65},
        # --- Күрделілік 70 ---
        {'q': "2x dx анықталмаған интегралы неге тең?", 'opts': ["x^2 + C", "2x^2 + C", "x + C", "2 + C"],
         'ans': "x^2 + C", 'diff': 70},
        {'q': "6x^2 dx анықталмаған интегралы неге тең?", 'opts': ["2x^3 + C", "3x^3 + C", "6x^3 + C", "x^3 + C"],
         'ans': "2x^3 + C", 'diff': 70},
        {'q': "y = 4x - 9 түзуінің еңісі (бұрыштық коэффициенті) нешеге тең?", 'opts': ["4", "-9", "9", "-4"], 'ans': "4", 'diff': 70},
        # --- Күрделілік 75 ---
        {'q': "2 негізді логарифмі 32-ден нешеге тең?", 'opts': ["4", "5", "6", "16"], 'ans': "5", 'diff': 75},
        {'q': "10 негізді логарифмі 1000-нан нешеге тең?", 'opts': ["2", "3", "4", "10"], 'ans': "3", 'diff': 75},
        {'q': "Ықшамдаңыз: ln(e^5)", 'opts': ["1", "e", "5", "e^5"], 'ans': "5", 'diff': 75},
        # --- Күрделілік 80 ---
        {'q': "x 0-ге ұмтылғанда sin(x)/x шегі неге тең?", 'opts': ["0", "1", "Шексіздік", "Анықталмаған"],
         'ans': "1", 'diff': 80},
        {'q': "n шексіздікке ұмтылғанда (1 + 1/n)^n шегі неге тең?",
         'opts': ["0", "1", "e", "Шексіздік"], 'ans': "e", 'diff': 80},
        {'q': "sin(x) функциясының туындысы неге тең?", 'opts': ["-cos(x)", "cos(x)", "sin(x)", "-sin(x)"],
         'ans': "cos(x)", 'diff': 80},
        # --- Күрделілік 85 ---
        {'q': "[[2, 1], [1, 2]] матрицасының детерминанты нешеге тең?", 'opts': ["2", "3", "4", "5"], 'ans': "3",
         'diff': 85},
        {'q': "[1, 2, 3] және [4, 5, 6] векторларының скаляр көбейтіндісі нешеге тең?",
         'opts': ["20", "32", "38", "40"], 'ans': "32", 'diff': 85},
        {'q': "[[1, 2], [3, 4]] матрицасының транспонирленгені қандай?",
         'opts': ["[[1, 3], [2, 4]]", "[[4, 3], [2, 1]]", "[[2, 1], [4, 3]]", "[[1, 2], [3, 4]]"],
         'ans': "[[1, 3], [2, 4]]", 'diff': 85},
        # --- Күрделілік 90 ---
        {'q': "e^(2x) функциясының туындысы неге тең?", 'opts': ["e^(2x)", "2e^(x)", "2e^(2x)", "e^(x)"], 'ans': "2e^(2x)",
         'diff': 90},
        {'q': "1/x dx интегралы неге тең?", 'opts': ["x + C", "ln(x) + C", "1/x^2 + C", "e^x + C"],
         'ans': "ln(x) + C", 'diff': 90},
        {'q': "ln(x) функциясының туындысы неге тең?", 'opts': ["x", "1/x", "ln(x)", "e^x"], 'ans': "1/x", 'diff': 90},
        # --- Күрделілік 95 ---
        {'q': "e^x dx анықталмаған интегралы неге тең?", 'opts': ["e^x + C", "xe^x + C", "e^(x+1) + C", "ln(x) + C"],
         'ans': "e^x + C", 'diff': 95},
        {'q': "x^4 функциясының екінші туындысы неге тең?", 'opts': ["4x^3", "12x^2", "24x", "x^2"],
         'ans': "12x^2", 'diff': 95},
        {'q': "cos(x) dx интегралын 0-ден pi/2-ге дейін есептеңіз.",
         'opts': ["0", "1", "pi/2", "-1"], 'ans': "1", 'diff': 95},
        # --- Күрделілік 98 ---
        {'q': "1 + 1/2 + 1/4 + 1/8 + ... шексіз геометриялық қатарының қосындысы нешеге тең?",
         'opts': ["1.5", "2", "Шексіздік", "2.5"], 'ans': "2", 'diff': 98},
        {'q': "e^x функциясының x=0 нүктесіндегі Тейлор қатары x^2 мүшесіне дейін қандай?",
         'opts': ["1 + x + x^2", "1 + x + x^2/2", "x + x^2/2", "1 + 2x + x^2"],
         'ans': "1 + x + x^2/2", 'diff': 98},
        {'q': "sin(x) функциясының Маклорен қатарындағы x^3 мүшесінің коэффициенті нешеге тең?",
         'opts': ["1/6", "-1/6", "1/3", "-1/3"], 'ans': "-1/6", 'diff': 98},
        # --- Күрделілік 99 (Өте қиын) ---
        {'q': "Эйлер төстігі бойынша, e^(i*pi) + 1 неге тең?", 'opts': ["-1", "0", "1", "pi"], 'ans': "0",
         'diff': 99},
        {'q': "f(z) = 1/(z^2 + 1) функциясының z = i нүктесіндегі қалдығы (резидуумы) неге тең?",
         'opts': ["1/(2i)", "-1/(2i)", "i/2", "-i/2"], 'ans': "1/(2i)", 'diff': 99},
        {'q': "f(t) = t функциясының Лаплас түрлендіруі неге тең?",
         'opts': ["1/s", "1/s^2", "s", "s^2"], 'ans': "1/s^2", 'diff': 99},
        # --- Көптүрлілік үшін қосымша сұрақтар ---
        {'q': "100 - 37 нешеге тең?", 'opts': ["57", "63", "67", "73"], 'ans': "63", 'diff': 10},
        {'q': "11-ді 11-ге көбейтсе нешеге тең?", 'opts': ["111", "121", "131", "141"], 'ans': "121", 'diff': 15},
        {'q': "200-ді 25-ке бөлсе нешеге тең?", 'opts': ["6", "7", "8", "9"], 'ans': "8", 'diff': 20},
        {'q': "84-тің 50%-ы нешеге тең?", 'opts': ["38", "42", "44", "48"], 'ans': "42", 'diff': 25},
        {'q': "x-ті табыңыз: 7x = 49", 'opts': ["x = 6", "x = 7", "x = 8", "x = 9"], 'ans': "x = 7", 'diff': 30},
        {'q': "Радиусы 3 болатын дөңгелектің ауданы қанша? (pi = 3.14 деп алыңыз)",
         'opts': ["18.84", "28.26", "9.42", "31.4"], 'ans': "28.26", 'diff': 35},
        {'q': "27-нің куб түбірі нешеге тең?", 'opts': ["2", "3", "4", "9"], 'ans': "3", 'diff': 40},
        {'q': "4 пен 6-ның ең кіші ортақ еселігі нешеге тең?", 'opts': ["8", "10", "12", "24"], 'ans': "12", 'diff': 45},
        {'q': "Тиын екі рет лақтырылды. Екі рет те 'heads' түсу ықтималдығы қанша?",
         'opts': ["1/2", "1/3", "1/4", "1/8"], 'ans': "1/4", 'diff': 50},
        {'q': "Алтыбұрыштың ішкі бұрыштарының қосындысы неше градус?",
         'opts': ["540", "600", "720", "900"], 'ans': "720", 'diff': 55},
        {'q': "4x^3 + 2x функциясының туындысы неге тең?", 'opts': ["12x^2 + 2", "12x + 2", "4x^2 + 2", "8x^2 + 2"],
         'ans': "12x^2 + 2", 'diff': 60},
        {'q': "x^2 - 4x + 3 = 0 теңдеуінің түбірлері қандай?", 'opts': ["x=1, 3", "x=2, 2", "x=-1, -3", "x=0, 4"],
         'ans': "x=1, 3", 'diff': 65},
        {'q': "cos(x) dx анықталмаған интегралы неге тең?",
         'opts': ["sin(x) + C", "-sin(x) + C", "cos(x) + C", "-cos(x) + C"], 'ans': "sin(x) + C", 'diff': 70},
        {'q': "3 негізді логарифмі 81-ден нешеге тең?", 'opts': ["2", "3", "4", "5"], 'ans': "4", 'diff': 75},
        {'q': "cos(x) функциясының туындысы неге тең?", 'opts': ["sin(x)", "-sin(x)", "cos(x)", "-cos(x)"],
         'ans': "-sin(x)", 'diff': 80},
        {'q': "I бірлік матрицасының (2x2) меншікті мәні нешеге тең?",
         'opts': ["0", "1", "2", "Анықталмаған"], 'ans': "1", 'diff': 85},
        {'q': "Көбейтінді ережесін қолданып, x * e^x функциясының туындысы неге тең?",
         'opts': ["e^x", "xe^x", "e^x + xe^x", "e^x - xe^x"], 'ans': "e^x + xe^x", 'diff': 90},
        {'q': "sin(x) dx интегралын 0-ден pi-ге дейін есептеңіз.",
         'opts': ["0", "1", "2", "-2"], 'ans': "2", 'diff': 95},
        {'q': "x^n / n! қатарының жинақталу радиусы нешеге тең?",
         'opts': ["0", "1", "e", "Шексіздік"], 'ans': "Шексіздік", 'diff': 98},
        {'q': "Дирак дельта функциясының Фурье түрлендіруі неге тең?",
         'opts': ["0", "1", "delta(w)", "Шексіздік"], 'ans': "1", 'diff': 99},
    ]

    # --- IRT Selection & Scoring Engine ---
    if not st.session_state.quiz_complete:
        st.subheader(f"{st.session_state.quiz_step}-сұрақ, барлығы 5")
        st.progress(st.session_state.ability_score / 100,
                    text=f"Жүйенің студент қабілетіне ағымдағы бағасы: {st.session_state.ability_score:.1f}/100")

        # 1. Find the best question (the closest difficulty to current ability)
        if st.session_state.current_q_data is None:
            available_questions = [q for q in question_bank if q['q'] not in st.session_state.asked_questions]
            # Sort by absolute difference between ability and difficulty
            available_questions.sort(key=lambda x: abs(x['diff'] - st.session_state.ability_score))
            # Find all questions that share the same closest difficulty distance
            best_diff = abs(available_questions[0]['diff'] - st.session_state.ability_score)
            best_candidates = [q for q in available_questions if abs(q['diff'] - st.session_state.ability_score) == best_diff]
            # Randomly select from the best candidates to avoid repeating the same question
            st.session_state.current_q_data = random.choice(best_candidates)
            st.session_state.asked_questions.append(st.session_state.current_q_data['q'])

        q_data = st.session_state.current_q_data

        # Display Question info
        st.caption(f"Жүйе ағымдағы қабілетке сүйене отырып, күрделілік деңгейі {q_data['diff']}/100 сұрақты таңдады.")
        user_choice = st.radio(f"**{q_data['q']}**", q_data['opts'], index=None, key=f"q_{st.session_state.quiz_step}")

        if st.button("Жіберу"):
            if user_choice:
                # 2. Proportional IRT Scoring Logic
                diff_variance = q_data['diff'] - st.session_state.ability_score

                if user_choice == q_data['ans']:
                    # Reward: Base points + bonus if the question was harder than their current ability
                    reward = max(5.0, 10.0 + (diff_variance * 0.4))
                    st.session_state.ability_score = min(100.0, st.session_state.ability_score + reward)
                    st.success(f"✅ Дұрыс! Қабілет деңгейі {reward:.1f} ұпайға жоғарылады.")
                else:
                    # Penalty: Base points + extra penalty if the question was easier than their current ability
                    penalty = max(5.0, 10.0 - (diff_variance * 0.4))
                    st.session_state.ability_score = max(0.0, st.session_state.ability_score - penalty)
                    st.error(f"❌ Қате. Қабілет деңгейі -{penalty:.1f} ұпайға төмендеді.")

                # Move to next step
                if st.session_state.quiz_step >= 5:
                    st.session_state.quiz_complete = True
                else:
                    st.session_state.quiz_step += 1
                    st.session_state.current_q_data = None

                import time

                time.sleep(2)  # Show the result before reloading
                st.rerun()
            else:
                st.warning("Алдымен жауапты таңдаңыз.")

    else:
        # --- Final Results Dashboard ---
        st.success("🎉 Адаптивті бағалау аяқталды!")
        st.metric(label="Қорытынды когнитивті қабілет (Тета көрсеткіші)", value=f"{st.session_state.ability_score:.1f}/100")

        st.markdown("### 🤖 Автономды педагогикалық әрекет:")
        if st.session_state.ability_score >= 80:
            st.info("Студент сандық логиканы жоғары деңгейде меңгергенін көрсетті. Күрделі есептер жинағына бағытталуда.")
        elif st.session_state.ability_score >= 40:
            st.warning("Студент орташа құзыреттілік көрсетті. Орта деңгейдегі білім олқылықтары қарау үшін белгіленді.")
        else:
            st.error(
                "Студенттің математикалық негізгі дағдылары жеткіліксіз. Негізгі арифметика/алгебра бойынша ЖИ (AI) тьютор араласуы іске қосылды.")

        if st.button("Бағалауды қайта бастау"):
            st.session_state.quiz_step = 1
            st.session_state.ability_score = 50.0
            st.session_state.asked_questions = []
            st.session_state.quiz_complete = False
            st.session_state.current_q_data = None
            st.rerun()

with tab3:
    st.header("📝 Мөлдір ЖИ (AI) эссе бағалаушы")
    st.markdown("Этикалық ЖИ (AI) стандарттарына сәйкестікті көрсету. Бұл модуль жазбаша жауаптарды бағалау үшін табиғи тілді өңдеуді (Natural Language Processing) қолданады, сонымен қатар толық мөлдір, тексерілетін шешім матрицасын ұсынады.")

    # --- API Key Input ---
    api_key = st.secrets["api_key"]

    def load_example():
        st.session_state.essay_text = "Quicksort алгоритмі — 'бөліп ал да билей бер' (divide-and-conquer) стратегиясын қолданатын өте тиімді сұрыптау әдісі. Ол массивтен 'тірек' (pivot) элементін таңдап, қалған элементтерді тірек элементінен кіші немесе үлкен екеніне қарай екі ішкі массивке бөледі. Алайда, тірек элементі нашар таңдалса, оның ең нашар уақыттық күрделілігі O(N^2) болады, сондықтан қазіргі жүйелерде кездейсоқ тірек элементтері жиі қолданылады."

    st.button("Студент жұмысының мысалын жүктеу", on_click=load_example)
    # --- UI Elements ---
    essay_input = st.text_area(
        "Студент эссесін осында қойыңыз:",
        value=st.session_state.essay_text if 'essay_text' in st.session_state else "",
        height=200,
        placeholder="Кез келген эссені осында жазыңыз немесе қойыңыз. ЖИ (AI) оны компьютерлік ғылымдар принциптері бойынша динамикалық түрде бағалайды..."
    )

    if st.button("Бағалау және мөлдір кері байланыс жасау"):
        if essay_input.strip() == "":
            st.warning("Бағалау үшін эссе енгізіңіз.")
        else:
            with st.spinner("Семантикалық талдау жүргізілуде..."):
                try:
                    # Initialize the modern genai client
                    client = genai.Client(api_key=api_key)

                    # --- The Prompt Engineering (The Secret Sauce) ---
                    full_prompt = f"""
                    Сіз 'Білім берудегі бағалаудың білікті жүйесі' (БББЖ/IEAS) жүйесісіз.
                    Төмендегі компьютерлік ғылымдар эссесін 100 ұпай бойынша бағалаңыз.
                    Жауабыңызды МІНДЕТТІ ТҮРДЕ қазақ тілінде және дәл осы форматта беріңіз, мөлдір түсіндірмелілік қамтамасыз етіңіз. Кіріспе сөздер жазбаңыз, тек матрицаны шығарыңыз.

                    **Жалпы баға:** [Ұпай]/100

                    **1. Тұжырымдаманы меңгеру (40 ұпай)**
                    * ЖИ (AI) ескертпесі: [Студенттің түсінігін қысқаша талдау]
                    * Ұпай: [X]/40

                    **2. Техникалық дәлдік (30 ұпай)**
                    * ЖИ (AI) ескертпесі: [Техникалық тұжырымдары мен күрделіліктерін қысқаша талдау]
                    * Ұпай: [X]/30

                    **3. Синтаксис және құрылым (30 ұпай)**
                    * ЖИ (AI) ескертпесі: [Жазу сапасын қысқаша талдау]
                    * Ұпай: [X]/30

                    **Педагогикалық ұсыныс:** [Студенттің ең әлсіз бөліміне негізделген, келесі не оқу керек екендігі туралы бір сөйлем].

                    ---
                    **БАҒАЛАУҒА АРНАЛҒАН СТУДЕНТ ЭССЕСІ:**
                    {essay_input}
                    """

                    # Call the live API using the new method
                    response = client.models.generate_content(
                        model='gemini-3-flash-preview',  # Using the cutting-edge fast model
                        contents=full_prompt
                    )

                    st.success("✅ Тікелей талдау аяқталды!")
                    st.divider()

                    # Display the genuine, dynamically generated response
                    st.markdown("### 🔍 ЖИ (AI) шешімінің талдамасы (Түсіндірмелілік деңгейі)")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"API байланыс қатесі")