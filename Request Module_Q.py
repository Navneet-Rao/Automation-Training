import requests
import sys

TOKEN          = input("Token       : ")
ALERT_TYPE     = input("Alert type  (critical / nosignal) : ")
FROM_TIMESTAMP = input("From        (e.g. 2026-06-17T04:10:00Z) : ")
TO_TIMESTAMP   = input("To          (e.g. 2026-06-17T04:20:00Z) : ")

API_URL = "https://ac-intelsat.hub.quvia.ai/neuron-api/visualization/api/network-summary/status-history/v3"

payload = {
    "flightStatuses":   {"include": ["active"], "exclude": []},
    "altitude":         {"include": ["gt25k", "gte10_lte25k"], "exclude": []},
    "enabledMetrics":   ["eqoemin.packet_loss", "eqoemin.web_qoe_score", "eqoemin.rtt_ms"],
    "includeFirstLast": False,
    "timeRange": {
        "fromTimestamp": FROM_TIMESTAMP,
        "toTimestamp":   TO_TIMESTAMP,
    },
}

if ALERT_TYPE == "nosignal":
    payload["site.custom_string_6"] = {"include": ["FALSE"], "exclude": []}

print("Fetching data from Quvia API ...")

headers  = {"Authorization": "Bearer " + TOKEN}
response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    sys.exit()

api_result = response.json()

status_data = api_result.get("status", {})

rows = []

for timestamp_string, counts in status_data.items():

    critical  = counts.get("critical", 0)
    no_signal = counts.get("noSignal", 0)
    warning   = counts.get("warning",  0)
    good      = counts.get("good",     0)
    total     = critical + no_signal + warning + good

    if ALERT_TYPE == "nosignal":
        affected = no_signal
    else:
        affected = critical

    if total > 0:
        pct = round(affected / total * 100, 1)
    else:
        pct = 0.0

    rows.append({
        "time":     timestamp_string,
        "critical": critical,
        "nosignal": no_signal,
        "warning":  warning,
        "good":     good,
        "affected": affected,
        "total":    total,
        "pct":      pct,
    })

if len(rows) == 0:
    print("No data found. Check your token or timestamps.")
else:

    peak_row = rows[0]
    for row in rows:
        if row["affected"] > peak_row["affected"]:
            peak_row = row

    if ALERT_TYPE == "nosignal":
        label = "No Signal"
    else:
        label = "Critical"

    print("")
    print("Peak —", label, "Alert")
    print("Time     :", peak_row["time"])
    print("Critical :", peak_row["critical"])
    print("No Signal:", peak_row["nosignal"])
    print("Warning  :", peak_row["warning"])
    print("Good     :", peak_row["good"])
    print("Affected :", peak_row["affected"])
    print("Total    :", peak_row["total"])
    print("Percent  :", str(peak_row["pct"]) + "%")
    print("")
