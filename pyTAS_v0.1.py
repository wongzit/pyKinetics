from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sys
import scipy as sp
import scipy.optimize


def import_csv_data():
    global fName
    fTyp = [('Comma-separated values files','*.csv'), ('All files', '*.*')]
    iDir = '/home/wangzhe/Desktop/unisoku_fake_mac/data/'         #iDir = '/home/'
    csvfilepath = filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir, title = 'Choose file')
    fName.set(csvfilepath)
    global fileName
    fileName = fName.get()

root = Tk()
root.title('py.LFP v0.1-α')
root.geometry('600x600')

def firstopen():
    with open(fileName, 'r') as csvFile:
        csvData = csvFile.readlines()   

    timeUnit = 'ns'
    try:
        with open(f'{fileName[:-3]}HDR', 'r', encoding = "shift-jis") as hdrFile:
            hdrData = hdrFile.readlines()
        for b in hdrData:
            if 'X-unit' in b:
                timeUnit = b.split()[2]
    except FileNotFoundError:
        messagebox.showwarning("Warning", "Could not locate *.HDR file, 'ns' will be used for time unit.")  

    global waveLength
    waveLength = []
    for a in csvData[0].strip().split(','):
        if a:
            waveLength.append(int(a))   

    global decayTime
    decayTime = []
    for b in range(1, len(csvData)):
        decayTime.append(float(csvData[b].strip().split(',')[0]))   

    inTensity = []
    for c in range(1, len(csvData)):
        for d in range(1, len(csvData[c].strip().split(','))):
            inTensity.append(float(csvData[c].strip().split(',')[d]))   

    midWave = waveLength[0] / 2 + waveLength[-1] / 2    

    global waveMatrix
    waveMatrix = {}
    for waveNo in range(len(waveLength)):
        waveInt = []
        for timeNo in range(len(decayTime)):
            waveInt.append(inTensity[waveNo + timeNo * len(waveLength)])
        waveMatrix[waveLength[waveNo]] = waveInt

    global timeMatrix
    timeMatrix = {}
    for timeNo2 in range(len(decayTime)):
        timeInt = []
        for waveNo2 in range(len(waveLength)):
            timeInt.append(inTensity[timeNo2 * len(waveLength) + waveNo2])
        timeMatrix[decayTime[timeNo2]] = timeInt

    def motion(event):  
        x1 = event.xdata
        y1 = event.ydata
        ln_v.set_xdata(x1)
        if len(waveLength) > 1:
            ln_h.set_ydata(y1)
        plt.draw()

    # Plot decay profile for single wavelength
    if len(waveLength) == 1:
        def motion3(event):
            if event.button == 1:
                global startTime
                startX = event.xdata
                startLn.set_xdata(startX)
                startTime = float(startX)
            elif event.button == 3:
                global endTime
                endX = event.xdata
                endLn.set_xdata(endX)
                endTime = float(endX)
            plt.draw()
        #plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(decayTime, inTensity)
        ax.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ln_v = plt.axvline(0, linestyle = 'dashed', linewidth = 1, c = 'grey')
        plt.connect('motion_notify_event', motion)
        startLn = plt.axvline(0, linewidth = 1, color = 'red')
        endLn = plt.axvline(0, linewidth = 1, color = 'blue')
        plt.connect('motion_notify_event', motion3)
        #plt.show()
        figWin = Toplevel()
        figWin.title(fileName)
        canvas = FigureCanvasTkAgg(fig, figWin)
        canvas.get_tk_widget().grid()
        toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).grid()
        
        def mono_exp_decay1(start_time, end_time):
            A0, K0, C0 = 0.005, 8, 0            

            fit_xList, fit_intList = [], []
            for i in range(len(decayTime)):
                if decayTime[i] >= startTime and decayTime[i] <= endTime:
                    fit_xList.append(decayTime[i])
                    fit_intList.append(waveMatrix[waveLength[0]][i])
            fit_x = np.array(fit_xList, dtype = float)
            fit_int = np.array(fit_intList, dtype = float)
            #print(fit_x, fit_int)

            def model_func(t, A, K, C):
                global startTime
                return A * np.exp((1/K) * (startTime-t)) + C            

            def fit_exp_nonlinear(t, y):
                opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y, maxfev = 10000)
                A, K, C = opt_parms
                return A, K, C          

            A1, K1, C1 = fit_exp_nonlinear(fit_x, fit_int)
            #print('$y = %0.4f e^{-t/%0.4f } + %0.4f$ ' % (A1, K1, C1))
            fittedY = model_func(fit_x, A1, K1, C1)         

            fig_f, ax_f = plt.subplots()
            ax_f.plot(decayTime, waveMatrix[waveLength[0]])
            ax_f.plot(fit_x, fittedY, c = 'red', linewidth = 1, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f } + %0.4f$' % (A1, K1, C1))
            #ax_f.plot(fit_x, fittedY)
            ax_f.legend()           

            figWinFit = Toplevel()
            figWinFit.title('Decay Fitting:' + fileName)
            canvas_f = FigureCanvasTkAgg(fig_f, figWinFit)
            canvas_f.get_tk_widget().grid()

        lifetimeBtn = Button(figWin, text = "Exponential fitting", command = lambda: mono_exp_decay1(startTime, endTime)).grid()

    # Plot heat map for TAS
    else:
        z = np.array(inTensity).reshape(len(decayTime), len(waveLength))
        x, y = np.meshgrid(waveLength, decayTime)
        fig, ax = plt.subplots()
        ax.pcolormesh(x, y, z, shading = 'gouraud')
        ax.set_xlabel('Wavelength (nm)', fontsize = 13)
        ax.set_ylabel(f'Time ({timeUnit})', fontsize = 13)
        ln_v = plt.axvline(midWave, linestyle = 'dashed', linewidth = 1, c = 'grey')
        ln_h = plt.axhline(0, linestyle = 'dashed', linewidth = 1, c = 'grey')
        plt.connect('motion_notify_event', motion)

        figWin = Toplevel()
        figWin.title(fileName)
        canvas = FigureCanvasTkAgg(fig, figWin)
        canvas.get_tk_widget().grid()
        toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).grid()

    if len(waveLength) > 1:
        def showDecay2():
            def motion2(event):  
                x2 = event.xdata
                ln_v2.set_xdata(x2)
                plt.draw()

            def motion3(event):
                if event.button == 1:
                    global startTime
                    startX = event.xdata
                    startLn.set_xdata(startX)
                    startTime = float(startX)
                elif event.button == 3:
                    global endTime
                    endX = event.xdata
                    endLn.set_xdata(endX)
                    endTime = float(endX)
                plt.draw()

            #startTime = 0
            #endTime = 0

            fig3, ax3 = plt.subplots()
            startLn = plt.axvline(0, linewidth = 1, color = 'red')
            endLn = plt.axvline(0, linewidth = 1, color = 'blue')
            plt.connect('motion_notify_event', motion3)

            ax3.plot(decayTime, waveMatrix[wavelen.get()])
            ax3.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
            ax3.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
            ax3.set_title(f'{wavelen.get()} nm')

            ln_v2 = plt.axvline(0, linestyle = 'dashed', linewidth = 1, c = 'grey')
            plt.connect('motion_notify_event', motion2)

            figWin3 = Toplevel()
            figWin3.title(fileName)
            canvas3 = FigureCanvasTkAgg(fig3, figWin3)
            canvas3.get_tk_widget().grid()
            toolbar3 = NavigationToolbar2Tk(canvas3, figWin3, pack_toolbar = False).grid()

            def mono_exp_decay(start_time, end_time, wavel):
                #print(start_time, end_time, wavel)
                A0, K0, C0 = 0.005, 8, 0            

                fit_xList, fit_intList = [], []
                for i in range(len(decayTime)):
                    if decayTime[i] >= startTime and decayTime[i] <= endTime:
                        fit_xList.append(decayTime[i])
                        fit_intList.append(waveMatrix[wavel][i])
                fit_x = np.array(fit_xList, dtype = float)
                fit_int = np.array(fit_intList, dtype = float)
                #print(fit_x, fit_int)

                def model_func(t, A, K, C):
                    global startTime
                    return A * np.exp((1/K) * (startTime-t)) + C            

                def fit_exp_nonlinear(t, y):
                    opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y, maxfev = 10000)
                    A, K, C = opt_parms
                    return A, K, C          

                A1, K1, C1 = fit_exp_nonlinear(fit_x, fit_int)
                #print('$y = %0.4f e^{-t/%0.4f } + %0.4f$ ' % (A1, K1, C1))
                fittedY = model_func(fit_x, A1, K1, C1)         

                fig_f, ax_f = plt.subplots()
                ax_f.plot(decayTime, waveMatrix[wavel])
                ax_f.plot(fit_x, fittedY, c = 'red', linewidth = 1, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f } + %0.4f$' % (A1, K1, C1))
                #ax_f.plot(fit_x, fittedY)
                ax_f.legend()           

                figWinFit = Toplevel()
                figWinFit.title('Decay Fitting:' + fileName)
                canvas_f = FigureCanvasTkAgg(fig_f, figWinFit)
                canvas_f.get_tk_widget().grid()
            
            lifetimeBtn2 = Button(figWin3, text = "Exponential fitting", command = lambda: mono_exp_decay(startTime, endTime, int(wavelen.get()))).grid()
        
        wavelen = IntVar()
        wavelen.set(waveLength[0])
        waveDrop = OptionMenu(figWin, wavelen, *waveLength).grid()
        decayWaveBtn = Button(figWin, text = 'Time Profile', command = showDecay2).grid()

waveLength, decayTime = [], []
waveMatrix, timeMatrix = {}, {}

Label(root, text = 'Read data from:').grid(row = 1, column = 0)
fName = StringVar()
fileName = ''
filePathEntry = Entry(root, textvariable = fName).grid(row = 1, column = 1, columnspan = 2)

openButton = Button(root, text = 'Open .csv file', command = import_csv_data).grid(row = 2, column = 0, columnspan = 1)
readButton = Button(root, text = 'Read', command = firstopen).grid(row = 2, column = 2)
quitButton = Button(root, text = 'Quit Program', command = sys.exit).grid(row = 3, column = 0)


root.mainloop()

