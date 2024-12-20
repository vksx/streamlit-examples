import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def DisplayPlot(df):
    if df["month"].dtype == "object":
        df["month"] = (
            pd.Categorical(
                df["month"],
                categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                ordered=True,
            ).codes
            + 1
        )

    month = df["month"]
    col1 = df["col1"]
    col2 = df["col2"]
    col3 = df["col3"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=month, y=col1, name="col1", line=dict(color="blue", width=4))
    )
    fig.add_trace(
        go.Scatter(x=month, y=col2, name="col2", line=dict(color="red", width=2))
    )
    fig.add_trace(
        go.Scatter(
            x=month,
            y=col3,
            name="col3",
            mode="lines",
            line=dict(color="#CDCDCD", width=2, dash="dot"),
        )
    )

    # Iterate through segments and fill regions conditionally
    for i in range(1, len(month)):
        x1, x2 = month[i - 1], month[i]
        y1_col1, y2_col1 = col1[i - 1], col1[i]
        y1_col2, y2_col2 = col2[i - 1], col2[i]

        # Check if col1 is above col2 throughout the segment
        if y1_col1 > y1_col2 and y2_col1 > y2_col2:
            fig.add_trace(
                go.Scatter(
                    x=[x1, x2, x2, x1],
                    y=[y1_col1, y2_col1, y2_col2, y1_col2],
                    fill="toself",
                    fillcolor="rgba(0, 255, 0, 0.3)",  # Green fill
                    mode="none",
                    showlegend=False,
                )
            )
        # Check if col2 is above col1 throughout the segment
        elif y1_col1 < y1_col2 and y2_col1 < y2_col2:
            fig.add_trace(
                go.Scatter(
                    x=[x1, x2, x2, x1],
                    y=[y1_col2, y2_col2, y2_col1, y1_col1],
                    fill="toself",
                    fillcolor="rgba(255, 0, 0, 0.3)",  # Red fill
                    mode="none",
                    showlegend=False,
                )
            )
        else:  # Handle crossing lines within the segment
            # Avoid division by zero by checking if the difference is non-zero
            denominator = (y2_col1 - y1_col1) - (y2_col2 - y1_col2)
            if denominator != 0:
                # Find the intersection point using linear interpolation
                intersect_x = x1 + (x2 - x1) * ((y1_col2 - y1_col1) / denominator)
                intersect_y = y1_col1 + (intersect_x - x1) * (
                    (y2_col1 - y1_col1) / (x2 - x1)
                )

                # Fill green where col1 is above
                if y1_col1 > y1_col2:
                    fig.add_trace(
                        go.Scatter(
                            x=[x1, intersect_x, intersect_x, x1],
                            y=[y1_col1, intersect_y, intersect_y, y1_col2],
                            fill="toself",
                            fillcolor="rgba(0, 255, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )

                    # Fill red where col2 is above
                    fig.add_trace(
                        go.Scatter(
                            x=[intersect_x, x2, x2, intersect_x],
                            y=[intersect_y, y2_col1, y2_col2, intersect_y],
                            fill="toself",
                            fillcolor="rgba(255, 0, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )
                else:
                    # Fill red where col2 is above
                    fig.add_trace(
                        go.Scatter(
                            x=[x1, intersect_x, intersect_x, x1],
                            y=[y1_col2, intersect_y, intersect_y, y1_col1],
                            fill="toself",
                            fillcolor="rgba(255, 0, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )

                    # Fill green where col1 is above
                    fig.add_trace(
                        go.Scatter(
                            x=[intersect_x, x2, x2, intersect_x],
                            y=[intersect_y, y2_col2, y2_col1, intersect_y],
                            fill="toself",
                            fillcolor="rgba(0, 255, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )
            else:
                # If lines are parallel, fill based on initial conditions
                if y1_col1 > y1_col2:
                    fig.add_trace(
                        go.Scatter(
                            x=[x1, x2, x2, x1],
                            y=[y1_col1, y2_col1, y2_col2, y1_col2],
                            fill="toself",
                            fillcolor="rgba(0, 255, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )
                else:
                    fig.add_trace(
                        go.Scatter(
                            x=[x1, x2, x2, x1],
                            y=[y1_col2, y2_col2, y2_col1, y1_col1],
                            fill="toself",
                            fillcolor="rgba(255, 0, 0, 0.3)",
                            mode="none",
                            showlegend=False,
                        )
                    )

    month_mapping = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun"}

    fig.update_layout(
        title=dict(text="Comparison of col1 and col2"),
        xaxis=dict(
            title=dict(text="Month"),
            tickvals=list(month_mapping.keys()),
            ticktext=list(month_mapping.values()),
        ),
        yaxis=dict(title=dict(text="Values")),
        showlegend=True,
    )

    st.plotly_chart(fig)


st.title("Interactive Line Plot with Conditional Filling")
st.write(
    "This app allows you to visualize different datasets with conditional region filling between two lines."
)

datasets = {
    "Actual Dataset": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [0.1555, 0.1097, 0.1459, 0.2804, 0.267],
        "col2": [0.1256, 0.119, 0.175, 0.2634, 0.1855],
        "col3": [0.1863, 0.1863, 0.1863, 0.1863, 0.1863],
    },
    "No Crossing": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [10, 15, 20, 25, 30],
        "col2": [5, 10, 15, 20, 25],
        "col3": [7, 12, 17, 22, 27],
    },
    "Single Crossing": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [10, 20, 15, 25, 30],
        "col2": [5, 15, 20, 10, 25],
        "col3": [7, 12, 17, 22, 27],
    },
    "Multiple Crossings": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [10, 20, 10, 30, 15],
        "col2": [5, 15, 25, 10, 20],
        "col3": [7, 12, 17, 22, 27],
    },
    "Flat Segments": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [10, 15, 15, 20, 25],
        "col2": [5, 15, 15, 10, 20],
        "col3": [7, 12, 17, 22, 27],
    },
    "Zigzagging Lines": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "col1": [10, 20, 15, 25, 20, 30],
        "col2": [5, 15, 20, 10, 25, 15],
        "col3": [7, 12, 17, 22, 27, 32],
    },
    "Extreme Differences": {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "col1": [50, 60, 70, 80, 90],
        "col2": [10, 20, 30, 40, 50],
        "col3": [7, 12, 17, 22, 27],
    },
}

dataset_name = st.sidebar.selectbox("Choose a dataset", list(datasets.keys()))
data = datasets[dataset_name]
df = pd.DataFrame(data)
DisplayPlot(df)
