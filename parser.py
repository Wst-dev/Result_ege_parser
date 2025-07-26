import json
import os

def load_settings():
    """Загружает настройки из settings.json"""
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_settings(settings):
    """Сохраняет настройки в settings.json"""
    try:
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении настроек: {e}")
        return False

def get_student_id():
    """Получает ID абитуриента - либо из файла, либо запрашивает у пользователя"""
    

    settings = load_settings()
    

    if 'student_id' in settings and settings['student_id']:
        student_id = settings['student_id']
        print(f"ID абитуриента найден: {student_id}")
        return student_id
    

    while True:
        try:
            student_id = input("Введите ID абитуриента: ").strip()
            if not student_id.isdigit():
                print("ID должен содержать только цифры. Попробуйте еще раз.")
                continue
            if not (6 <= len(student_id) <= 8):
                print("Длина ID должна быть от 6 до 8 символов. Попробуйте еще раз.")
                continue
            settings['student_id'] = student_id
            if save_settings(settings):
                print(f"ID абитуриента '{student_id}' сохранен в settings.json")
            else:
                print("Не удалось сохранить настройки, но ID будет использован в текущей сессии")
            return student_id
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем")
            return None

def main():
    """Главная функция программы"""
    print("=== Программа управления ID абитуриента ===")
    
    student_id = get_student_id()
    
    if student_id:
        print(f"\nТекущий ID абитуриента: {student_id}")
    else:
        print("Программа завершена без получения ID")

if __name__ == "__main__":
    main()
