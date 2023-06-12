# %% 
"""
Title: Theoretical Threshold Models for Ultrasonic Atomization
Author: Josué D. Meneses Díaz
Date: 2023-05-23
Description: This program creates a simple class with different threshold models for ultrasonic atomization.

#TODO : add experimental curves
#TODO: add VUKASINOVIC's model 
"""


#%%
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ThresholdAtomizationModel:
    """
    Class to model sessile atomization threshold using power ultrasounds.
    """
    def __init__(self):
        """
        Initialize an instance of ThresholdAtomizationModel class.
        """
        self.mu = 1 / 1000      # Pa s, Viscosity
        self.rho = 1000         # kg/m^3, Density
        self.sigma = 72.88 / 1000    # N/m, Surface tension
        self.frequencies = np.linspace(10000, 50000, 1000)   # Hz, Frequency
        # models
        self.experimental_threshold = None
        self.gaete = None
        self.pohlman = None
        self.alzuaga = None
        self.eisenmenger = None
        self.experimental = None

    def update(self):
        """
        Update threshold models.
        """
        self.gaete = self.calculate_gaete_model()
        self.pohlman = self.calculate_pohlman_model()
        self.alzuaga = self.calculate_alzuaga_model()
        self.eisenmenger = self.calculate_eisenmenger_model()

    def calculate_eisenmenger_model(self):
        """
        Calculate Eisenmenger's pseudo empirical model.
        Year: 1959
        """
        return 8 * (self.mu / self.rho) * np.sqrt(self.rho / (2 * np.pi * self.sigma * self.frequencies))
    
    def calculate_pohlman_model(self):
        """
        Calculate Pohlman's model for atomization threshold.
        Year: 1974
        """
        return (2 * self.mu / self.rho) * (self.rho / (np.pi * self.sigma * self.frequencies)) ** (1 / 3)

    def calculate_gaete_model(self):
        """
        Calculate Gaete's empirical model for threshold atomization.
        Year: 2018
        """
        k = 14338 / 1e6
        x = -0.8216
        return k * (self.frequencies ** x)

    def calculate_alzuaga_model(self):
        """
        Calculate Alzuaga's empirical model for threshold atomization.
        Year: 2004
        """
        alpha = 2 * (self.sigma / (self.rho * (self.frequencies ** 2))) ** (2 / 3)
        beta = (8 * self.mu * (2 * np.pi) ** (1 / 3)) / (2 * self.rho * self.frequencies)
        return np.sqrt((18 / (2 * np.pi) ** (7 / 3)) * (alpha + beta))


    def plot_models(self, ax=None, models=None):
        """
        Create a plot with the threshold models.
        """
        if ax is None:
            ax = plt.gca()

        if models is None:
            models = ['gaete', 'eisenmenger', 'pohlman', 'alzuaga']

        for model in models:
            if model == 'gaete':
                ax.plot(self.frequencies, self.gaete * 1e6, label='Gaete 2018')
            elif model == 'eisenmenger':
                ax.plot(self.frequencies, self.eisenmenger * 1e6, label='Eisenmenger 1957')
            elif model == 'pohlman':
                ax.plot(self.frequencies, self.pohlman * 1e6, label='Pohlman 1974')
            elif model == 'alzuaga':
                ax.plot(self.frequencies, self.alzuaga * 1e6, label='Alzuaga 2004')
            else:
                raise ValueError(f"Model '{model}' is not valid.")

        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Threshold [$\mu m$]')
        ax.set_title('Threshold Atomization Models')
        # ax.grid(which='both', color='gray', linestyle='-.', linewidth=0.5)
        ax.legend()


#%%

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    plt.style.use('paper')

    #%% load experimental data
    filename = "data/sessile_drop_thresholds.xlsx"
    df = pd.read_excel(filename, sheet_name='Agua destilada Incerteza', usecols='F:L')
    # df = pd.read_excel(filename, sheet_name='Agua destilada Incerteza', usecols='B:D')
    df
    df_47p8uL = df[(df["Volumen [uL].1"]==47.8)]


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

    ax.plot(df_47p8uL["Frecuencia [Hz].1"], df_47p8uL["Umbral [um].1"], 'ko')
    plt.locator_params(axis='x', nbins=5)
    
    
    ax2 = fig.add_subplot(122)
    models_to_plot = ['gaete', 'eisenmenger', 'pohlman', ] # ['gaete', 'pohlman'] 
    threshold_water.plot_models(ax2, models=models_to_plot)
    ax2.set_ylabel('')
    ax2.set_title('')
    
    
    ax2.plot(df_47p8uL["Frecuencia [Hz].1"], df_47p8uL["Umbral [um].1"], 'ko')
    plt.locator_params(axis='x', nbins=5)

    ax2.errorbar(
                    df_47p8uL["Frecuencia [Hz].1"],
                    df_47p8uL["Umbral [um].1"],
                    yerr=df_47p8uL["dU 2S/sqrt(N) [um]"], 
                    color='k',
                    fmt='o', markersize=6, capsize=4, elinewidth=1, markerfacecolor='k', markeredgewidth=1,
                    label="Experimental"
                )

    plt.suptitle('Modelos de Umbral de Atomización')


    # Normalize vector
    threshold_water.alzuaga = threshold_water.alzuaga/np.max(threshold_water.alzuaga)/1e6
    threshold_water.gaete = threshold_water.gaete/np.max(threshold_water.gaete)/1e6
    threshold_water.eisenmenger = threshold_water.eisenmenger/np.max(threshold_water.eisenmenger)/1e6
    threshold_water.pohlman = threshold_water.pohlman/np.max(threshold_water.pohlman)/1e6
    experimental = df_47p8uL["Umbral [um].1"]/np.max(df_47p8uL["Umbral [um].1"])


    fig = plt.figure(3) # figsize=(10,5))
    ax2 = fig.add_subplot(111)
    threshold_water.plot_models(ax2, models=['eisenmenger', 'pohlman', 'alzuaga', ])
    ax2.set_ylabel('$A_{Th}/A_0$')


    # normalizate experimental data
    ax2.errorbar(
                    df_47p8uL["Frecuencia [Hz].1"],
                    experimental,
                    yerr=df_47p8uL["U/dU"], 
                    color='k',
                    fmt='o', markersize=6, capsize=4, elinewidth=1, markerfacecolor='k', markeredgewidth=1,
                    label="Experimental"
                )

    # ax2.plot(df_47p8uL["Frecuencia [Hz].1"], experimental, 'ko')

    plt.show()


#%%----------------------------------------------------------------


# %%
