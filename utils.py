def get_language(text: str, language_code: str) -> str:
    languages = {
        "Select a language": {
            "UZ": "Tilni tanlang:",
            "RU": "Выберите язык:",
            "EN": "Select a language:"
        },
        "Write an appeal": {
            "UZ": "Murojat yozish",
            "RU": "Написать обращение",
            "EN": "Write an appeal"
        },
        "My appeals": {
            "UZ": "Mening murojatlarim",
            "RU": "Мои обращения",
            "EN": "My appeals"
        },
        "Main menu": {
            "UZ": "Asosiy menyu",
            "RU": "Главное меню",
            "EN": "Main menu"
        },
        "Share contact": {
            "UZ": "Kontakt ulashish",
            "RU": "Поделиться контактом",
            "EN": "Share contact"
        },
        "Please share your contact details": {
            "UZ": "Iltimos, kontakt ma'lumotlaringizni ulashing",
            "RU": "Пожалуйста, поделитесь вашими контактными данными",
            "EN": "Please share your contact details"
        },
        "For your appeals": {
            "UZ": "Sizning murojatlariz uchun",
            "RU": "Для ваших обращений",
            "EN": "For your appeals"
        },
        "Write your appeal": {
            "UZ": "Murojaatingizni yozing",
            "RU": "Напишите ваше обращение",
            "EN": "Write your appeal"
        },
        "Upload file": {
            "UZ": "File yuklash",
            "RU": "Загрузить файл",
            "EN": "Upload file"
        },
        "Upload file or press '-'": {
            "UZ": "File yuklang yoki '-' belgisini bosing",
            "RU": "Загрузите файл или нажмите '-'",
            "EN": "Upload file or press '-'"
        },
        "Please upload the file": {
            "UZ": "Iltimos, faylni yuklang",
            "RU": "Пожалуйста, загрузите файл",
            "EN": "Please upload the file"
        },
        "Your appeal has been saved": {
            "UZ": "Murojaatingiz saqlandi",
            "RU": "Ваше обращение сохранено",
            "EN": "Your appeal has been saved"
        },
        "You have no appeals": {
            "UZ": "Sizda murojatlar yo'q",
            "RU": "У вас нет обращений",
            "EN": "You have no appeals"
        }
    }

    return languages.get(text, {}).get(language_code, text)