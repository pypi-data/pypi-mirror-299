months = {
    "en": {
        "January": "January", "February": "February", "March": "March",
        "April": "April", "May": "May", "June": "June", "July": "July",
        "August": "August", "September": "September", "October": "October",
        "November": "November", "December": "December",
    },
    "swa": {
        "January": "Januari", "February": "Februari", "March": "Machi",
        "April": "Aprili", "May": "Mei", "June": "Juni", "July": "Julai",
        "August": "Agosti", "September": "Septemba", "October": "Octoba",
        "November": "Novemba", "December": "Desemba",
    },
}

lesson_title = {
    "en": "LESSON",
    "swa": "SOMO LA",
}

def custom_title_case(s):
    words = s.split()
    titled_words = []
    for word in words:
        if "'" in word:
            parts = word.split("'")
            titled_word = parts[0].capitalize() + "'" + parts[1].lower()
        else:
            titled_word = word.capitalize()
        titled_words.append(titled_word)
    return ' '.join(titled_words)

def get_lesson_text(lang, case="title"):
    lesson_text = lesson_title[lang]
    if case == "title":
        lesson_text = custom_title_case(lesson_text)
    elif case == "upper":
        lesson_text = lesson_text.upper()
    return lesson_text