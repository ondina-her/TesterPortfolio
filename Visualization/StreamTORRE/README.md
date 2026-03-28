# Project Title
Rotating Tower Visualization with Streamlit

## Description
A simple interactive web app built with Streamlit, Matplotlib, and NumPy that visualizes a rotating tower made of polygons.
Users can control the number of floors, rotation per floor, and polygon shape through interactive sliders and dropdowns.

## Features
Interactive controls in the sidebar:

Number of floors

Rotation per floor (degrees)

Polygon sides (triangle, square, pentagon, hexagon)

Real‑time 3D visualization of the tower.

Demonstrates reproducibility and testing of visualization workflows.

## Installation
Clone the repository and create a virtual environment:

git clone https://github.com/ondina-her/streamlit-tower.git
cd streamlit-tower
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt

## Usage
Run the app with:

bash6
streamlit run ST_Torre.py
Then open the browser at http://localhost:8501.

## Example Screenshots
(Add 1–2 screenshots of the app running with different settings.)

## Testing Notes
Example test cases:

Polygon sides = 3 → tower should be triangular.

Rotation per floor = 1 → tower should be straight.

Floors = 1 → only one polygon should appear.

Rotation per floor = 15 → tower should spiral strongly.

## Technologies Used
Python

Streamlit

Matplotlib

NumPy

## Author
Created by Ondina as part of a software testing and visualization portfolio project.

