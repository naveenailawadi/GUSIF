from api import db


# make a transaction class
class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)

    # negative share amounts will count as a sell --> no need to store the type
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Float, nullable=False)

    # this is the date of the transaction, which should not be changed
    date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())

    # add a fund object
    fund = db.relationship("FundModel", backref="transactions")

    # add a holding object (that was directly affected)
    holding = db.relationship('HoldingModel', backref='transactions')


# make a fund model --> will have record dates (and can be sorted)
class FundModel(db.Model):
    __tablename__ = 'funds'
    id = db.Column(db.Integer, primary_key=True)

    # bind the fund to a transaction
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'), nullable=False)

    name = db.Column(db.String(50), nullable=False)

    # have some sector portfolios
    sector_portfolios = db.relationship(
        'SectorPortfolioModel', backref='funds', dynamic=True)


# make a sector portfolio model
class SectorPortfolioModel(db.Model):
    __tablename__ = 'sector_portfolios'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=True)

    # bind the sector to a fund
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'))

    # add some holdings
    holdings = db.relationship(
        'HoldingModel', backref='sector_portfolios', dynamic=True)


# make a holding model
class HoldingModel(db.Model):
    __tablename__ = 'holdings'
    id = db.Column(db.Integer, primary_key=True)

    # bind the holding to a sector portfolio and a transaction
    sector_id = db.Column(db.Integer, db.ForeignKey(
        'sector_portfolios.id'))
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.id'))

    # add a ticker
    ticker = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)


# make a function that copies models
def copy_model(model):
    db.session.expunge(model)

    db.session.make_transient(model)

    return model


if __name__ == '__main__':
    # check if there are any transactions
    if len(TransactionModel.query.all()) == 0:
        transaction = TransactionModel(ticker=None, price=0, shares=0, date=0)
