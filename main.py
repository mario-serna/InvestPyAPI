from logging import exception
import investpy
from flask import Flask
from flask_restful import Resource, Api, reqparse
from numpy import e

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('list', type=str, help='Stocks ID')
parser.add_argument('columns', type=str, help='Columns to get')
parser.add_argument('from_date', type=str, help='From date dd/MM/yyyy')
parser.add_argument('to_date', type=str, help='To date dd/MM/yyyy')


class Welcome(Resource):
    def get(self):
        return "Welcome to InvestPyAPI"


class StockList(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            print(args.list)
            if args.list != None:
                stocks = args.list.split(",")
                print(stocks)
                frames = []
                labels = []
                for stock in stocks:
                    try:
                        print(stock)
                        search_result = investpy.search_quotes(
                            text=stock, products=['stocks'], countries=['peru'], n_results=None)
                        print(search_result)
                        if search_result:
                            data = search_result[0].retrieve_historical_data(
                                from_date=args.from_date, to_date=args.to_date)
                            labels.append(stock)
                            frames.append(data.to_csv())
                    except Exception as e:
                        print(e)
                        pass
                frames.insert(0, ",".join(labels))
                return frames

            search_result = investpy.stocks.get_stocks(country="peru")
            return search_result.to_csv()
        except Exception as e:
            print(e)
            return ""


class Stock(Resource):
    def get(self, id):
        try:
            args = parser.parse_args()
            print(id)
            print(args.from_date)
            search_result = investpy.search_quotes(
                text=id, products=['stocks'], countries=['peru'], n_results=None)

            print(search_result)
            data = search_result[0].retrieve_historical_data(
                from_date=args.from_date, to_date=args.to_date)

            if args.columns:
                data = data.loc[:, data.columns.isin(args.columns.split(","))]
            return data.to_csv()
        except Exception as e:
            print(e)
            return ""


api.add_resource(Welcome, '/')
api.add_resource(StockList, '/stocks')
api.add_resource(Stock, '/stocks/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)
