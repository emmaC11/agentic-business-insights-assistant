import pandas as pd

# return specific item sales data across the full range in df
def get_item_sales(df: pd.DataFrame, item: str) -> str:

        earliest_date = df["week_start"].min()
        latest_date = df["week_start"].max()

        # check if item searched exists
        if item not in df["item"].nunique():
            return (f"item not found in sales history - {item}")

        item_rows = df[df["item"] == item]
        total = item_rows["quantity"].sum()
        weeks_sold = (item_rows["quantity"] > 0).sum()
        weeks_in_range = df["week_start"].nunique()

        if total == 0:
              return f"{item} sold nothing in range chosen"

        # idmax finds index label (row num) to find where max col occurs
        # rows loc uses idmax index labelto extract entire row with the max value
        best_week = item_rows.loc[item_rows["quantity"].idxmax()]

        # agent generate res from this
        return (
            f"'{item}' — {earliest_date} to {latest_date}\n"
            f"- Total sold: {total} units\n"
            f"- Sold in {weeks_sold} of {weeks_in_range} weeks\n"
            f"- Best week: {best_week['week_start'].date()} ({int(best_week['quantity'])} units)"
        )