# `machine_tools`

`machine_tools` - модуль работы с базой данных станков.

Поддерждиваемые функции:

	Получение списка станков:
		names = machine_tools.list_mt(group=any_group, type_=any_type)

	Получение характеристик станка (в формате DataFrame):
		chars = machine_tools.characteristics(name=any_name)

	Получение паспортных данных станка (в формате DataFrame):
		table = machine_tools.passport_data(name=any_name)

