import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, records):
        self.records.append(records)

    def today_stats(self):
        today = dt.date.today()
        return sum(i.amount for i in self.records if i.date == today)

    def get_today_stats(self):
        return self.today_stats()

    def get_today_spent(self):
        return self.limit - self.get_today_stats()

    def week_stats(self):
        start_week = dt.date.today()
        end_week = start_week - dt.timedelta(days=6)
        return sum(i.amount for i in self.records
                   if start_week >= i.date >= end_week)

    def get_week_stats(self):
        return self.week_stats()


class CashCalculator(Calculator):

    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1
    dict_rate = {'eur': (EURO_RATE, 'Euro'),
                 'usd': (USD_RATE, 'USD'),
                 'rub': (RUB_RATE, 'руб')}

    def get_today_cash_remained(self, current):
        today_spent = self.get_today_spent()
        if today_spent == 0:
            return 'Денег нет, держись'
        course, rate = self.dict_rate[current]
        remainder = abs(today_spent / course)
        if today_spent > 0:
            return f'На сегодня осталось {remainder:.2f} {rate}'
        return f'Денег нет, держись: твой долг - {remainder:.2f} {rate}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        more_calories = self.get_today_spent()
        if more_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {more_calories} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000, comment='бар в Танин др',
                                      date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
