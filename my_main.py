import sqlite3
import bcrypt

# новый, используемый, сломанный | used


NAME = 'sport_item.db'
conn = sqlite3.connect(NAME)
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            new INTEGER DEFAULT 0,
            used INTEGER DEFAULT 0,
            broken INTEGER DEFAULT 0
        )''')

conn.commit()
conn.close()


def register_user(username, password):
    # регистрация пользователя
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    # проверяем, не существует ли пользователь с таким именем
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Имя пользователя уже занято."

    # хешируем пароль
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

    # добавляем пользователя в базу данных
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, "user"))
        conn.commit()
        conn.close()
        return True, "Пользователь успешно зарегистрирован."
    except sqlite3.Error as e:
        conn.close()
        return False, f"Ошибка при регистрации: {e}"


def login_user(username, password):
    # вход пользователя
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    # Получаем хешированный пароль из базы данных
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        hashed_password = result[0].encode('utf-8')
        password_bytes = password.encode('utf-8')
        if bcrypt.checkpw(password_bytes, hashed_password):
            return True, "Вход выполнен успешно."
        else:
            return False, "Неверный пароль."
    else:
        return False, "Пользователь не найден."


def item_request(name, count):
    pass
    # проверял, не работает)
    # ожидать подтверждения, после item_request_accept(name, count)


def item_request_accept(name, count):
    # переводит из new в used по названию заданное кол-во

    conn = sqlite3.connect("sport_item.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT new, used FROM items WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            current_new, current_used = result
            if current_new >= count:
                new_value = current_new - count
                used_value = current_used + count
                cursor.execute("UPDATE items SET new = ?, used = ? WHERE name = ?", (new_value, used_value, name))
                conn.commit()
                return True, f"Переведено {count} шт. для '{name}'."
            else:
                return False, f"Недостаточно элементов в столбце 'new' для '{name}'."
        else:
            return False, f"Предмет с именем '{name}' не найден."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Ошибка при работе с базой данных: {e}"
    finally:
        conn.close()


def add_item(name, count):
    # добавление предмета в бд
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    # проверяем, не существует ли предмет с таким именем
    cursor.execute("SELECT * FROM items WHERE name = ?", (name,))
    if cursor.fetchone():
        conn.close()
        return False, "предмет с таким названием уже существует"
    try:
        cursor.execute("INSERT INTO items (name, new) VALUES (?, ?)", (name, count))
        conn.commit()
        conn.close()
        return True, f"предмет {name} успешно добавлен"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Ошибка при добавлении: {e}"


'''
проверки, все работает

add_item("что-то", 40)
print(add_item("что-то", 40))
print(item_request_accept("что-то", 20))

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            success, message = register_user(username, password)
            print(message)      
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            success, message = login_user(username, password)
            print(message)
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
'''

