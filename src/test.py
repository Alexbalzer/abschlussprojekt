import plotly.express as px
import pandas as pd

# Beispiel-DataFrame
df = pd.DataFrame({
    "x": ["A", "B", "C"],
    "y": [1, 3, 2]
})

fig = px.bar(df, x="x", y="y")
fig.write_image("test_output.png")
