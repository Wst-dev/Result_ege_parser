import json
import os
import glob
import csv

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

def find_student_places(student_id):
    """Ищет место абитуриента по ID во всех csv-файлах в папке"""
    csv_files = glob.glob('*.csv')
    found = False
    for filename in csv_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                place = 1
                faculty_name = os.path.splitext(os.path.basename(filename))[0].replace('_', ' ')
                for row in reader:
                    id_field = None
                    for key in row.keys():
                        if 'id' in key.lower():
                            id_field = key
                            break
                    if not id_field:
                        continue
                    if row[id_field].strip() == student_id:
                        print(f"На факультете {faculty_name} абитуриент находится на {place} месте")
                        found = True
                        break
                    place += 1
                else:
                    print(f"В файле '{filename}' абитуриент с ID {student_id} не найден.")
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")
    if not csv_files:
        print("CSV-файлы не найдены в папке.")
    if not found and csv_files:
        print(f"Абитуриент с ID {student_id} не найден ни в одном из файлов.")

def main():
    """Главная функция программы"""
    print("=== Программа управления ID абитуриента ===")
    
    student_id = get_student_id()
    
    if student_id:
        print(f"\nТекущий ID абитуриента: {student_id}")
        find_student_places(student_id)
    else:
        print("Программа завершена без получения ID")

if __name__ == "__main__":
    main()
