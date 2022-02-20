from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd


# Read in data
df = pd.read_csv("cleaned_salaries.csv")

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.Iframe(
        id='boxplot',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcon-widget',
        value='Canada',  # REQUIRED to show the plot on the first page load
        options=[{'label': con, 'value': con} for con in df.Country.unique()])])

# Set up callbacks/backend
@app.callback(
    Output('boxplot', 'srcDoc'),
    Input('xcon-widget', 'value'))


def plot_altair(xcon):
    data = df[(df["Country"] == xcon)]
    chart = alt.Chart(data).mark_boxplot().encode(
        x=alt.X("Salary_USD:Q", 
                title="Salary in USD", 
                axis=alt.Axis(format='~s'),
                scale=alt.Scale(zero=False)),
        y=alt.Y('GenderSelect', title="Gender"),
        tooltip='count()',
        color=alt.Color('GenderSelect', title='Gender')
    ).properties(
        title='Boxplot by gender',
        projection={"type":'mercator'},
        width=400,
        height=180
    ).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
    
