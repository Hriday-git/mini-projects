import plotly.express as px

fig = px.bar(x=["A", "B", "C"], y=[10, 20, 30],
             title="Test Plot - If this opens, everything works")

fig.show(renderer="browser")