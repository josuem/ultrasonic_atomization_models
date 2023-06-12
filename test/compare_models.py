
# %%
import matplotlib.pyplot as plt
from ultrasonic_atomization_models import ThresholdAtomizationModel
import os

plt.style.use('paper')
os.system('cls')

threshold_water = ThresholdAtomizationModel()
threshold_water.frequencies = np.linspace(5900, 45e3, 1000)
threshold_water.update()

fig = plt.figure(1, ) # figsize=(10,5))
ax = fig.add_subplot(111)    
threshold_water.plot_models() # ax, models=models_to_plot
ax.set_title('')

fig = plt.figure(2, figsize=(10,7))
ax = fig.add_subplot(121)    
threshold_water.plot_models() # ax, models=models_to_plot
ax.set_title('')

plt.locator_params(axis='x', nbins=5)

ax2 = fig.add_subplot(122)
models_to_plot = ['gaete', 'eisenmenger', 'pohlman', ] # ['gaete', 'pohlman'] 
threshold_water.plot_models(ax2, models=models_to_plot)
ax2.set_ylabel('')
ax2.set_title('')

plt.show()
