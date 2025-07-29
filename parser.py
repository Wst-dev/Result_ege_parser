import json
import os
import glob
import csv
import re

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

def load_results_history():
    """Загружает историю результатов из results_history.json"""
    if os.path.exists('results_history.json'):
        try:
            with open('results_history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_results_history(history):
    """Сохраняет историю результатов в results_history.json"""
    with open('results_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

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

def find_student_places(student_id):
    """Ищет место абитуриента по ID во всех csv-файлах в папке и сравнивает с предыдущими результатами"""
    csv_files = glob.glob('*.csv')
    found = False
    history = load_results_history()
    new_history = {}
    for filename in csv_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = list(csv.DictReader(f, delimiter=';'))
                faculty_name = os.path.splitext(os.path.basename(filename))[0].replace('_', ' ')
                faculty_name = re.sub(r'\.\d{4}-\d{2}-\d{2}.*$', '', faculty_name)
                place = 1
                student_place = None
                consent_list = []
                id_field = "ID участника"
                consent_field = "Подано согласие" 
                for row in reader:
                    if id_field and row[id_field].strip() == student_id:
                        student_place = place
                        student_consent_place = len(consent_list) + 1
                    if id_field and consent_field and row[consent_field].strip() != '—':
                        consent_list.append(row[id_field].strip())
                    place += 1

                new_history[filename] = {
                    'student_place': student_place,
                    'student_consent_place': student_consent_place,
                    'consent_count': len(consent_list)
                }
                prev = history.get(filename, {})
                prev_place = prev.get('student_place')
                prev_consent_place = prev.get('student_consent_place')
                print(f"{faculty_name}:")
                # --- Позиция среди подавших согласие ---
                consent_str = f"- позиция относительно поданных заявлениях: {student_consent_place if student_consent_place is not None else 'нет в списке'}"
                consent_change = ""
                if prev:
                    if prev_consent_place is not None and student_consent_place is not None:
                        diff = prev_consent_place - student_consent_place
                        if diff > 0:
                            consent_change = f" (стали выше на {abs(diff)} позиций)"
                        elif diff < 0:
                            consent_change = f" (стали ниже на {abs(diff)} позиций)"
                        else:
                            consent_change = " (позиция не изменилась)"
                    elif prev_consent_place is None and student_consent_place is not None:
                        consent_change = " (появились в списке подавших согласие)"
                    elif prev_consent_place is not None and student_consent_place is None:
                        consent_change = " (вышли из списка подавших согласие)"
                print(consent_str + consent_change)
                # --- Общее количество заявлений ---
                print(f"- общее количество заявлений о зачислении: {len(consent_list)}")
                # --- Обычная позиция ---
                place_str = f"- позиция в списке: {student_place if student_place is not None else 'нет в списке'}"
                place_change = ""
                if prev:
                    if prev_place is not None and student_place is not None:
                        diff = prev_place - student_place
                        if diff > 0:
                            place_change = f" (стали выше на {abs(diff)} позиций)"
                        elif diff < 0:
                            place_change = f" (стали ниже на {abs(diff)} позиций)"
                        else:
                            place_change = " (позиция не изменилась)"
                    elif prev_place is None and student_place is not None:
                        place_change = " (появились в списке)"
                    elif prev_place is not None and student_place is None:
                        place_change = " (вышли из списка)"
                print(place_str + place_change + "\n")
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")
    save_results_history(new_history)
    if not csv_files:
        print("CSV-файлы не найдены в папке.")

def main():
    """Главная функция программы"""
    print("=== Программа поиска места абитуриента ===")
    
    student_id = get_student_id()
    
    if student_id:
        print(f"\nТекущий ID абитуриента: {student_id}")
        find_student_places(student_id)
    else:
        print("Программа завершена без получения ID")

if __name__ == "__main__":
    main()
