import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Load the dataset (update the file path as needed)
game_sales_df = pd.read_csv('video_games_sales.csv')

# Convert User_Score to numeric
game_sales_df['User_Score'] = pd.to_numeric(game_sales_df['User_Score'], errors='coerce')

# Data Preparation

# Top 10 highest-selling games globally
top_10_global_sales = game_sales_df[['Name', 'Global_Sales']].sort_values(by='Global_Sales', ascending=False).head(10)

# Sales by platform
sales_by_platform = game_sales_df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)

# Sales trends over time
sales_trend_yearly = game_sales_df.groupby('Year_of_Release').agg({
    'Global_Sales': 'sum',
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum'
}).reset_index()

# Initialize the Dash app
app = dash.Dash(__name__)

# Visualizations

# Bar chart: Top 10 games by global sales
top_10_bar_chart = px.bar(top_10_global_sales, x='Name', y='Global_Sales',
                           title='Top 10 Highest-Selling Games Globally')

# Pie chart: Sales by platform
platform_pie_chart = px.pie(values=sales_by_platform, names=sales_by_platform.index,
                             title='Sales by Platform')

# Line chart: Global sales trends over time
sales_trend_line_chart = px.line(sales_trend_yearly, x='Year_of_Release', y='Global_Sales',
                                  title='Global Sales Trends Over Time')

# Dashboard Layout
app.layout = html.Div(children=[
    html.H1(children='Video Game Sales Dashboard'),

    # Top 10 games bar chart
    dcc.Graph(id='top-10-bar-chart', figure=top_10_bar_chart),

    # Sales by platform pie chart
    dcc.Graph(id='platform-pie-chart', figure=platform_pie_chart),

    # Sales trend over time line chart
    dcc.Graph(id='sales-trend-line-chart', figure=sales_trend_line_chart),

    # Add a dropdown for filtering by genre
    html.H2(children='Filter by Genre'),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in game_sales_df['Genre'].dropna().unique()],
        value=game_sales_df['Genre'].dropna().unique()[0],  # Default to the first genre
        clearable=False,
        style={'width': '50%', 'margin': '0 auto'}
    ),

    # Top 5 games in selected genre
    dcc.Graph(id='top-5-genre-chart'),

    # Search for individual game performance
    html.H2(children='Search for Individual Game Performance'),

    # Centered and larger search input
    html.Div([
        dcc.Input(id='game-search-input', type='text', placeholder='Enter game name...',
                  style={'width': '50%', 'padding': '10px', 'fontSize': '18px', 'borderRadius': '8px',
                         'border': 'px solid #ddd'}),
    ], style={'textAlign': 'center', 'padding': '20px'}),

    html.Div(id='game-performance-output')
])

# Callback function to update top 5 games in the selected genre
@app.callback(
    Output('top-5-genre-chart', 'figure'),
    [Input('genre-dropdown', 'value')]
)
def update_top_5_genre_chart(selected_genre):
    filtered_df = game_sales_df[game_sales_df['Genre'] == selected_genre]
    top_5_games = filtered_df[['Name', 'Global_Sales']].sort_values(by='Global_Sales', ascending=False).head(5)
    return px.bar(top_5_games, x='Name', y='Global_Sales', title=f'Top 5 Games in {selected_genre} Genre')

# Callback function to update individual game performance based on search input
@app.callback(
    Output('game-performance-output', 'children'),
    [Input('game-search-input', 'value')]
)
def display_game_performance(game_name):
    if game_name:
        # Search for the game by name (case-insensitive)
        game_details = game_sales_df[game_sales_df['Name'].str.contains(game_name, case=False, na=False)]

        if not game_details.empty:
            # Extract relevant information for the game
            game_info = game_details.iloc[0]  # Taking the first match for simplicity

            # Bar chart for regional sales
            regional_sales = {
                'NA Sales': game_info['NA_Sales'],
                'EU Sales': game_info['EU_Sales'],
                'JP Sales': game_info['JP_Sales'],
                'Other Sales': game_info['Other_Sales']
            }
            regional_sales_chart = px.bar(x=list(regional_sales.keys()), y=list(regional_sales.values()),
                                           title='Regional Sales', labels={'x': 'Region', 'y': 'Sales (Million Units)'})

            # Gauge chart for Critic and User Scores
            score_gauge_chart = go.Figure()
            score_gauge_chart.add_trace(go.Indicator(
                mode="gauge+number",
                value=game_info['Critic_Score'],
                domain={'x': [0, 1], 'y': [0.75, 1]},
                title={'text': "Critic Score", 'font': {'size': 24}},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
            ))
            score_gauge_chart.add_trace(go.Indicator(
                mode="gauge+number",
                value=game_info['User_Score'] * 10,  # Scaling user score to match 0-100 scale
                domain={'x': [0, 1], 'y': [0.25, 0.5]},
                title={'text': "User Score", 'font': {'size': 24}},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkgreen"}}
            ))

            # Table for regional sales breakdown
            sales_table = html.Table([
                html.Thead(html.Tr([html.Th("Region"), html.Th("Sales (Million Units)")]),
                           style={'borderBottom': '2px solid black', 'textAlign': 'left'}),
                html.Tbody([
                    html.Tr([html.Td('NA Sales'), html.Td(game_info['NA_Sales'])]),
                    html.Tr([html.Td('EU Sales'), html.Td(game_info['EU_Sales'])]),
                    html.Tr([html.Td('JP Sales'), html.Td(game_info['JP_Sales'])]),
                    html.Tr([html.Td('Other Sales'), html.Td(game_info['Other_Sales'])])
                ])
            ], style={'width': '50%', 'margin': '0 auto', 'borderCollapse': 'collapse', 'border': '1px solid black'})

            # Card layout to display key information
            game_info_cards = html.Div([
                html.Div([
                    html.H4(f"Game: {game_info['Name']}"),
                    html.P(f"Platform: {game_info['Platform']}"),
                    html.P(f"Year of Release: {game_info['Year_of_Release']}"),
                    html.P(f"Genre: {game_info['Genre']}"),
                    html.P(f"Publisher: {game_info['Publisher']}"),
                    html.H4(f"Global Sales: {game_info['Global_Sales']} million units")
                ], style={'padding': '20px', 'border': '1px solid black', 'borderRadius': '10px', 'backgroundColor': '#f9f9f9'})
            ])

            # Display the game information, sales charts, scores, and table
            return html.Div([
                game_info_cards,
                dcc.Graph(figure=regional_sales_chart),
                dcc.Graph(figure=score_gauge_chart),
                html.H3("Regional Sales Breakdown"),
                sales_table
            ])
        else:
            return html.P("Game not found. Please check the name and try again.")
    return html.P("Please enter a game name to search.")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
