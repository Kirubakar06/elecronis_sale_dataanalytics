# Tamil Nadu Electronics Sales Analytics

This project reads `TN_Electronics_Sales_Analytics.csv`, cleans and validates
the sales records, creates sales summaries and charts, and loads the cleaned
records into MySQL.

## Setup on Windows PowerShell

1. Install the project dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Set the MySQL password for the current PowerShell session. Do not put the
   password in a Python file:

   ```powershell
   $env:MYSQL_PASSWORD = "your-mysql-password"
   ```

   Optional settings are `MYSQL_HOST` (default `localhost`), `MYSQL_PORT`
   (default `3306`), `MYSQL_USER` (default `root`), and `MYSQL_DATABASE`
   (default `tn_electronics_sales_analytics`).

3. Run the pipeline:

   ```powershell
   python main.py
   ```

The MySQL user must be allowed to create the configured database. The pipeline
creates it if it does not exist and replaces the
`tn_electronics_sales_analytics` table on each run. Cleaned data, CSV reports,
an Excel file, and charts are written to `reports`.

The CSV uses Indian rupee values and `DD-MM-YYYY` dates. Blank lines are
ignored; malformed records and conflicting order IDs stop the pipeline with
an explicit error.
