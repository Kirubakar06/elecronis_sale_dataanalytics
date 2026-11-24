from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def create_charts(data: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_paths = []

    monthly_sales = (
        data.assign(Month=data["Order_Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Total_Amount"]
        .sum()
        .sort_index()
    )
    figure, axis = plt.subplots(figsize=(10, 5))
    monthly_sales.plot(kind="line", marker="o", ax=axis)
    axis.set(title="Monthly Sales", xlabel="Month", ylabel="Sales (INR)")
    axis.grid(axis="y", alpha=0.3)
    figure.tight_layout()
    monthly_path = output_dir / "monthly_sales.png"
    figure.savefig(monthly_path, dpi=150)
    plt.close(figure)
    chart_paths.append(monthly_path)

    category_sales = (
        data.groupby("Category")["Total_Amount"]
        .sum()
        .sort_values(ascending=True)
    )
    figure, axis = plt.subplots(figsize=(9, 5))
    category_sales.plot(kind="barh", ax=axis, color="steelblue")
    axis.set(title="Sales by Category", xlabel="Sales (INR)", ylabel="Category")
    axis.grid(axis="x", alpha=0.3)
    figure.tight_layout()
    category_path = output_dir / "sales_by_category.png"
    figure.savefig(category_path, dpi=150)
    plt.close(figure)
    chart_paths.append(category_path)

    return chart_paths
