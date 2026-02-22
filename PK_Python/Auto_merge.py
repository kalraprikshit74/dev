import pandas as pd


df1 = pd.read_csv("target.csv", sep="\t")
df2 = pd.read_csv("source.csv", sep="\t")

missing_in_df2 = [col for col in df1.columns if col not in df2.columns]
df1_cols = list(df1.columns)
for col in missing_in_df2:
    most_common_values = {col: df1[col].mode()[0] for col in missing_in_df2}
    id = df1_cols.index(col)
    print(id,col,most_common_values[col])
    df2.insert(id, col, most_common_values[col])
df2.to_csv("output.csv", sep="\t", index=False)

print("Merge complete. Output saved as: output.csv")
