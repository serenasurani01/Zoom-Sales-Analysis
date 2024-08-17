import pandas as pd
import numpy as np
import random
from datetime import timedelta

# Function to generate unique user ids
def generate_unique_user_id(existing_ids):
    while True:
        user_id = random.randint(100000000, 999999999)
        if user_id not in existing_ids:
            existing_ids.add(user_id)  # Add this new user_id to the existing set
            return user_id

# Define the target quarters and target revenues (in USD)
target_revenue = {
    '2020-01-31': 188.25 * 1e6 * 0.4,  # Converting from million to actual values
    '2020-04-30': 328.17 * 1e6 * 0.4,
    '2020-07-31': 663.52 * 1e6 * 0.4,
    '2020-10-31': 777.20 * 1e6 * 0.4,
    '2021-01-31': 882.49 * 1e6* 0.4,
    '2021-04-30': 956.24 * 1e6 * 0.4,
    '2021-07-31': 1.02 * 1e9 * 0.4,
    '2021-10-31': 1.05 * 1e9 * 0.4,
    '2022-01-31': 1.07 * 1e9 * 0.4,
    '2022-04-30': 1.07 * 1e9 * 0.4,
    '2022-07-31': 1.10 * 1e9 * 0.4,
    '2022-10-31': 1.10 * 1e9* 0.4
}

# Plan types without the 'basic' plan
plan_types = ['pro', 'enterprise', 'business']

# Set up regions (North America gets special handling)
regions = ['NA', 'EU', 'APAC', 'SA']

# Generate 25,000 rows for each quarter
existing_user_ids = set()  # Store all user IDs to ensure uniqueness
all_data = []  # To store all rows

for quarter, revenue_goal in target_revenue.items():
    start_date = pd.to_datetime(quarter) - pd.DateOffset(months=3)
    end_date = pd.to_datetime(quarter)
    
    total_revenue = 0
    rows_generated = 0
    
    while total_revenue < revenue_goal:
        user_id = generate_unique_user_id(existing_user_ids)

        # Adjust plan types based on observed trends
        if pd.to_datetime(quarter) <= pd.to_datetime('2020-07-31'):
            # Early 2020: Enterprise spikes, Business present but lower
            plan = random.choices(plan_types, weights=[0.2, 0.7, 0.1])[0]  # 70% Enterprise, 10% Business
        elif pd.to_datetime(quarter) >= pd.to_datetime('2021-10-31'):
            # Late 2021: Pro dominates, Business drops, Enterprise reduced
            plan = random.choices(plan_types, weights=[0.8, 0.15, 0.05])[0]  # 80% Pro, 15% Enterprise, 5% Business
        else:
            # Middle period: More balanced
            plan = random.choices(plan_types, weights=[0.5, 0.4, 0.1])[0]  # 50% Pro, 40% Enterprise, 10% Business

        # Adjust for yearly plan drop off towards the end of 2021
        if pd.to_datetime(quarter) >= pd.to_datetime('2021-10-31'):
            period = random.choices(['year', 'month'], weights=[0.5, 0.5])[0]  # 50/50 for year and month
        else:
            period = random.choices(['year', 'month'], weights=[0.9, 0.1])[0]  # 90% yearly plans until end of 2021
        
        # Adjust region based on the trends in the image
        if pd.to_datetime(quarter) <= pd.to_datetime('2020-04-30'):
            # North America makes up two-thirds of bookings during early 2020
            region = random.choices(regions, weights=[0.66, 0.1, 0.1, 0.14])[0]
        elif pd.to_datetime(quarter) >= pd.to_datetime('2021-07-31'):
            # Other regions pick up after 2021
            region = random.choices(regions, weights=[0.4, 0.25, 0.2, 0.15])[0]  # NA decreases, APAC and EU increase
        else:
            # More balanced distribution mid-2020 to mid-2021
            region = random.choice(regions)

        sub_start_ts = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        sub_end_ts = sub_start_ts + (timedelta(days=365) if period == 'year' else timedelta(days=30))

        # Adjust the price based on how much revenue is still needed
        max_price = (revenue_goal - total_revenue) / 500  # Spread revenue over approximately 500 users
        price = round(random.uniform(10, min(max_price, 10000)), 2)  # Cap the price at $1000 or the max_price needed
        price_usd = price * random.uniform(1.0, 1.1)  # Simulate conversion rate fluctuations

        # Ensure we don't exceed the target revenue
        if total_revenue + price_usd > revenue_goal:
            price_usd = revenue_goal - total_revenue

        currency = random.choice(['USD', 'EUR', 'CAD', 'GBP'])
        country_code = region

        all_data.append([user_id, plan, period, sub_start_ts, sub_end_ts, price, price_usd, currency, country_code])
        total_revenue += price_usd
        rows_generated += 1

        # Break if we've reached the revenue target
        if total_revenue >= revenue_goal:
            break

    print(f"Generated {rows_generated} rows for quarter {quarter} with total revenue of {total_revenue:.2f}")

# Create a DataFrame
columns = ['USER_ID', 'PLAN', 'PERIOD', 'SUB_START_TS', 'SUB_END_TS', 'PRICE', 'PRICE_USD', 'CURRENCY', 'COUNTRY_CODE']
df = pd.DataFrame(all_data, columns=columns)

# Save the data to CSV
df.to_csv("generated_subscription_data_with_trends_2020_2022.csv", index=False)

print("Data generation complete!")
