import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_ago = self.today - dt.timedelta(days=6)

    def add_record(self, records):
        self.records.append(records)

    def get_today_stats(self):
        return sum(i.amount for i in self.records if i.date == self.today)

    def get_today_spent(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        week_spent = 0
        for i in self.records:
            if self.today >= i.date >= self.week_ago:
                week_spent += i.amount
        return week_spent


class CashCalculator(Calculator):

    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1
    dict_rate = {'eur': [EURO_RATE, 'Euro'],
                 'usd': [USD_RATE, 'USD'],
                 'rub': [RUB_RATE, 'руб']}

    def get_today_cash_remained(self, current):
        remainder = self.get_today_spent()
        today_stats = self.get_today_stats()
        course, rate = self.dict_rate[current]
        total_spent = abs(remainder / course)
        if self.limit > today_stats:
            return f'На сегодня осталось {total_spent:.2f} {rate}'
        elif self.limit < today_stats:
            return f'Денег нет, держись: твой долг - {total_spent:.2f} {rate}'
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        more_calories = self.get_today_spent()
        spent_calories = self.get_today_stats()
        if self.limit >= spent_calories:
            return (f'Сегодня можно съесть что-нибудь ещё,'
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
