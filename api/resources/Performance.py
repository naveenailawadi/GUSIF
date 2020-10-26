from api import db
from api.resources import validate_admin_token, load_json
from api.models.Portfolio import TransactionModel, FundModel, SectorPortfolioModel, HoldingModel, copy_model
from flask_restful import Resource


# create a resource for creating a brand new fund to track
class FundResource(Resource):
    def post(self):
        data = load_json()

        # make a new fund on the data
        try:
            token = data['token']
            fund_data = data['fund']
        except KeyError:
            return {'message': 'must include token, fund'}, 422

        # validate the admin
        message, error_code = validate_admin_token(token)
        if message:
            return message, error_code

        # make a fund object and bind it to the transaction
        associated_transaction = TransactionModel.query.filter_by(
            transaction_id=fund_data['transaction_id']).first()
        new_fund = FundModel(
            transaction_id=associated_transaction.id, name=fund_data['name'])

        # add the portfolios
        for sector in fund_data['sectors']:
            # create a sector object
            new_sector = SectorPortfolioModel(name=sector['name'])

            # iterate over the holdings to add them to the sector portfolio
            for holding in sector['holdings']:
                new_holding = HoldingModel(
                    ticker=holding['ticker'], shares=holding['shares'])

                # add the holding to the sector portfolio
                new_sector.append(new_holding)

            # add the portfolio to the fund
            new_fund.append(new_sector)

        db.session.add(new_fund)
        db.session.commit()

        # return that the upload was successful
        return {'status': 'success'}, 201


# create a resource for buying/selling a position
class TransactionResource(Resource):
    def post(self):
        data = load_json()

        # make a new fund on the data
        try:
            token = data['token']
            sector_name = data['sector_name']
            price = data['price']
            shares = data['shares']
            ticker = data['ticker']
        except KeyError:
            return {'message': 'must include token, sector, price, shares, ticker'}, 422

        # validate the admin
        message, error_code = validate_admin_token(token)
        if message:
            return message, error_code

        # get the most recent transaction
        recent_transaction = TransactionModel.query.order_by(
            TransactionModel.date).desc().first()

        # make a new transaction
        transaction = TransactionModel(
            ticker=ticker, price=price, shares=shares)

        # get the fund
        old_fund = recent_transaction.fund

        # make the new fund
        new_fund = copy_model(old_fund)

        # get the sector in the new fund to update
        sector_portfolio = new_fund.sector_portfolios.query.filter_by(
            name=sector_name).first()

        if not sector_portfolio:
            return {'message': f"No sector associated with name: {sector_name} in fund {old_fund.name} last updated on {recent_transaction.date}"}

        # check if there is a holding --> either add or subtract shares
        holding = sector_portfolio.query.filter_by(ticker=ticker).first()
        if holding:
            # take a variety of actions
            if int(holding.shares) == int(-1 * shares):
                sector_portfolio.remove(holding)
            else:
                holding.shares += shares
        else:
            # add the holding
            new_holding = HoldingModel(
                transaction_id=transaction.id, ticker=ticker, shares=shares)
            sector_portfolio.append(new_holding)

        # add the fund
        transaction.append(new_fund)
        db.session.add(transaction)

        db.session.commit()

        return {'status': 'success'}, 201


'''
Example for making a new fund
{
    "name": "GUSIF2020",
    "transaction_id": 0,
    "timestamp": 0,
    "sectors": [
        {
            "name": "INR",
            "holdings": [
                {
                    "ticker": "LUV",
                    "shares": 100
                }
            ]
        }
    ]
}

NOTES
- transaction_id binds the fund data to a particular place in time
'''
