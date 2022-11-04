# `machine_tools`

`machine_tools` - модуль работы с базой данных станков.
---
---

Поддерждиваемые функции:

	Получение списка станков:
		names = machine_tools.list_mt(group=any_group, 
                                          type_=any_type)

	Получение характеристик станка (в формате DataFrame):
		chars = machine_tools.characteristics(name=any_name)

	Получение паспортных данных станка (в формате DataFrame):
		table = machine_tools.passport_data(name=any_name)

---

Поддерждиваемые классы:

    Класс "Материал":
        Создать класс:
            machine_tools = machine_tools.MachineTool()

        Показать передаваемые параметры класса:
            print(machine_tools.__doc__)

        Показать присвоенные параметры класса:
            machine_tools.show
        
        Задать настройки по умолчанию:
            machine_tools.get_default_settings

        Изменить станок:
            machine_tools.update_chars(name = new_name)

        Изменить значение параметра "Жесткость системы СПИД":
            machine_tools.update_hard_MFTD(hard_MFTD = new_hard_MFTD)

        Очистить характеристики:
            machine_tools.clear_characteristics

---