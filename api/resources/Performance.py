from api import db
from api.resources import validate_admin_token, load_json
from api.models import copy_model, object_as_dict
from api.models.Portfolio import TransactionModel, FundModel, SectorPortfolioModel, HoldingModel
from flask_restful import Resource


# create a resource for creating a brand new fund to track
class FundResource(Resource):
    # make a function to get the current fund
    def get(self):
        fund = TransactionModel.query.order_by(
            TransactionModel.date.desc()).first().fund

        # get the fund into a dict
        fund_dict = fund.as_dict()

        return {'status': 'success', 'fund': fund_dict}

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
            id=fund_data['transaction_id']).first()
        new_fund = FundModel(
            transaction_id=associated_transaction.id, name=fund_data['name'])

        # add the portfolios
        for sector in fund_data['sectors']:
            # create a sector object
            new_sector = SectorPortfolioModel(
                name=sector['name'], cap_adj=sector['cap_adj'])

            # iterate over the holdings to add them to the sector portfolio
            for holding in sector['holdings']:
                new_holding = HoldingModel(
                    ticker=holding['ticker'], shares=holding['shares'])

                # add the holding to the sector portfolio
                new_sector.holdings.append(new_holding)

            # add the portfolio to the fund
            new_fund.sector_portfolios.append(new_sector)

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
            TransactionModel.date.desc()).first()
        og_portfolios = [
            portfolio for portfolio in TransactionModel.query.order_by(
                TransactionModel.date.desc()).first().fund.sector_portfolios]

        # make a new transaction
        transaction = TransactionModel(
            ticker=ticker, price=price, shares=shares)

        # get the fund
        old_fund = recent_transaction.fund

        # make the new fund
        new_fund = copy_model(old_fund)

        # add the old portfolios
        for portfolio in og_portfolios:
            new_fund.sector_portfolios.append(portfolio)

        # get the sector in the new fund to update
        old_sector_portfolio = new_fund.sector_portfolios.filter_by(
            name=sector_name).first()

        if not old_sector_portfolio:
            return {'message': f"No sector associated with name: {sector_name} in fund {old_fund.name} last updated on {recent_transaction.date}", 'attempted_new_fund': new_fund.as_dict()}, 404

        # make a new portfolio and switch it with the old one
        new_fund.sector_portfolios.remove(old_sector_portfolio)
        og_holdings = [
            holding for holding in old_sector_portfolio.holdings]
        sector_portfolio = copy_model(old_sector_portfolio)

        for holding in og_holdings:
            sector_portfolio.holdings.append(holding)

        # adjust the capital of the portfolio
        sector_portfolio.cap_adj -= transaction.total()

        # check if there is a holding --> either add or subtract shares
        old_holding = sector_portfolio.holdings.filter_by(
            ticker=ticker).first()
        if old_holding:
            print(
                f"Old holdings: {[object_as_dict(holding) for holding in sector_portfolio.holdings]}")
            sector_portfolio.holdings.remove(old_holding)
            print(
                f"New holdings: {[object_as_dict(holding) for holding in sector_portfolio.holdings]}")
            # make a new holding and replace the old one
            holding = copy_model(old_holding)

            # take a variety of actions
            if int(holding.shares) == int(-1 * shares):
                # leave the holding removed
                pass
            else:
                holding.shares += shares
                sector_portfolio.holdings.append(holding)
        else:
            # add the holding
            holding = HoldingModel(
                transaction_id=transaction.id, ticker=ticker, shares=shares)
            sector_portfolio.holdings.append(holding)

        # add the holding, portfolio, and fund
        new_fund.sector_portfolios.append(sector_portfolio)
        transaction.fund = new_fund
        db.session.add(transaction)

        db.session.commit()

        return {'status': 'success', 'new_portfolio': sector_portfolio.as_dict()}, 201


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
- will eventually need a way to add a new sector portfolio
    - also need a way to manually change the sector capital adjustments
'''
