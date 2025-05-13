from datetime import datetime

from sqlalchemy import text

from machine_tools_2.app.db.session import engine


def add_test_machine():
    with engine.connect() as connection:
        # SQL запрос для вставки тестовой записи
        insert_query = text(
            """
            INSERT INTO machines (
                name, type, manufacturer, model, year, serial_number,
                spindle_power, spindle_speed, table_size_x, table_size_y,
                table_size_z, tool_count, control_system, created_at, updated_at
            ) VALUES (
                'Test Machine', 'CNC', 'Test Manufacturer', 'TM-100',
                2024, 'SN123456', 15.0, 24000, 500, 500, 400,
                12, 'Fanuc', :created_at, :updated_at
            )
        """
        )

        # Текущее время для created_at и updated_at
        now = datetime.utcnow()

        # Выполняем запрос
        connection.execute(insert_query, {"created_at": now, "updated_at": now})
        connection.commit()

        print("Тестовая запись успешно добавлена!")


if __name__ == "__main__":
    add_test_machine()
