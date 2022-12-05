import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

precisionsDF = pd.read_csv('./MCityBagFileResultsDN.csv')

precisionsDF = precisionsDF.astype(float)

print("Precision Data Frame:\n", precisionsDF)

print("\nNumber of Precision Samples Taken:", len(precisionsDF))

print("\nMean", precisionsDF.mean())

fig, axes = plt.subplots(1, 1)
fig.suptitle('Precision Scatterplot')
axes.set_xlabel("Data Sample")
axes.set_ylabel("Precision")
sns.scatterplot(data=precisionsDF, x=precisionsDF.index, y="Precision")
fig.set_size_inches(10, 10)
plt.show()