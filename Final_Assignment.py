!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

tesla = yf.Ticker("TSLA")

tesla_data = tesla.history (period="max")

tesla_data.reset_index(inplace=True)
tesla_data.head()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup (html_data)

tesla_revenue1 = pd.DataFrame(columns=["Date", "Revenue"])
read_html_pandas_data = pd.read_html(url)
read_html_pandas_data = pd.read_html(str(soup))
tesla_revenue1 = read_html_pandas_data[1]
tesla_revenue = tesla_revenue1.copy()
tesla_revenue.columns = ['Date','Revenue']
tesla_revenue.head()

tesla_revenue = tesla_revenue.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue != ""]

tesla_revenue.tail()

GameStop = yf.Ticker("GME")

gme_data = GameStop.history(period="max")

gme_data.reset_index(inplace=True)

url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data1 = requests.get(url1).text

soup1 = BeautifulSoup (html_data1)

gme_revenue1 = pd.DataFrame(columns=["Date", "Revenue"])
read_html_pandas_data = pd.read_html(url1)
read_html_pandas_data = pd.read_html(str(soup1))
gme_revenue1 = read_html_pandas_data[1]
gme_revenue = gme_revenue1.copy()
gme_revenue.columns = ['Date','Revenue']
gme_revenue.head()

gme_revenue.tail()

make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GameStop')
