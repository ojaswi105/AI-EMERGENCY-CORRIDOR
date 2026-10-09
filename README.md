# AI Emergency Corridor

A demo system where an ambulance/fire truck picks the fastest route to a
hospital, and reroutes automatically when the path is flagged as busy.

Uses **OSRM** (Open Source Routing Machine) via its free public demo
server — no API key needed. Live traffic is not available for free, so
congestion is *simulated* (~35% chance a route is flagged busy on each
request, plus a manual "force reroute" button to demo it on command).
This is the natural place to plug in a real traffic API later.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## How to use

1. Click the map once to place the ambulance's start point.
2. Click again to place the hospital (destination).
3. Click "Get fastest route" — draws the route and shows distance/time.
4. Click "Simulate traffic jam (force reroute)" — forces the system to
   pick an alternate route and highlights it in red, to demonstrate the
   rerouting behaviour for your project demo.

## How it maps to the architecture

- **Ambulance app** → the map click (start point) simulates the GPS ping.
- **Route engine** → `get_routes()` in `app.py`, calls OSRM.
- **Traffic check** → `is_congested()` — replace this with a real traffic
  feed or a "report road blocked" feature for a stronger project.
- **Navigation** → the `/get-route` response drawn on the Leaflet map.
- **Arrival** → not modeled here, but you could add a "mark arrived"
  button that logs response time for your report.

## Ideas to extend it for a stronger submission

- Add a form to type addresses instead of only clicking the map
  (use OSRM's `/nearest` or Nominatim for geocoding).
- Log every route request (start, end, distance, time, rerouted or not)
  to a small SQLite database, then show stats/graphs — this gives you
  real "data" to present.
- Add multiple ambulances (multiple markers) and show which one is
  closest to a given emergency.
- Add a basic "traffic signal alert" simulation: when the ambulance is
  within X meters of a fixed point, print/log "signal cleared".
