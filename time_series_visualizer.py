import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("Python/Data Analysis/page view time series visualizer/fcc-forum-pageviews.csv")
df["date"]=pd.to_datetime(df["date"])
df.set_index("date")

# Clean data
df = df[(df["value"]<=df["value"].quantile(0.975))&
(df["value"]>=df["value"].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig,ax=plt.subplots(figsize=(12,12))
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    sns.lineplot(data=df)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    
    df_bar["Months"]=pd.DatetimeIndex(df['date']).month
    df_bar["Years"]=pd.DatetimeIndex(df['date']).year
    df_bar=df_bar.groupby(["Years", "Months"], as_index=False)["value"].mean()
    
    # Draw bar plot
    fig,ax=plt.subplots(figsize=(12,10))
    sns.barplot(data=df_bar,x="Years",y="value", hue="Months",palette="Set3")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    plt.legend(["January","February","March","April","May","June","July","August","September","October","November","December"],loc='upper left')
    

    # # # # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig,axes=plt.subplots(1,2,figsize=(12,6))

    # YEAR PLOT
    sns.boxplot(ax=axes[0],x="year", y="value", data=df_box)
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # MONTH PLOT
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(ax=axes[1],x="month", y="value", data=df_box,order=month)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig