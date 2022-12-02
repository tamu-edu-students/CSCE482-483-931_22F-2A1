import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./MCityBagFileResultsHN.csv')

precisionsDF = df[df.index % 7 == 6]

precisionsDF = precisionsDF.astype(float)

print("Precision Data Frame:\n", precisionsDF)

print("\nNumber of Precision Samples Taken:", len(precisionsDF))

print("\nMean", precisionsDF.mean())
