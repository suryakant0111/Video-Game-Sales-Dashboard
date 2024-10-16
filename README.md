# Video Game Sales Dashboard

This project is a web application that visualizes video game sales data using Dash, Plotly, and Pandas. The dashboard provides insights into the top-selling games, sales trends over time, and individual game performance based on user input.

## Features

- **Top 10 Highest-Selling Games**: A bar chart displaying the top 10 games based on global sales.
- **Sales by Platform**: A pie chart showing the distribution of sales by platform.
- **Sales Trends Over Time**: A line chart illustrating global sales trends over the years.
- **Filter by Genre**: A dropdown allowing users to filter and view the top 5 games in a selected genre.
- **Search Functionality**: A search bar to find individual game performance, including a detailed view of sales and scores.

## Prerequisites

Make sure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

## Installation

1. Clone this repository:
   ```bash
   https://github.com/suryakant0111/Video-Game-Sales-Dashboard/tree/main
Create a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Place the video_games_sales.csv dataset in the project directory.

Running the Application
To run the dashboard, execute the following command:

bash
Copy code
python app.py
Visit http://127.0.0.1:8050/ in your web browser to view the dashboard.

Contributing
Contributions are welcome! Please create a pull request or submit an issue.

License
This project is licensed under the MIT License. See the LICENSE file for details.

vbnet
Copy code

### Steps to Upload to GitHub
1. Create a new repository on GitHub.
2. Initialize your local repository if you haven't already:
   ```bash
   git init
Add the files:
bash
Copy code
git add app.py requirements.txt README.md video_games_sales.csv
Commit the changes:
bash
Copy code
git commit -m "Initial commit of video game sales dashboard"
Add the remote repository and push the changes:
bash
Copy code
git remote add origin https://github.com/suryakant0111/Video-Game-Sales-Dashboard/tree/main
git push -u origin master
