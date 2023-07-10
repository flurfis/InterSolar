import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
import numpy as np
import pdb
from numpy.random import random


def bland_altman_plot(data1, data2, *args, **kwargs):
    data1 = np.asarray(data1)
    data2 = np.asarray(data2)
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between data1 and data2
    md = np.mean(diff)  # Mean of the difference
    sd = np.std(diff, axis=0)  # Standard deviation of the difference
    CI_low = md - 1.96 * sd
    CI_high = md + 1.96 * sd

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md, color='black', linestyle='-')
    plt.axhline(md + 1.96 * sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96 * sd, color='gray', linestyle='--')
    return md, sd, mean, CI_low, CI_high

def format_bland_altman(rp_data, mm_data, plotName):
    five_step_rp_all_col = rp_data.iloc[::5, :]
    five_rp_data = five_step_rp_all_col[8]
    mm_data_s = mm_data[1]
    md, sd, mean, CI_low, CI_high = bland_altman_plot(five_rp_data, mm_data_s)
    #plt.title(r"$\mathbf{Bland-Altman}$" + " " + r"$\mathbf{Plot}$")
    plt.title(plotName, fontweight="bold")
    plt.xlabel("Durchschnittliche Volt Messungen")
    plt.ylabel("Differenz")
    plt.ylim(md - 3.5 * sd, md + 3.5 * sd)

    xOutPlot = np.min(mean) + (np.max(mean) - np.min(mean)) * 1.14

    plt.text(xOutPlot, md - 1.96 * sd,
             r'-1.96 SA:' + "\n" + "%.2f" % CI_low,
             ha="center",
             va="center",
             )
    plt.text(xOutPlot, md + 1.96 * sd,
             r'+1.96 SA:' + "\n" + "%.2f" % CI_high,
             ha="center",
             va="center",
             )
    plt.text(xOutPlot, md,
             r'Mean:' + "\n" + "%.2f" % md,
             ha="center",
             va="center",
             )
    plt.subplots_adjust(right=0.85)
    figname = "plots/BlandAltman/BA_" + plotName + ".png"
    plt.savefig(figname)
    plt.show()
    #print("liksdh")

def create_basic_plot(rp_data, mm_data, plotName):
    #plt = data[8].plot()
    #plt = rp_data[8].plot(x="min", y="Volt")
    mm_s = mm_data[1]
    idx_mm = pd.Series(range(0, 5*mm_s.size, 5))

    plt.plot(rp_data[8], label='Raspberry Pi')
    #plt.scatter(idx_mm, mm_s, c='red', s=15, label='Multimeter')
    plt.plot(idx_mm, mm_s, c='red', label='Multimeter')

    plt.xlabel("Zeit in Minuten")
    plt.ylabel("Volt")
    plt.legend(prop={'size': 6})
    plt.title(plotName, fontweight="bold")
    figname = "plots/" + plotName + ".png"
    plt.savefig(figname)
    plt.show()

def create_diff_plot(rp_data, mm_data, plotName):
    #https://stackoverflow.com/questions/16399279/bland-altman-plot-in-python
    five_step_rp_all_col = rp_data.iloc[::5, :]
    five_rp_data = five_step_rp_all_col[8].to_numpy()
    mm_data_s = mm_data[1].to_numpy()
    #import pingouin as pg
    #ax = pg.plot_blandaltman(df['new'], df['gold_standard'])


    f, ax = plt.subplots(1, figsize=(8, 5))
    sm.graphics.mean_diff_plot(five_rp_data, mm_data_s, sd_limit = 0, ax=ax)
    plt.title(plotName, fontweight="bold")
    figname = "plots/BlandAltman/BA_" + plotName + ".png"
    plt.savefig(figname, bbox_inches='tight')
    plt.show()

def time_diff_plot(rp_data, mm_data, plotName):
    five_step_rp_all_col = rp_data.iloc[::5, :].reset_index()
    five_rp_data = five_step_rp_all_col[8]
    mm_data_s = mm_data[1]

    diff = mm_data_s.sub(five_rp_data)

    idx_mm = pd.Series(range(0, 5 * mm_data_s.size, 5))

    plt.scatter(idx_mm, diff,  label='Differenz')

    # obtain m (slope) and b(intercept) of linear regression line
    m, b = np.polyfit(idx_mm, diff, 1)

    # add linear regression line to scatterplot
    plt.plot(idx_mm, m * idx_mm + b, c='red', label='Lin. Regression')

    plt.xlabel("Zeit in Minuten")
    plt.ylabel("Differenz (Multimeter - Raspberry Pi)")
    plt.legend(prop={'size': 6})
    plt.title(plotName, fontweight="bold")
    figname = "plots/diff_to_time_plots/diff_" + plotName + ".png"
    plt.savefig(figname)
    plt.show()

    #print("lslkdjf")

def basic_plot_aufl(rp_data, mm_data, plotName):
    mm_s = mm_data[1]
    idx_mm = pd.Series(range(0, 5 * mm_s.size, 5))

    filter = rp_data[5]==15
    start_afer_hole = rp_data.where(filter, inplace=False)

    plt.plot(rp_data[8], c='C0', label='Raspberry Pi')
    plt.plot(start_afer_hole[8], 'r1', markersize=6, c='fuchsia', label='Raspberry Pi, Restart')
    # plt.scatter(idx_mm, mm_s, c='red', s=15, label='Multimeter')
    plt.plot(idx_mm, mm_s, c='red', label='Multimeter')

    plt.xlabel("Zeit in Minuten")
    plt.ylabel("Volt")
    plt.legend(prop={'size': 6})
    plt.title(plotName, fontweight="bold")
    figname = "plots/" + plotName + ".png"
    plt.savefig(figname)
    plt.show()
    lol = 2



def read_data():
    #nm=normalmode, rp=raspberry py, mm=multimeter
    print("start")
    path_raumtemp_nm_mm = os.path.join('..', 'Messungen', 'Raumtemperatur_NormalMode', 'measurements_raumtemp_normalmode.csv')
    path_raumtemp_nm_rp = os.path.join('..', 'Messungen', 'Raumtemperatur_NormalMode', 'voltmeter_raumtemp_normalmode.csv')

    path_warm_nm_mm = os.path.join('..', 'Messungen', 'warm_normalMode','messungen_warm_normal_mode.csv')
    path_warm_nm_rp = os.path.join('..', 'Messungen', 'warm_normalMode','voltmeter_warm.csv')

    path_cold_nm_mm = os.path.join('..', 'Messungen', 'Kalt_normalMode', 'messungen_multimeter_kalt.csv')
    path_cold_nm_rp = os.path.join('..', 'Messungen', 'Kalt_normalMode', 'voltmeter_cold.csv')

    #entladen
    path_raumtemp_entl_mm = os.path.join('..', 'Messungen', 'Raumtemp_entlMode', 'raumtemp_entladung_manuell.csv')
    path_raumtemp_entl_rp = os.path.join('..', 'Messungen', 'Raumtemp_entlMode', 'voltmeter_raum_entl.csv')

    #aufladen
    path_aufl_mm = os.path.join('..', 'Messungen', 'aufladen_sonne', 'manuell_aufl_sonne.csv')
    path_aufl_rp = os.path.join('..', 'Messungen', 'aufladen_sonne', 'voltmeter_heiss_aufladen_u_entl.csv')


    #y,m,d,wd,h,min,s,ms,val (8)
    data_raumtmp_nm_mm = pd.read_csv(path_raumtemp_nm_mm, header=None, skiprows=[0])
    data_raumtmp_nm_rp = pd.read_csv(path_raumtemp_nm_rp, header=None)
    create_basic_plot(data_raumtmp_nm_rp, data_raumtmp_nm_mm, "Normaler Betrieb bei Raumtemperatur")
    #create_diff_plot(data_raumtmp_nm_rp, data_raumtmp_nm_mm, "Normaler Betrieb bei Raumtemperatur")
    format_bland_altman(data_raumtmp_nm_rp, data_raumtmp_nm_mm, "Normaler Betrieb bei Raumtemperatur")
    time_diff_plot(data_raumtmp_nm_rp, data_raumtmp_nm_mm, "Normaler Betrieb bei Raumtemperatur")

    data_warm_nm_mm = pd.read_csv(path_warm_nm_mm, header=None, skiprows=[0])
    data_warm_nm_rp = pd.read_csv(path_warm_nm_rp, header=None)
    create_basic_plot(data_warm_nm_rp, data_warm_nm_mm, "Normaler Betrieb bei 30 Grad Celsius")
    format_bland_altman(data_warm_nm_rp, data_warm_nm_mm, "Normaler Betrieb bei 30 Grad Celsius")
    time_diff_plot(data_warm_nm_rp, data_warm_nm_mm, "Normaler Betrieb bei 30 Grad Celsius")

    data_cold_nm_mm = pd.read_csv(path_cold_nm_mm, header=None, skiprows=[0])
    data_cold_nm_rp = pd.read_csv(path_cold_nm_rp, header=None)
    create_basic_plot(data_cold_nm_rp, data_cold_nm_mm, "Normaler Betrieb bei kalter Temperatur")
    format_bland_altman(data_cold_nm_rp, data_cold_nm_mm, "Normaler Betrieb bei kalter Temperatur")
    time_diff_plot(data_cold_nm_rp, data_cold_nm_mm, "Normaler Betrieb bei kalter Temperatur")

    data_raumtmp_entl_mm = pd.read_csv(path_raumtemp_entl_mm, header=None, skiprows=[0])
    data_raumtmp_entl_rp = pd.read_csv(path_raumtemp_entl_rp, header=None)
    create_basic_plot(data_raumtmp_entl_rp, data_raumtmp_entl_mm, "Entladen bei Raumtemperatur")
    format_bland_altman(data_raumtmp_entl_rp, data_raumtmp_entl_mm, "Entladen bei Raumtemperatur")
    time_diff_plot(data_raumtmp_entl_rp, data_raumtmp_entl_mm, "Entladen bei Raumtemperatur")

    data_aufl_mm = pd.read_csv(path_aufl_mm, header=None, skiprows=[0])
    data_aufl_rp = pd.read_csv(path_aufl_rp, header=None)
    create_basic_plot(data_aufl_rp, data_aufl_mm, "Aufladen in der Sonne")
    basic_plot_aufl(data_aufl_rp, data_aufl_mm, "Aufladen in der Sonne")
    #create_diff_plot(data_aufl_rp, data_aufl_mm, "Aufladen in der Sonne")


if __name__ == '__main__':
    data = read_data()


