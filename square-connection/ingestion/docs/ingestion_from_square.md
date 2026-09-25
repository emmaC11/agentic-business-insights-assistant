# Fetching sales data from Square

# 1 - Add Square production tokens
Access to Square APIs requires a JWT token, these tokens can be retrieved from https://developer.squareup.com/apps

![Select app name in applications tab ](image_1.png)
![Copy prod token](image_2.png)

Location ID is also is required and can be copied from the locations tab:

![Copy Location ID](image_3.png)

# 2 - Update environment variables
Open .env file & paste production token and location ID

![Paste values here in placeholders](image_4.png)

# 3 - Trigger ingestion
Open a new powershell terminal and run the command:
```powershell
python -m ingestion.runner
```

A new parquet file named sales_weekly.parquet will be created

![sales_weekly.parquet created](image_5.png)