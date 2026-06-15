import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

TOPICS = ["Welcome", "Discover", "Explore", "Learn"]

HEALTH_DATA = {'Category': ['Mental Health', 'Cardiovascular', 'Respiratory', 'Diabetes', 'Other'],
    'Cases': [35, 25, 20, 15, 5]}

BAR_DATA = pd.read_csv("birth_by_age_2024.csv")

LINE_DATA = pd.read_csv("Measels_cases_long.csv")


SCATTER_DATA = pd.read_csv("Health_med_age_area.csv")

HEALTH_CATEGORIES = sorted(SCATTER_DATA["General health (6 categories)"].unique())


EXPLORE_DATA = pd.read_csv("Correlation_data.csv")

EXPLORE_VARIABLES = ["Number of deaths", "Fertality rate", 'Gross disposable household income per head (£)', 'Average house price (£)']

#MAIN PAGE TABS
app.layout = dbc.Container(
    [
        dcc.Tabs(
            id="topic-tabs",
            value="Welcome",
            children=[dcc.Tab(label=topic, value=topic) for topic in TOPICS],
        ),
        html.Div(id="tab-content", className="mt-3"),
    ],
    fluid=True,
)

#TABS CALLBACKS (DISCOVER-GRAPHS, EXPLORE-CORRELATION GRAPH, LEARN?)
@app.callback(
        Output("tab-content", "children"), 
        Input("topic-tabs", "value"))
def render_tab_content(selected_topic):
 
#WELCOME PAGE
    if selected_topic == "Welcome":
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2("Welcome to the Open Data Dashboard", className="fw-bold mb-3 text-primary"),
                        html.P("This interactive website is designed to help you explore, understand, and analyze UK government data related to different topics. Select a tab above to begin.", className="text-muted fs-5 mb-5"),
                    ], className="text-center py-5")
                ], width=10, lg=8)
            ], className="justify-content-center"),

            dbc.Row([
                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.H4("Discover", className="card-title text-primary mb-3"),
                        html.P("View interactive graphs related to health, population, immigration, and more.", className="card-text text-muted")
                    ]), className="shadow-sm h-100 border-0 text-center")
                ], width=12, md=4, className="mb-3"),

                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.H4("Explore", className="card-title text-primary mb-3"),
                        html.P("Have fun with the data by plotting different variables against each other to find hidden correlations.", className="card-text text-muted")
                    ]), className="shadow-sm h-100 border-0 text-center")
                ], width=12, md=4, className="mb-3"),

                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.H4("Learn", className="card-title text-primary mb-3"),
                        html.P("Build your data literacy by learning how to read graphs, understand statistics, and spot misinformation.", className="card-text text-muted")
                    ]), className="shadow-sm h-100 border-0 text-center")
                ], width=12, md=4, className="mb-3"),
            ], className="g-4 mb-5")
        ])

    elif selected_topic == "Discover":
        return dbc.Card(
            dbc.CardBody([
                html.H3("Discover UK Government Datasets", className="mb-4 text-center"),
                
#BUTTON GROUP
                dbc.Row([
                    dbc.Col([
                        dbc.RadioItems(
                            id="discover-data-selector",
                            className="btn-group shadow-sm mb-4",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary px-4",
                            labelCheckedClassName="active fw-bold",
                            options=[
                                {"label": "Health", "value": "Health"},
                                {"label": "Population", "value": "Population"},
                                {"label": "Immigration", "value": "Immigration"},
                                {"label": "Scotland", "value": "Scotland"}
                            ],
                            value="Health", 
                        )
                    ], width=12, className="d-flex justify-content-center") 
                ]),
                
                html.Div(id="discover-content")
            ])
        )

    elif selected_topic == "Explore":
        return dbc.Card(
            dbc.CardBody([
                html.H3("Explore correlations", className="mb-3 text-center"),
                html.P([
                "Regional data showing the relationship between two selected variables for England and Wales.",
                html.Br(),
                "Each point represents a different area. Hover over points to see details."],
                className="card-text text-center text-muted mb-4"
                ),

                dbc.Row([
                    dbc.Col([
                        html.Label("X variable", className="mb-2"),
                        dcc.Dropdown(
                            id="explore-x-variable",
                            options=[{"label": v, "value": v} for v in EXPLORE_VARIABLES],
                            value="Fertality rate",
                            clearable=False,
                            className="shadow-sm"
                        )
                    ], width=3),

                    dbc.Col([
                        html.Label("Y variable", className="mb-2"),
                        dcc.Dropdown(
                            id="explore-y-variable",
                            options=[{"label": v, "value": v} for v in EXPLORE_VARIABLES],
                            value="Number of deaths",
                            clearable=False,
                            className="shadow-sm"
                        )
                    ], width=3),
                ], className="g-4 mb-4 justify-content-center"),

                html.Div(id="explore-content")
            ])
        )

    elif selected_topic == "Learn":
        return dbc.Card(
            dbc.CardBody([
                dbc.Row([
# THE SIDEBAR MENU
                    dbc.Col([
                        html.H6("LEARN MODULES", className="text-muted fw-bold mb-3"),
                        dbc.RadioItems(
                            id="learn-sidebar",
                            className="d-flex flex-column",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary text-start mb-2 w-100",
                            labelCheckedClassName="active btn-primary text-white fw-bold",
                            options=[
                                {"label": "Data Literacy", "value": "literacy"},
                                {"label": "Spotting Misinfo", "value": "misinfo"}, 
                                {"label": "External Sources", "value": "sources"},
                            ],
                            value="literacy", 
                        )
                    ], width=2, className="border-end pe-3"), 

#THE MAIN CONTENT AREA
                    dbc.Col([
                        html.Div(id="learn-sidebar-content")
                    ], width=10, className="ps-4")
                ], style={"minHeight": "60vh"}) 
            ])
        )
        
    else:
           return html.Div(f"No content found for {selected_topic}")

#DISCOVER DROPDOWN CALLBACK
@app.callback(
    Output("discover-content", "children"),
    Input("discover-data-selector", "value")
)
def update_discover_content(selected_data):

#HEALTH
    if selected_data == "Health":                         
        df_health = pd.DataFrame(HEALTH_DATA)
        df_bar = pd.DataFrame(BAR_DATA)
        df_line = LINE_DATA
        df_scatter = pd.DataFrame(SCATTER_DATA)

#BAR DATA FILTER
        eng_wales_df = df_bar[df_bar["Area of usual residence Name"] == "ENGLAND AND WALES"].copy()
        age_order = ["Under 20", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40 to 44","45 and over"]

        bar_fig = px.bar(
            eng_wales_df,
            x="Age of Mother at birth (years)",
            y="Number of live births",
            category_orders={"Age of Mother at birth (years)": age_order},
            title="Live births by age of mother: England and Wales")
        
#LINE DATA FILTER
        age_labels = sorted(df_line["Age"].unique())
        default_selected = ["Under 1", "1 to 4", "5 to 9"]        
        default_df = df_line[df_line["Age"].isin(default_selected)]


        line_fig = px.line(
            default_df,
            x="Year",
            y="Cases",
            color="Age",
            markers=True,
            title="Measels cases over the years"
            )
        line_fig.update_xaxes(dtick=1)


#SIDE BAR DATA FILTER
        death_df = pd.read_csv("leading_causes_mortality.csv")
        death_df["Leading cause"] = death_df["Leading cause"].str.replace('"', '', regex=False).str.strip()
        death_df["Year"] = death_df["Year"].astype(int)
        death_df["Deaths"] = pd.to_numeric(death_df["Deaths"], errors="coerce")

        max_deaths = death_df["Deaths"].max()

        bar_race_fig = px.bar(
            death_df.sort_values(["Year", "Deaths"]),
            x="Deaths",
            y="Leading cause",
            orientation="h",
            animation_frame="Year",
            animation_group="Leading cause",
            range_x=[0, max_deaths * 1.1],
            title="Leading causes of death over time",
            template="plotly_white"
        )

        bar_race_fig.update_layout(
            height=350,
            xaxis_title="Deaths",
            yaxis_title="Leading cause",
            showlegend=False
        )

        bar_race_fig.update_traces(marker_color="#302a9d")

#SCATTERPLOT
        scatter_fig = px.scatter(
            df_scatter,
            x="Median age",
            y="Percent of all health responses",
            title="Wellness score by age",
            hover_data={
            "Area name": True,
            "Area code": False,
            "Median age": True,
            "Percent of all health responses": ':.1f',
            "Observation": False,
            "total_responses": False,
            "General health (6 categories)": False
        },)

        return html.Div([
            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Confirmed cases of measles by age group: 2012 to 2024", className="card-title"),
                            html.P(
                                "Select one or more age groups to display on the line chart.",
                                className="card-text"
                            ),
#LINE GRAPH CHECKLIST
                            dcc.Checklist(
                                id="age-checklist",
                                options=[{"label": age, "value": age} for age in age_labels],
                                value=default_selected,
                                inline=True,
                                labelStyle={"marginRight": "15px", "fontSize": "12px"}
                            ),
#LINE GRAPH
                            dcc.Graph(
                                id="cases-line-chart",
                                figure=line_fig,
                                style={"height": "350px"}
                            )
                        
                        ]),
                        dbc.CardFooter(
                            html.Small(html.A("Data available at UK.gov", href="https://www.gov.uk/government/publications/measles-historic-confirmed-cases-notifications-and-deaths/measles-historic-confirmed-cases-notifications-and-deaths", target="_blank", className="text-decoration-none")),
                            className="text-center"
                    )
                    ], className="h-100 mb-3")

                ], width=6),
                    
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Leading causes of death over time", className="card-title"),
                                html.P("Animated horizontal bar chart showing how deaths change by leading cause across years.",
                                className="card-text"
                                ),
#SIDE BAR ANIMATED BAR CHART                                
                            dcc.Graph(figure=bar_race_fig, style={"height": "350px"})
                        ]),
                        dbc.CardFooter(
                            html.Small(html.A("Data available at ONS", href="https://www.ons.gov.uk/releases/leadingcausesofdeathuk#data", target="_blank", className="text-decoration-none")),
                            className="text-center")   
                            
                    ],className="h-100 mb-3")
                ], width=6)      
            ], className="g-3"),
                

            dbc.Row([

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Births by age of mother", className="card-title"),
                            html.P( "Graph shows number of live births by mother's age.",
                                className="card-text"),

                            dcc.Graph(figure=bar_fig, style={"height": "350px"}) 
#BAR CHART                            
                        ]),
                     
                        dbc.CardFooter(
                            html.Small(html.A("Data available at ONS", href="https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/birthsinenglandandwalesbirthregistrations", target="_blank", className="text-decoration-none")),
                            className="text-center"),
                        ],
                    className="h-100 mb-3")
                ], width=6),


                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Reported general health and median age by area (England and Wales)", className="text-center card-title"),
                            html.P("Select a health category to see a realtionship between median age and percentage of people in the area that report that health status.",
                            className="card-text"),

                            dcc.Dropdown(
                                id="health-category-dropdown",
                                options=[{"label": c, "value": c} for c in HEALTH_CATEGORIES],
                                value="Good health",
                                clearable=False,
                                searchable=False,
                                className="mb-3"
                                ),
#SCATTERPLOT
                            dcc.Graph(
                                id="health-scatterplot",
                                style={"height": "350px"})
                            ]),

                        dbc.CardFooter(
                            html.Small([html.A("Health data available at ONS", href="https://www.ons.gov.uk/datasets/TS037/editions/2021/versions/3", target="_blank", className="m-3 text-decoration-none"),(html.A("Median age data available at ONS", href="https://www.ons.gov.uk/explore-local-statistics/indicators/median-age", target="_blank", className="m-3 text-decoration-none"))]),
                            className="text-center"),
                        
                        ],
                     
                    className="h-100 mb-3")
                ], width=6),
            ], className="g-3")
        ])

    else:
        return html.Div([
            html.H3(f"{selected_data} Data"),
            html.P(f"Charts for {selected_data} will appear here")
        ])


#LINE GRAPH CHECKLIST CALLBACK

@app.callback(
    Output("cases-line-chart", "figure"),
    Input("age-checklist", "value")
)
def update_line_chart(selected_ages):
    if not selected_ages:
        return px.line(title="No age groups selected")

    
    df_line = pd.read_csv("Measels_cases_long.csv")
    filtered = df_line[df_line["Age"].isin(selected_ages)]

    fig = px.line(
        filtered,
        x="Year",
        y="Cases",
        color="Age",
        markers=True,
        title="Measels cases over the years"
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(range=[0,800])
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Cases",
        template="plotly_white"
    )

    return fig


#HEALTH SCATTERPLOT
@app.callback(
    Output("health-scatterplot", "figure"),
    Input("health-category-dropdown", "value")
)
def update_health_scatter(selected_category):
    filtered = SCATTER_DATA[
        SCATTER_DATA["General health (6 categories)"] == selected_category
    ]

    fig = px.scatter(
        filtered,
        x="Median age",
        y="Percent of all health responses",
        hover_data={
            "Area name": True,
            "Area code": False,
            "Median age": True,
            "Percent of all health responses": ':.1f',
            "Observation": False,
            "total_responses": False,
            "General health (6 categories)": False
        },
        title=f"{selected_category} by median age"
    )

    fig.update_traces(
        marker=dict(size=12, color="#302a9d"),
        textposition="top center"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Median age",
        yaxis_title="Percentage of people reporting this health status",
        height=350,
        margin=dict(l=40, r=20, t=60, b=40)
    )

    return fig


#EXPLORE TAB CORRELATION PLOT CALLBACK   
@app.callback(
    Output("explore-content", "children"),
    Input("explore-x-variable", "value"),
    Input("explore-y-variable", "value")
)
def update_explore_content(x_var, y_var):
    fig = px.scatter(
        EXPLORE_DATA,
        x=x_var,
        y=y_var,
        hover_data=["Area name",y_var,x_var],
        title=f"{y_var} vs {x_var}",
        template="plotly_white"
    )

    fig.update_traces(marker=dict(size=12, color="#302a9d", opacity=0.7))
    fig.update_layout(height=500)

    return dbc.Card([
        dbc.CardBody([
            html.H4("Correlation scatterplot", className="card-title text-center"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig)
                ], width=10, lg=8) 
            ], className="justify-content-center")
        ]),
        
    
        dbc.CardFooter(
            html.Small(html.A("Data available at ONS", href="https://www.ons.gov.uk/explore-local-statistics/indicators", target="_blank", className="text-decoration-none")),
            className="text-center"
        )
    ], className="shadow-sm border-0 mt-3")

#LEARN SIDEBAR NAVIGATION CALLBACK
@app.callback(
    Output("learn-sidebar-content", "children"),
    Input("learn-sidebar", "value")
)
def render_sidebar_content(selection):
    
#DATA LITERACY 
    if selection == "literacy":
        return html.Div([
            html.Div([
                dbc.RadioItems(
                    id="stats-toggle-switch",
                    className="btn-group shadow-sm",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary px-4",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "How to Read Graphs", "value": "graphs"},
                        {"label": "Basic Math & Methods", "value": "methods"},
                    ],
                    value="graphs",
                )
            ], className="d-flex justify-content-center mb-5"), 
            html.Div(id="stats-toggle-content")
        ])

#SPOTTING MISINFORMATION
    elif selection == "misinfo":
        return html.Div([
            html.H4("Spotting Data Misinformation", className="mb-4"),
            html.P("Graphs and statistics can be easily manipulated to tell a specific story. Here are the most common 'Data Traps' to watch out for in the news, on social media, and in business reports:", className="text-muted mb-4"),

            html.Div([
                html.H5("The Truncated Y-Axis", className="text-danger"),
                html.P([html.Strong("The Trick: "), "A bar chart or line graph starts the vertical axis at a number higher than zero (e.g., starting at 50 instead of 0)."]),
                html.P([html.Strong("The Reality: "), "This artificially magnifies tiny differences. A 2% difference between two bars can be made to look like a massive 200% difference, tricking the eye into seeing a huge gap where none exists."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Cherry-Picked Timeframes", className="text-danger"),
                html.P([html.Strong("The Trick: "), "Showing a line graph that only covers a very specific window of time (e.g., isolating a single bad week in the stock market)."]),
                html.P([html.Strong("The Reality: "), "By zooming in too close, normal fluctuations look like permanent crashes or massive spikes. Always ask: ", html.Em("What does this graph look like if we zoom out to 5 or 10 years?")])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Relative vs. Absolute Percentages", className="text-danger"),
                html.P([html.Strong("The Trick: "), "A headline screams: 'New Study Shows 100% Increase in Disease X!'"]),
                html.P([html.Strong("The Reality: "), "This relies on 'Relative' percentages. If only 1 in a million people get a disease, and it rises to 2 in a million, that is technically a 100% increase. But the 'Absolute' risk only increased by 0.0001%. It's a classic fear-mongering tactic."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("nbalanced Sample Sizes", className="text-danger"),
                html.P([html.Strong("The Trick: "), "Using statistics that sound definitive, like '80% of Doctors Recommend...'"]),
                html.P([html.Strong("The Reality: "), "The statistic is meaningless without knowing the sample size and selection process. If they only asked 5 doctors who already work for the company, that '80%' means nothing to the general public."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Implied Causation", className="text-danger"),
                html.P([html.Strong("The Trick: "), "Showing a scatterplot where two lines follow the exact same path to imply one caused the other."]),
                html.P([html.Strong("The Reality: "), "Correlation does not equal causation. Ice cream sales and sunburn rates both peak in July, but eating ice cream does not cause sunburn. Always look for the hidden third variable (in this case, hot summer weather)."])
            ], className="mb-4")
        ])

#EXTERNAL SOURCES
    elif selection == "sources":
        return html.Div([
            html.H4("Further Reading", className="mb-4"),
            html.Ul([
                html.Li(html.A("The truth behind the numbers: spotting statistical misuse | Webinar", href="https://www.youtube.com/watch?v=lmJkini0ESQ", target="_blank", className="text-decoration-none")),
                html.Li(html.A("Misinformed by Visualization: What Do We Learn From Misinformative Visualizations?", href="https://arxiv.org/abs/2204.09548", target="_blank", className="text-decoration-none")),
                html.Li(html.A("The impact of misinformation on the COVID-19 pandemic", href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9114791/", target="_blank", className="text-decoration-none")),
                html.Li(html.A("Media manipulation and disinformation", href="https://datasociety.net/research/media-manipulation/", target="_blank", className="text-decoration-none")),
                html.Li(html.A("RESIST-2: Counter-Disinformation Toolkit", href="https://www.communications.gov.uk/wp-content/uploads/2021/11/RESIST-2-counter-disinformation-toolkit.pdf", target="_blank", className="text-decoration-none")),
            ], className="lh-lg")
        ])
        
    return html.Div("Content not found.")



# TOGGLE SWITCH CONTENT CALLBACK
@app.callback(
    Output("stats-toggle-content", "children"),
    Input("stats-toggle-switch", "value")
)
def render_toggle_content(toggle_view):
    if toggle_view == "graphs":
        
#EXAMPLE GRAPHS
        bar_fig = px.bar(x=["North", "South", "East", "West"], y=[120, 95, 140, 110], title="Categorical Comparison", template="plotly_white")
        bar_fig.update_traces(marker_color="#302a9d")

        line_fig = px.line(x=["Q1", "Q2", "Q3", "Q4"], y=[10, 15, 12, 22], markers=True, title="Time-Series Trends", template="plotly_white")
        line_fig.update_traces(line_color="#302a9d", marker=dict(size=10))

        pie_fig = px.pie(names=["Company A", "Company B", "Others"], values=[50, 30, 20], title="Proportional Breakdown", template="plotly_white", hole=0.3)

        scatter_fig = px.scatter(x=[1, 2, 3, 4, 5], y=[50, 110, 140, 210, 260], title="Variable Correlation", template="plotly_white")
        scatter_fig.update_traces(marker=dict(size=12, color="#302a9d"))

        hist_fig = px.histogram(x=[22, 24, 25, 25, 26, 27, 29, 31, 35, 41, 45, 50], nbins=5, title="Viewing Data Distribution", template="plotly_white")
        hist_fig.update_traces(marker_color="#302a9d")

        return html.Div([
            html.H4("Understanding Graphs", className="mb-4 text-center"),
            html.P("Overview of different types of graphs.", className="text-muted mb-4"),

 #BAR CHART CARD
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=bar_fig, style={"height": "300px"}), width=8),
                        dbc.Col([
                            html.H5("Bar Charts"),
                            html.P("Purpose: To compare quantities across distinct, unrelated categories."),
                            html.Strong("How to read it:"), 
                            html.P("The length or height of the bar directly represents the value. They are excellent for quick, side-by-side comparisons."),
                            html.Strong("What to watch for:"), 
                            html.P("Be cautious of bar charts that use a truncated y-axis, which can exaggerate small differences. Always check if the y-axis starts at zero to get an accurate sense of scale.")
                        ], width=4, className="d-flex flex-column justify-content-center")
                    ])
                ), className="mb-4 shadow-sm"),

#LINE GRAPH CARD
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=line_fig, style={"height": "300px"}), width=8),
                        dbc.Col([
                            html.H5("Line Graphs"),
                            html.P("Purpose: To display continuous data and illustrate trends over a specific period."),
                            html.Strong("How to read it:"), 
                            html.P("Follow the slope of the line. A steep upward slope indicates rapid growth, while a gentle slope indicates gradual change."),
                            html.Strong("What to watch for:"), 
                            html.P("Be cautious of graphs that only show a short time frame, which can exaggerate normal fluctuations. Always check the x-axis range to understand the full context.")
                        ], width=4, className="d-flex flex-column justify-content-center")
                    ])
                ), className="mb-4 shadow-sm"),

#PIE CHART CARD
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie_fig, style={"height": "300px"}), width=8),
                        dbc.Col([
                            html.H5("Pie Charts"),
                            html.P("Purpose: To show how a total amount (100%) is divided into proportional segments."),
                            html.Strong("How to read it:"), 
                            html.P("The arc length and angle of each slice represent its percentage of the whole."),
                            html.Strong("What to watch for:"), 
                            html.P("Percentages should add up to 100%. Slice sizes can be manipulated to look more dramatic than they are by using slice sizes not proportional to the data.")

                        ], width=4, className="d-flex flex-column justify-content-center")
                    ])
                ), className="mb-4 shadow-sm"),

# SCATTER PLOT CARD
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=scatter_fig, style={"height": "300px"}), width=8),
                        dbc.Col([
                            html.H5("Scatter Plots"),
                            html.P("Purpose: To reveal relationships or patterns between two different numerical variables."),
                            html.Strong("How to read it:"), 
                            html.P("If dots trend upward from left to right, the two variables increase together. Remember: Correlation does not imply causation."),
                            html.Strong("What to watch for:"), 
                            html.P("Outliers can skew the apparent relationship. Always look for clusters of points and consider if there might be a hidden third variable influencing both.")
                ], width=4, className="d-flex flex-column justify-content-center")
            ])), className="mb-4 shadow-sm"),

# HISTOGRAM CARD
            dbc.Card(
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=hist_fig, style={"height": "300px"}), width=8),
                        dbc.Col([
                            html.H5("Histograms"),
                            html.P("Purpose: To show how continuous data is distributed across distinct intervals (or 'bins')."),
                            html.Strong("How to read it:"), 
                            html.P("Histograms group data points into ranges to show where the majority of the data clusters."),
                            html.Strong("What to watch for:"), 
                            html.P("The choice of bin size can dramatically change the appearance of the distribution. Too few bins can oversimplify the data, while too many can make it look noisy. Always check the binning method used to understand the true shape of the data distribution.")
                        ], width=4, className="d-flex flex-column justify-content-center")
                    ])
                ), className="mb-4 shadow-sm")
        ])
        
    elif toggle_view == "methods":

        return html.Div([
            html.H4("Basic Statistics", className="mb-4"),
            html.P("Basic concepts used to summarize and describe datasets.", className="text-muted mb-4"),

            html.Div([
                html.H5("Mean (The Average)", className="text-primary"),
                html.P([html.Strong("Definition: "), "The sum of all values divided by the total number of values."]),
                html.P([html.Strong("Best used for: "), "Symmetrical data without extreme high or low numbers."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Median (The Middle)", className="text-primary"),
                html.P([html.Strong("Definition: "), "The exact middle value when all numbers are sorted from smallest to largest."]),
                html.P([html.Strong("Best used for: "), "Data that has extreme outliers (like income or house prices)."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Mode (The Most Common)", className="text-primary"),
                html.P([html.Strong("Definition: "), "The number or category that appears most frequently in a dataset."]),
                html.P([html.Strong("Best used for: "), "Categorical data, or figuring out the most popular option."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Range", className="text-primary"),
                html.P([html.Strong("Definition: "), "The difference between the highest and lowest values in a dataset."]),
                html.P([html.Strong("Best used for: "), "Getting a quick, simple understanding of how widely spread out the data is."])
            ], className="mb-4 border-bottom pb-3"),

            html.Div([
                html.H5("Standard Deviation", className="text-primary"),
                html.P([html.Strong("Definition: "), "A measure of how clustered or scattered the data is around the mean."]),
                html.P([html.Strong("Best used for: "), "Understanding consistency and risk. High standard deviation means the numbers are spread out over a wide range."])
            ], className="mb-4")
        ])

if __name__ == "__main__":
    app.run(debug=True)