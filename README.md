# SkyPather

SkyPather is a Python flight pathfinding program that finds routes between Florida aviation fixes and airports using weather-aware search algorithms. It uses real wind data from AviationWeather.gov and graph data from external point files to calculate and display routes on a map of Florida.

## Features

- Uses **Greedy Best-First Search**
- Uses **A\* Search**
- Incorporates **weather-aware heuristics**
- Imports fix and airport data from external files
- Fetches wind data using `weatherapi.py`
- Uses `points.py` for graph construction, plotting, and node lookup
- Displays the route visually on a Florida map using `matplotlib`

## How It Works

The program:

1. Calls functions from `weatherapi.py` to fetch wind data
2. Calls functions from `points.py` to:
   - read fixes from `fixes.txt`
   - read airports from `airports.txt`
   - connect nodes into a graph
   - find nodes by code
   - plot fixes and routes
3. Lets the user choose a start node and goal node
4. Runs either:
   - **Greedy Best-First Search**
   - **A\* Search**
5. Plots the resulting route on a map of Florida

## Files Required

Make sure these files are in the same folder as `SkyPather.py`:

- `SkyPather.py`
- `weatherapi.py`
- `points.py`
- `fixes.txt`
- `airports.txt`
- `florida.png`

## Dependencies

Install the required Python package:

```bash
pip install matplotlib
