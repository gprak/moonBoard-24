import prepare_data as prd
import pandas as pd
from simple_nn import SimpleNN
import matplotlib.pyplot as plt
#df_5_10 = prd.get_df(5,10)
#print(df_5_10.head())

#df_5_10.to_hdf("df_5_10"+'.h5', key='df', mode='w')
df_5_10 = pd.read_hdf("df_5_10"+'.h5', 'df')


ann = SimpleNN(df_5_10)
epochs = 100
losses_train, loss_test, correct = ann.run_model((10,10),lr=0.01,epochs=epochs)
n_test = ann.y_test.shape[0]

print(ann.y_test.shape[0])
# plt.plot(range(epochs), losses_train)
# plt.ylabel("Loss")
# plt.xlabel("epoch")


print(f"{losses_train[-1]:.8f}")
print(f"{loss_test:.8f}")
print(f"\n{correct} out of {n_test} = {100*correct/n_test:.2f}% correct")
