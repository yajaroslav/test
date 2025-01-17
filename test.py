# git config --system http.sslCAPath G:/@ Ярослав/Pyton/Git/mingw64/etc/ssl/certs/ca-bundle.crt


import sqlite3


def delete_items_table(db_name: str) -> None:
    """Удаляет таблицу 'items' из указанной базы данных SQLite.

    Args:
        db_name: Имя файла базы данных.
    """
    try:
        # Подключение к базе данных
        con = sqlite3.connect(db_name)
        cursor = con.cursor()

        # SQL запрос для удаления таблицы 'items', если она существует
        cursor.execute("DROP TABLE IF EXISTS items;")

        # Фиксация изменений
        con.commit()
        print(f"Таблица 'items' успешно удалена из базы данных '{db_name}'.")

    except sqlite3.Error as e:
        print(f"Ошибка при удалении таблицы 'items': {e}")

    finally:
        # Закрытие соединения с базой данных
        if 'conn' in locals():
            con.close()


if __name__ == "__main__":
    database_name = 'sport_item.db'
    delete_items_table(database_name)

