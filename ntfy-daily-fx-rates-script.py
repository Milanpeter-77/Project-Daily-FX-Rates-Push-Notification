# %% [markdown]
# # **Daily FX Rates – Push Notification**
# 
# This script sends daily foreign exchange rates as a push notification using ntfy.sh.
# 

# %%
import requests
import datetime

# Topic name (must match what your iPhone ntfy app is subscribed to)
topic = "daily-fx-rates"

# Path to the log file
log_file = f"ntfy-{topic}-log.txt"

# Get current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# %% [markdown]
# ## **Exchange Rates Request**
# 
# 1. **Requests exchange rates** (EUR, GBP, HUF) from the Open Exchange Rates API using a USD base.
#    - Web page: [**Open Exchange Rates**](https://openexchangerates.org/account)
# 2. **Logs** whether the API request succeeded or failed.
# 3. **Calculates cross-rates**:
# 
#    * EUR/HUF
#    * USD/HUF
#    * GBP/HUF
#    * EUR/USD
# 4. **Formats the results** into a summary message, but does not print or save it (used later as the content of the notification).
# 

# %%
# App ID
API_KEY = "9b9a3c99b74d4050bfd6508f454a0583"

# Currencies needed for conversion
symbols = ["EUR", "GBP", "HUF"]
url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}&symbols={','.join(symbols)}"
response = requests.get(url)
data = response.json()

# Log the result of the exchange rate requests
with open(log_file, "a") as log:
    if response.status_code == 200:
        log.write(f"[{timestamp}] Exchange rates downloaded successfully\n")
    else:
        log.write(f"[{timestamp}] Failed to download exchange rates. Status code: {response.status_code}\n")
        log.write(f"[{timestamp}] Response: {response.text}\n")

# Check for errors
if response.status_code != 200 or "rates" not in data:
    exit()

# Extract rates from USD base
rates = data["rates"]
usd_to_eur = rates["EUR"]
usd_to_gbp = rates["GBP"]
usd_to_huf = rates["HUF"]

# Compute cross rates
eur_to_huf = usd_to_huf / usd_to_eur
usd_to_huf = usd_to_huf
gbp_to_huf = usd_to_huf / usd_to_gbp
eur_to_usd = 1 / usd_to_eur

# Store results
message = (
    f"EUR/HUF: {eur_to_huf:.2f}\n"
    f"USD/HUF: {usd_to_huf:.2f}\n"
    f"GBP/HUF: {gbp_to_huf:.2f}\n"
    f"EUR/USD: {eur_to_usd:.4f}"
)

# %% [markdown]
# ## **Notification Request**
# 
# 1. **Defines the ntfy.sh endpoint** by combining the base URL with your custom topic name — this is where the notification will be sent.
#     - Web page: [**ntfy.sh**](https://docs.ntfy.sh)
# 
# 2. **Sets the message body** to be used as the content of the notification.
# 
# 3. **Prepares optional headers** to customize the notification:
# 
#    * Sets a title.
#    * Sets the priority level.
#    * Other headers like emoji tags, clickable URLs, or file attachments are listed but commented out for optional use.
# 
# 4. **Sends the push notification** by making an HTTP POST request to ntfy.sh, including the message and headers.
# 
# 5. **Logs** whether the API request succeeded or failed.
# 

# %%
# ntfy.sh endpoint with my topic
url = f"https://ntfy.sh/{topic}"

# Main message body
# On my iphone: only the first 4 lines are shown
# On my watch: only the first 2 rows are shown
message = message

# Optional headers to enhance the notification
headers = {
    # Push notification title
    "Title": "FX Market Update",
    # Priority: min, low, default, high, max
    "Priority": "default",
    # Emojis/icons in ntfy (short code list: https://docs.ntfy.sh/emojis/)
    #"Tags": "",
    # Opens this URL when the notification is tapped
    #"Click": "https://www.investing.com/currencies/",
    # Attach images or files via a public URL
    #"Attach": "https://example.com/chart.png",
    # Custom filename if attachment is used
    #"Filename": "chart.png"
}

# Send the POST request with the message and headers
response = requests.post(url, data=message.encode("utf-8"), headers=headers)

# Log the result of the notification request
with open(log_file, "a") as log:
    if response.status_code == 200:
        log.write(f"[{timestamp}] Notification sent successfully\n")
    else:
        log.write(f"[{timestamp}] Failed to send notification. Status code: {response.status_code}\n")
        log.write(f"[{timestamp}] Response: {response.text}\n")


