from api import db
from api.models import object_as_dict
from Tracker import PriceMonitor
import yfinance as yf
from datetime import datetime as dt


# make a transaction class
class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # negative share amounts will count as a sell --> no need to store the type
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Float, nullable=False)

    # this is the date of the transaction, which should not be changed
    date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())

    # add a fund object
    fund = db.relationship("FundModel", backref="transactions", uselist=False)

    # add a holding object (that was directly affected)
    holding = db.relationship(
        'HoldingModel', backref='transactions', uselist=False)

    # calculate the transaction total
    def total(self):
        total = float(self.price) * float(self.shares)
        print(f"Total: {total}")
        return total


# make a fund model --> will have record dates (and can be sorted)
class FundModel(db.Model):
    __tablename__ = 'funds'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # bind the fund to a transaction
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'), nullable=False)

    name = db.Column(db.String(50), nullable=False)

    # have some sector portfolios
    sector_portfolios = db.relationship(
        'SectorPortfolioModel', backref='funds', lazy='dynamic')

    # make a function to get the entire fund as a dict
    def as_dict(self):
        fund_dict = object_as_dict(self)

        # get the sector portfolios
        sector_portfolio_dicts = [sector_portfolio.as_dict(
        ) for sector_portfolio in self.sector_portfolios]

        fund_dict['sector_portfolios'] = sector_portfolio_dicts
        fund_dict['value'] = sum([portfolio['value']
                                  for portfolio in sector_portfolio_dicts])

        return fund_dict


# make a sector portfolio model
class SectorPortfolioModel(db.Model):
    __tablename__ = 'sector_portfolios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=True)

    # bind the sector to a fund
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'))

    # add some holdings
    holdings = db.relationship(
        'HoldingModel', backref='sector_portfolios', lazy='dynamic')

    # add a capital adjustment
    cap_adj = db.Column(db.Float, nullable=False)

    # make a function to display it as a dictionary
    def as_dict(self):
        sector_portfolio_dict = object_as_dict(self)

        holding_dicts = [object_as_dict(holding)
                         for holding in self.holdings]

        # add the holdings to the main dict
        sector_portfolio_dict['holdings'] = holding_dicts
        sector_portfolio_dict['value'] = sum(
            [holding.value() for holding in self.holdings]) + self.cap_adj

        return sector_portfolio_dict


# make a holding model
class HoldingModel(db.Model):
    __tablename__ = 'holdings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # bind the holding to a sector portfolio and a transaction
    sector_id = db.Column(db.Integer, db.ForeignKey(
        'sector_portfolios.id'), nullable=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'), nullable=True)

    # add a ticker
    ticker = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)

    # make a method to get the current value from the YF api
    def value(self, date=dt.now()):
        monitor = PriceMonitor(self.ticker)

        price = monitor.get_close_price(date=date)

        position_value = self.shares * price

        return round(position_value, 2)


if __name__ == '__main__':
    # check if there are any transactions
    if len(TransactionModel.query.all()) == 0:
        transaction = TransactionModel(
            ticker='XXXXX', price=0, shares=0, date=dt(year=1997, month=1, day=1))
        db.session.add(transaction)
        db.session.commit()
