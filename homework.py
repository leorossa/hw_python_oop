import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, records):
        self.records.append(records)

    def get_today_stats(self):
        self.total_spent = 0
        for i in self.records:
            if i.date == dt.date.today():
                self.total_spent += i.amount
        return self.total_spent

    def get_week_stats(self):
        self.week_spent = 0
        week_ago = dt.date.today() - dt.timedelta(days=7)
        today = dt.date.today()
        for i in self.records:
            if today >= i.date >= week_ago:
                self.week_spent += i.amount
        return self.week_spent


class CashCalculator(Calculator):

    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1
    distonary_rate = {EURO_RATE: 'eur', USD_RATE: 'usd', RUB_RATE: 'rub'}
    rate_name = {'rub': 'руб', 'eur': 'Euro', 'usd': 'USD'}

    def get_today_cash_remained(self, current):
        remainder = abs(self.limit - self.get_today_stats())
        for i in self.distonary_rate:
            surname = self.rate_name[self.distonary_rate[i]]
            if self.distonary_rate[i] == current:
                if self.limit > self.get_today_stats():
                    return f'На сегодня осталось {round(remainder/i, 2)} {surname}'
                elif self.limit < self.get_today_stats():
                    return f'Денег нет, держись: твой долг - {round((remainder/i), 2)} {surname}'
                else:
                    return ('Денег нет, держись')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        spent_calories = super().get_today_stats()
        more_calories = self.limit - spent_calories
        if self.limit >= spent_calories:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {more_calories} кКал'
        else:
            return f'Хватит есть!'


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
    cash_calculator.add_record(Record(amount=145, comment="кофе")) 
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))
