
from pathlib import Path

import pandas as pd


def generate_analytics(data: pd.DataFrame, output_dir: Path) -> dict[str, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)

    sales_by_district = (
        data.groupby("District", as_index=False)["Total_Amount"]
        .sum()
        .sort_values("Total_Amount", ascending=False)
    )
    sales_by_category = (
        data.groupby("Category", as_index=False)["Total_Amount"]
        .sum()
        .sort_values("Total_Amount", ascending=False)
    )
    top_products = (
        data.groupby(["Product_ID", "Product_Name"], as_index=False)
        .agg(
            Units_Sold=("Quantity", "sum"),
            Orders=("Order_ID", "nunique"),
            Revenue=("Total_Amount", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )
    monthly_sales = (
        data.assign(Month=data["Order_Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)["Total_Amount"]
        .sum()
        .sort_values("Month")
    )

    reports = {
        "sales_by_district": sales_by_district,
        "sales_by_category": sales_by_category,
        "top_products": top_products,
        "monthly_sales": monthly_sales,
    }
    for name, report in reports.items():
        report.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8-sig")

    total_revenue = data["Total_Amount"].sum()
    average_order_value = data["Total_Amount"].mean()
    print(f"Orders: {data['Order_ID'].nunique()}")
    print(f"Total sales: INR {total_revenue:,.2f}")
    print(f"Average order value: INR {average_order_value:,.2f}")
    print("\nTop 5 products by revenue:")
    print(top_products.head(5).to_string(index=False))

    return reports
