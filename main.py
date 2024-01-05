import pandas as pd


class StockMarket:
    def __init__(self):
        self.orders_df = pd.DataFrame(columns=["Id", "Order", "Type", "Price", "Quantity"])

    def add_order(self, order_id, order_action, order_type, order_price, order_quantity):

        existing_order_index = self.orders_df[(self.orders_df["Id"] == order_id)].index

        if not existing_order_index.empty:
            existing_order = self.orders_df.loc[existing_order_index].iloc[0]

            if existing_order["Price"] != order_price:
                new_order_id = self.orders_df["Id"].max() + 1
                new_order = pd.DataFrame({"Id": [new_order_id],
                                          "Order": [order_action],
                                          "Type": [order_type],
                                          "Price": [order_price],
                                          "Quantity": [order_quantity]})
                self.orders_df = pd.concat([self.orders_df, new_order], ignore_index=True)
            elif order_type == "Remove" and existing_order["Quantity"] == order_quantity:
                self.orders_df = self.orders_df.drop(existing_order_index).reset_index(drop=True)
                print(f"Order removed: {order_id}")
            elif order_type == "Remove" and existing_order["Quantity"] > order_quantity:
                self.orders_df.loc[existing_order_index, "Quantity"] -= order_quantity
                print(f"Order partially removed: {order_id}")
        else:
            new_order = pd.DataFrame({"Id": [order_id],
                                      "Order": [order_action],
                                      "Type": [order_type],
                                      "Price": [order_price],
                                      "Quantity": [order_quantity]})
            updated_df = pd.concat([self.orders_df, new_order], ignore_index=True)

            self.orders_df = updated_df

    def display_summary(self):
        buy_orders = self.orders_df[(self.orders_df["Order"] == "Buy") & (self.orders_df["Type"] != "Remove")]
        if not buy_orders.empty:
            max_buy_value = 0
            best_buy_index = None

            for index, order in buy_orders.iterrows():
                order_value = order["Price"] * order["Quantity"]
                if order_value > max_buy_value:
                    max_buy_value = order_value
                    best_buy_index = order["Id"]

            print(f"Best Buy Order: {best_buy_index}, Max Buying Value: {max_buy_value}")
        else:
            print("No Buy Orders")

        sell_orders = self.orders_df[(self.orders_df["Order"] == "Sell") & (self.orders_df["Type"] != "Remove")]
        if not sell_orders.empty:
            max_sell_value = 0
            best_sell_index = None

            for index, order in sell_orders.iterrows():
                order_value = order["Quantity"] * order["Price"]
                if order_value > max_sell_value:
                    max_sell_value = order_value
                    best_sell_index = order["Id"]

            print(f"Best Sell Order: {best_sell_index}, Max Selling Value: {max_sell_value}")
        else:
            print("No Sell Orders")

        print("All orders after operations:")
        print(self.orders_df)


stock_market = StockMarket()

stock_market.add_order(1, "Buy", "Add", 20.0, 100)
stock_market.add_order(2, "Sell", "Add", 25.0, 200)
stock_market.add_order(3, "Buy", "Add", 23.0, 50)
stock_market.add_order(4, "Buy", "Add", 23.0, 70)
stock_market.add_order(3, "Buy", "Remove", 23.0, 50)
stock_market.add_order(5, "Sell", "Add", 28.0, 100)

stock_market.display_summary()
