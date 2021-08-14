"""Калькулятор денег и калорий.
Считает траты и полученные калории за день/неделю, сверяется с лимитом.
"""
import datetime as dt


class Record:
    """Класс для создания записей."""
    def __init__(self, amount, comment, date=None):
        # денежная сумма или количество килокалорий
        self.amount = float(amount)
        # поясняет на что потрачены деньги или откуда взялись калории
        self.comment = comment

        if date is not None:
            date_format = '%d.%m.%Y'
            # перевод строки в формат даты
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()


class Calculator:
    """Класс для хранения и суммирования записей."""
    def __init__(self, limit):
        self.limit = limit
        # пустой список, в котором потом будут храниться записи
        self.records = []

    def add_record(self, record):
        """Сохранение новой записи о приеме пищи/расходах."""
        self.records.append(record)

    def get_today_stats(self):
        """Сколько съедено/потрачено сегодня."""
        today = dt.date.today()
        today_stats = sum(
            record.amount for record in self.records
            if record.date == today)
        return today_stats

    def get_week_stats(self):
        """Сколько калорий получено/денег потрачено за последние 7 дней."""
        today = dt.date.today()
        period = dt.timedelta(days=7)
        week_ago_date = today - period
        week_stats = sum(
            record.amount for record in self.records
            if week_ago_date <= record.date <= today)
        return week_stats

    # в методах экземпляра класса
    # есть повторяющееся действие по подсчету остатка
    # есть смысл его также посчитать в родительском классе
    def get_today_remained(self):
        """Сколько осталось от лимита."""
        balance = self.limit - self.get_today_stats()
        return balance


class CaloriesCalculator (Calculator):
    """Класс для определения остатка по лимиту калорий."""
    def get_calories_remained(self):
        """Сколько калорий можно получить сегодня."""
        today_calories_remained = int(self.get_today_remained())

        if today_calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{today_calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator (Calculator):
    """Класс для определения остатка денег в выбранной валюте."""
    USD_RATE = 73.0
    EURO_RATE = 85.0

    def get_today_cash_remained(self, currency):
        """Сколько ещё можно потратить сегодня."""
        # если баланс уже равен 0, завершаем функцию
        if self.get_today_remained() == 0:
            return 'Денег нет, держись'
        # словарь валют и их курса к рублю
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', 1.0),
        }
        # проверяем корректность ввода валюты
        for i in currencies:
            is_correct = i == currency
            if is_correct:
                break
        if not is_correct:
            return 'Указана некорректная валюта'
        # это кажется проще, чем вызывать через индексы списка
        currency_name, currency_rate = currencies[currency]
        # состояние дневного баланса с учетом валюты
        today_cash_remained = round(
            self.get_today_remained() / currency_rate, 2)
        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_name}'
        else:
            return ('Денег нет, держись: '
                    f'твой долг - {abs(today_cash_remained)} {currency_name}')


# создадим калькулятор денег с дневным лимитом 1000
if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(
                                    amount=145,
                                    comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(
                                    amount=300,
                                    comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(
                                    amount=3000,
                                    comment='бар в Танин др',
                                    date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # На сегодня осталось 555 руб
