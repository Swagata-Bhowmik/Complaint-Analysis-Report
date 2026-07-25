# 📈 Ride-Hailing Demand Forecasting

> **One line:** Forecast ride-hailing demand by time and zone using real NYC TLC trip data,
> comparing classical, multivariate, modern, and deep-learning approaches — tied to a driver
> positioning business recommendation.

## The business problem
Ride-hailing platforms (Uber/Ola/Rapido-style) need to know how much demand to expect, when,
and where, so drivers can be positioned ahead of need — cutting rider wait time and driver idle
time.

## Data
**NYC TLC (Taxi & Limousine Commission) Trip Record Data** — official government source,
published monthly, current through ~2 months before today. Includes yellow/green taxis and
for-hire vehicles (Uber/Lyft-style). Source: nyc.gov/site/tlc/about/tlc-trip-record-data.page

> Chosen over the older 2014-2015 Kaggle "Uber Pickups" dataset because that data is now over a
> decade old — using it in a 2026 project would invite "why such old data?" questions. NYC TLC's
> official feed is authoritative, current, and still covers real Uber/ride-hailing trips.

## Status
🚧 Phase 1 — investigating the real data before building anything (per WORKING_METHOD.md).
