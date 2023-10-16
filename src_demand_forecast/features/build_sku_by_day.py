import pandas as pd

from src_demand_forecast.entities.train_pipeline_params import read_training_pipeline_params


def sku_demand_by_day(
    demand_orders: pd.DataFrame, demand_orders_status: pd.DataFrame
) -> pd.DataFrame:
    """
    Converts data from SQL to pandas DataFrame.
        1. Converts 'timestamp' into a datetime object and creates a new 'day' column with the date.
        2. Creates a cross combination of unique days and unique SKUs.
        3. Defines order IDs with delivery statuses (1, 3, 4, 5, 6).
        4. Calculates the total number of products sold for each pair (day, SKU).
        5. Combines sales data with SKU information.
        6. Returns the result with columns 'day', 'sku_id', 'sku', 'price', and 'qty' sorted by 'sku_id' and 'day'.

    Parameters:
        demand_orders (pd.DataFrame): The demand_orders DataFrame.
        demand_orders_status (pd.DataFrame): The demand_orders_status DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with the sales data.
    """
    # Convert timestamp to datetime
    demand_orders["timestamp"] = pd.to_datetime(demand_orders["timestamp"])
    demand_orders["day"] = demand_orders["timestamp"].dt.strftime("%Y-%m-%d")

    # Creating a combination of unique dates and SKUs
    unique_days = demand_orders["day"].drop_duplicates().reset_index(drop=True)
    unique_sku_ids = demand_orders["sku_id"].drop_duplicates().reset_index(drop=True)

    cross_join = pd.MultiIndex.from_product(
        [unique_days, unique_sku_ids], names=["day", "sku_id"]
    ).to_frame(index=False)
    # Identify orders with certain delivery statuses
    delivered_ids = demand_orders_status[
        demand_orders_status["status_id"].isin([1, 3, 4, 5, 6])
    ]["order_id"].drop_duplicates()
    # We determine the number of goods sold
    sales_qty = (
        demand_orders[demand_orders["order_id"].isin(delivered_ids)]
        .groupby(["day", "sku_id"])["qty"]
        .sum()
        .reset_index()
    )
    # Combine the data to get complete sales data
    full_sales = pd.merge(cross_join, sales_qty, on=["day", "sku_id"], how="left")
    full_sales["qty"].fillna(0, inplace=True)
    # Get information about the goods
    sku_info = demand_orders[["sku_id", "sku", "price"]].drop_duplicates()
    # Combine sales data with information about the goods
    result = pd.merge(full_sales, sku_info, on="sku_id", how="left").sort_values(
        by=["sku_id", "day"]
    )
    result = result[["day", "sku_id", "sku", "price", "qty"]]
    result["qty"] = result["qty"].astype(int)

    return result


def save_sku_demand_by_day(path: str, data: pd.DataFrame):
    data.to_csv(path, index=False, sep=",")


if __name__ == "__main__":
    params = read_training_pipeline_params("configs/train_config.yaml")
    demand_orders = pd.read_csv(params.input_demand_orders)
    demand_orders_status = pd.read_csv(params.input_demand_orders_status)
    sku_demand_day = sku_demand_by_day(demand_orders, demand_orders_status)
    save_sku_demand_by_day(params.output_sku_demand_day, sku_demand_day)
