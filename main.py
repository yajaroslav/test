import sqlite3
import bcrypt

NAME = 'sport_item.db'
conn = sqlite3.connect(NAME)
cursor = conn.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL
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
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
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


def add_item(name, quantity):
    # добавление предмета в бд
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    # проверяем, не существует ли предмет с таким именем
    cursor.execute("SELECT * FROM items WHERE name = ?", (name,))
    if cursor.fetchone():
        conn.close()
        return False, "предмет с таким названием уже существует"
    try:
        cursor.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
        conn.close()
        return True, f"предмет {name} успешно добавлен"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Ошибка при добавлении: {e}"


'''
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
# fgggggggg

