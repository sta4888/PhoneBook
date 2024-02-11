from typing import List

import click as click


class PhoneBook:
    """
    Класс PhoneBook представляет собой телефонный справочник.
    Справочник хранит информацию о контактах в текстовом файле.

    Структура записи в файле:
    Фамилия Имя Отчество Организация Рабочий_телефон Личный_телефон

    Attributes:
    filename (str): Имя файла для хранения контактов.
    """

    def __init__(self, filename):
        """
        Инициализация объекта PhoneBook.

        Args:
        filename (str): Имя файла для хранения контактов.
        """
        self.filename = filename

    def display_page(self, page_number, page_size=10) -> None:
        """
        Выводит на экран заданную страницу контактов из справочника.

        Args:
        page_number (int): Номер страницы.
        page_size (int): Размер страницы (по умолчанию 10).
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            for line in lines[start_index:end_index]:
                print(line.strip())

    def add_contact(self, contact) -> None:
        """
        Добавляет новый контакт в справочник.
        Контакт должен быть записан через запятую

        Args:
        contact (str): Строка с информацией о контакте.
        """
        with open(self.filename, 'a') as file:
            file.write(contact + '\n')

    def edit_contact(self, old_contact, new_contact) -> None:
        """
        Редактирует существующий контакт в справочнике.

        Args:
        old_contact (str): Строка с информацией о контакте, которую нужно заменить.
        new_contact (str): Строка с новой информацией о контакте.
        """
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        with open(self.filename, 'w') as file:
            for line in lines:
                if line.strip() == old_contact:
                    file.write(new_contact + '\n')
                else:
                    file.write(line)

    def search_contacts(self, **kwargs) -> List:
        """
        Поиск контактов по заданным характеристикам.

        Args:
        **kwargs: Пары "атрибут=значение" для поиска контактов.

        Returns:
        list: Список контактов, удовлетворяющих условиям поиска.
        """
        keys = {
            'фамилия': 0,
            'имя': 1,
            'отчество': 2,
            'организация': 3,
            'рабочий': 4,
            'личный': 5
        }
        found_contacts = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                contact_info = line.strip().split(',')
                is_match = True
                print(contact_info)
                for key, value in kwargs.items():
                    if contact_info[keys[key]].strip() != value:
                        is_match = False
                        break
                if is_match:
                    found_contacts.append(line.strip())
        return found_contacts


@click.group()
@click.option('--filename', default='contacts.pb', help='Имя файла для хранения контактов.')
@click.pass_context
def cli(ctx, filename):
    """
    Командная строка для управления телефонным справочником.
    """
    ctx.obj = PhoneBook(filename)


@cli.command()
@click.argument('page_number', type=int)
@click.option('--page_size', default=10, help='Размер страницы (по умолчанию 10).')
@click.pass_obj
def display(obj, page_number, page_size):
    """
    Выводит на экран заданную страницу контактов из справочника.
    """
    obj.display_page(page_number, page_size)


@cli.command()
@click.argument('contact')
@click.pass_obj
def add(obj, contact):
    """
    Добавляет новый контакт в справочник (Иванов, Иван, ...).
    """
    obj.add_contact(contact)


@cli.command()
@click.argument('old_contact')
@click.argument('new_contact')
@click.pass_obj
def edit(obj, old_contact, new_contact):
    """
    Редактирует существующий контакт в справочнике.
    """
    obj.edit_contact(old_contact, new_contact)


@cli.command()
@click.argument('search_criteria', nargs=-1)
@click.pass_obj
def search(obj, search_criteria):
    """
    Поиск контактов по заданным характеристикам.
    """
    search_dict = {}
    for criteria in search_criteria:
        key, value = criteria.split('=')
        search_dict[key] = value
    found_contacts = obj.search_contacts(**search_dict)
    click.echo("Найденные контакты:")
    for contact in found_contacts:
        click.echo(contact)


if __name__ == '__main__':
    cli()
