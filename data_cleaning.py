
import pandas as pd


REQUIRED_COLUMNS = (
    "Order_ID",
    "Order_Date",
    "District",
    "Branch",
    "Product_ID",
    "Product_Name",
    "Category",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Total_Amount",
    "Payment_Mode",
    "Customer_Type",
    "Sales_Executive",
)
TEXT_COLUMNS = (
    "Order_ID",
    "District",
    "Branch",
    "Product_ID",
    "Product_Name",
    "Category",
    "Payment_Mode",
    "Customer_Type",
    "Sales_Executive",
)
MONEY_COLUMNS = ("Unit_Price", "Discount", "Total_Amount")


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]

    order_id_column = next(
        (column for column in cleaned.columns if column.casefold() == "order id"),
        None,
    )
    if order_id_column is not None:
        cleaned = cleaned.rename(columns={order_id_column: "Order_ID"})

    if cleaned.columns.duplicated().any():
        raise ValueError("CSV contains duplicate column names.")

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(cleaned.columns))
    if missing_columns:
        raise ValueError(
            "CSV is missing required sales columns: " + ", ".join(missing_columns)
        )

    cleaned = cleaned.dropna(how="all").copy()
    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    missing_values = cleaned[list(REQUIRED_COLUMNS)].isna().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        details = ", ".join(
            f"{column}: {count}" for column, count in missing_values.items()
        )
        raise ValueError(f"Required sales values are missing ({details}).")

    cleaned["Order_Date"] = pd.to_datetime(
        cleaned["Order_Date"],
        format="%d-%m-%Y",
        errors="coerce",
    )
    if cleaned["Order_Date"].isna().any():
        raise ValueError("Order_Date contains values that are not in DD-MM-YYYY format.")

    quantity = pd.to_numeric(cleaned["Quantity"], errors="coerce")
    if quantity.isna().any() or (quantity % 1 != 0).any():
        raise ValueError("Quantity must contain whole numbers.")
    if (quantity <= 0).any():
        raise ValueError("Quantity must be greater than zero.")
    cleaned["Quantity"] = quantity.astype("int64")

    for column in MONEY_COLUMNS:
        raw_values = (
            cleaned[column]
            .astype("string")
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        values = pd.to_numeric(raw_values, errors="coerce")
        if values.isna().any():
            raise ValueError(f"{column} contains invalid currency values.")
        if (values < 0).any():
            raise ValueError(f"{column} cannot contain negative values.")
        cleaned[column] = values.astype("float64")

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    if cleaned["Order_ID"].duplicated().any():
        duplicate_ids = cleaned.loc[
            cleaned["Order_ID"].duplicated(keep=False), "Order_ID"
        ].unique()
        raise ValueError(
            "Conflicting rows share an Order_ID: " + ", ".join(duplicate_ids)
        )

    if cleaned.empty:
        raise ValueError("No valid sales records remain after cleaning.")
    return cleaned
