# List of 46 MWPs (Example structure, replace with the actual MWPs)
mwps = [
    {"Application", "ByLocation", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByDiscount", "Catalog", "Discount", "Filtered", "Payment"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Discount", "Filtered", "Payment"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Discount", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Call", "Catalog", "Discount", "Filtered", "Notification", "Payment"},
    {"Application", "ByDiscount", "Call", "Catalog", "CreditCard", "Discount", "Filtered", "Notification", "Payment"},
    {"Application", "ByDiscount", "Call", "Catalog", "CreditCard", "Filtered", "Notification", "Payment"},
    {"Application", "ByWeather", "Call", "Catalog", "CreditCard", "Filtered", "Notification", "Payment"},
    {"Application", "ByWeather", "Call", "Catalog", "CreditCard", "Discount", "Filtered", "Notification", "Payment"},
    {"Application", "ByWeather", "Call", "Catalog", "Discount", "Filtered", "Notification", "Payment"},
    {"Application", "ByLocation", "Catalog", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByLocation", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByLocation", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Filtered", "Payment"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Filtered", "Payment"},
    {"Application", "ByDiscount", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByWeather", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByWeather", "Catalog", "Discount", "Filtered", "Payment"},
    {"Application", "ByWeather", "Catalog", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByWeather", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "Discount", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByWeather", "Catalog", "Discount", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Discount", "Filtered", "Notification", "Payment", "SMS"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Discount", "Filtered", "Location", "Payment", "WiFi"},
    {"Application", "ByDiscount", "Catalog", "CreditCard", "Discount", "Filtered", "GPS", "Location", "Payment"},
    {"Application", "ByWeather", "Catalog", "CreditCard", "Discount", "Filtered", "Payment"}
]


# Step 1: Normalize MWPs by converting to sets
normalized_mwps = [frozenset(mwp) for mwp in mwps]

# Step 2: Find duplicates
duplicates = {}
for i, mwp in enumerate(normalized_mwps):
    if normalized_mwps.count(mwp) > 1:
        duplicates[mwp] = [j + 1 for j, m in enumerate(normalized_mwps) if m == mwp]

# Step 3: Display duplicates
print("Duplicate MWPs:")
for mwp, indices in duplicates.items():
    print(f"MWP {indices} are duplicates: {set(mwp)}")


# Print each MWP with its length
print("Lengths")
for i, mwp in enumerate(mwps, start=1):
    print(f"MWP {i}: {mwp} = {len(mwp)}")