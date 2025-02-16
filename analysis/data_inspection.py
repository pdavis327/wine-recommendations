# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: davis
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

# %%
wine_df = pd.read_csv("../assets/winemag-data-130k-v2.csv", index_col=[0])


# %%
wine_df = wine_df.drop(['taster_twitter_handle', 'taster_name', 'region_2'],axis=1)

# %%
wine_df = wine_df.rename(columns={'region_1':'region', 'price': 'price_dollars'})

# %%
wine_df.to_csv("../assets/winemag_processed.csv", index=False)

# %%
processed = pd.read_csv("../assets/winemag_processed.csv")

# %%
len(processed.columns)

# %%

# %%
