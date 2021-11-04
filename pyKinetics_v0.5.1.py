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
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import axes3d
import webbrowser

def import_csv_data():
    global fName
    fTyp = [('Comma-separated values files','*.csv'), ('All files', '*.*')]
    iDir = '/home/wangzhe/Desktop/unisoku_fake_mac/data/'         #iDir = '/home/'
    csvfilepath = filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir, title = 'Choose file')
    fName.set(csvfilepath)
    global fileName
    fileName = fName.get()

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

    def mono_exp_decay(start_time, end_time, wavel):
        A0, K0, C0 = 10, 10, 0
        fit_xList, fit_intList = [], []
        for i in range(len(decayTime)):
            if decayTime[i] >= start_time and decayTime[i] <= end_time:
                fit_xList.append(decayTime[i])
                fit_intList.append(waveMatrix[wavel][i])
        fit_x = np.array(fit_xList, dtype = float)
        fit_int = np.array(fit_intList, dtype = float)

        def model_func(t, A, K, C):
            global startTime
            return A * np.exp((1/K) * (startTime-t)) + C            

        def fit_exp_nonlinear(t, y):
            opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y, maxfev = 10000)
            A, K, C = opt_parms
            return A, K, C          

        A1, K1, C1 = fit_exp_nonlinear(fit_x, fit_int)
        fittedY = model_func(fit_x, A1, K1, C1)
        diffY = fit_intList - fittedY

        fig_f, ax_f = plt.subplots()
        ax_f.plot(decayTime, waveMatrix[wavel], linewidth = 1, label = 'Expt.')
        ax_f.plot(fit_x, diffY, c = 'green', linewidth = 1, label = ' Diff.', alpha = 0.9)
        ax_f.plot(fit_x, fittedY, c = 'red', linewidth = 1, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f$' % (A1, K1, C1))
        ax_f.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax_f.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ax_f.set_title(f'{wavel} nm')
        ax_f.legend()           

        figWinFit = Toplevel()
        figWinFit.title('Decay Fitting:' + fileName)
        canvas_f = FigureCanvasTkAgg(fig_f, figWinFit)
        canvas_f.get_tk_widget().pack(expand = True, fill = 'both')
        toolbar_f = NavigationToolbar2Tk(canvas_f, figWinFit, pack_toolbar = False).pack()

    def snd_exp_decay(start_time, end_time, wavel):
        A0, K0, C0, B0, L0 = 10, 10, 0, 10, 10
        fit_xList, fit_intList = [], []
        for i in range(len(decayTime)):
            if decayTime[i] >= start_time and decayTime[i] <= end_time:
                fit_xList.append(decayTime[i])
                fit_intList.append(waveMatrix[wavel][i])
        fit_x = np.array(fit_xList, dtype = float)
        fit_int = np.array(fit_intList, dtype = float)

        def model_func2(t, A, K, C, B, L):
            global startTime
            return A * np.exp((1/K) * (startTime-t)) + B * np.exp((1/L) * (startTime-t)) + C

        def fit_exp_nonlinear2(t, y):
            opt_parms, parm_cov = sp.optimize.curve_fit(model_func2, t, y, maxfev = 10000)
            A, K, C, B, L = opt_parms
            return A, K, C, B, L

        A2, K2, C2, B2, L2 = fit_exp_nonlinear2(fit_x, fit_int)
        fittedY2 = model_func2(fit_x, A2, K2, C2, B2, L2)
        diffY2 = fit_intList - fittedY2

        fig_f2, ax_f2 = plt.subplots()
        ax_f2.plot(decayTime, waveMatrix[wavel], linewidth = 1, label = 'Expt.')
        ax_f2.plot(fit_x, diffY2, c = 'green', linewidth = 1, label = ' Diff.', alpha = 0.9)
        ax_f2.plot(fit_x, fittedY2, c = 'red', linewidth = 1, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f$' % (A2, K2, B2, L2, C2))
        ax_f2.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax_f2.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ax_f2.set_title(f'{wavel} nm')
        ax_f2.legend()           

        figWinFit2 = Toplevel()
        figWinFit2.title('Decay Fitting:' + fileName)
        canvas_f2 = FigureCanvasTkAgg(fig_f2, figWinFit2)
        canvas_f2.get_tk_widget().pack(expand = True, fill = 'both')
        toolbar_f2 = NavigationToolbar2Tk(canvas_f2, figWinFit2, pack_toolbar = False).pack()

    def trd_exp_decay(start_time, end_time, wavel):
        A0, B0, C0, D0, K0, L0, M0 = 10, 10, 10, 0, 10, 10, 10
        fit_xList, fit_intList = [], []
        for i in range(len(decayTime)):
            if decayTime[i] >= start_time and decayTime[i] <= end_time:
                fit_xList.append(decayTime[i])
                fit_intList.append(waveMatrix[wavel][i])
        fit_x = np.array(fit_xList, dtype = float)
        fit_int = np.array(fit_intList, dtype = float)

        def model_func3(t, A, B, C, D, K, L, M):
            global startTime
            return A * np.exp((1/K) * (startTime-t)) + B * np.exp((1/L) * (startTime-t)) + C * np.exp((1/M) * (startTime-t)) + D

        def fit_exp_nonlinear3(t, y):
            opt_parms, parm_cov = sp.optimize.curve_fit(model_func3, t, y, maxfev = 100000)
            A, B, C, D, K, L, M = opt_parms
            return A, B, C, D, K, L, M

        A3, B3, C3, D3, K3, L3, M3 = fit_exp_nonlinear3(fit_x, fit_int)
        fittedY3 = model_func3(fit_x, A3, B3, C3, D3, K3, L3, M3)
        diffY3 = fit_intList - fittedY3

        fig_f3, ax_f3 = plt.subplots()
        ax_f3.plot(decayTime, waveMatrix[wavel], linewidth = 1, label = 'Expt.')
        ax_f3.plot(fit_x, diffY3, c = 'green', linewidth = 1, label = ' Diff.', alpha = 0.9)
        ax_f3.plot(fit_x, fittedY3, c = 'red', linewidth = 1, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f$' % (A3, K3, B3, L3, C3, M3, D3))
        ax_f3.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax_f3.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ax_f3.set_title(f'{wavel} nm')
        ax_f3.legend()           

        figWinFit3 = Toplevel()
        figWinFit3.title('Decay Fitting:' + fileName)
        canvas_f3 = FigureCanvasTkAgg(fig_f3, figWinFit3)
        canvas_f3.get_tk_widget().pack(expand = True, fill = 'both')
        toolbar_f3 = NavigationToolbar2Tk(canvas_f3, figWinFit3, pack_toolbar = False).pack()

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
        fig, ax = plt.subplots()
        ax.plot(decayTime, inTensity)
        ax.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ax.set_title(f'{waveLength[0]} nm')
        ln_v = plt.axvline(0, linestyle = 'dashed', linewidth = 1, c = 'grey')
        plt.connect('motion_notify_event', motion)
        startLn = plt.axvline(0, linewidth = 1, color = 'red')
        endLn = plt.axvline(0, linewidth = 1, color = 'blue')
        plt.connect('motion_notify_event', motion3)
        #plt.show()
        figWin = Toplevel()
        figWin.title(fileName)
        canvas = FigureCanvasTkAgg(fig, figWin)
        canvas.get_tk_widget().pack(expand = True, fill = 'both')
        toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).pack()

        fitFrame = LabelFrame(figWin, text = 'Non-linear fitting', font = ('Helvetica', 16, 'bold'), padx = 10, pady = 10)
        fitFrame.pack(fill = 'x')
        global fstOrFitIcon1
        fstOrFitIcon1 = PhotoImage(file = r'assets/fit_icon_1.png')
        lifetimeBtn = Button(fitFrame, image = fstOrFitIcon1, command = lambda: mono_exp_decay(startTime, endTime, waveLength[0])).grid(row = 0, column = 0)
        global sndOrFitIcon1
        sndOrFitIcon1 = PhotoImage(file = r'assets/fit_icon_2.png')
        lifetime2Btn = Button(fitFrame, image = sndOrFitIcon1, command = lambda: snd_exp_decay(startTime, endTime, waveLength[0])).grid(row = 0, column = 1)
        global trdOrFitIcon1
        trdOrFitIcon1 = PhotoImage(file = r'assets/fit_icon_3.png')
        lifetime3Btn = Button(fitFrame, image = trdOrFitIcon1, command = lambda: trd_exp_decay(startTime, endTime, waveLength[0])).grid(row = 0, column = 2)

    # Plot heat map for TAS
    else:
        z = np.array(inTensity).reshape(len(decayTime), len(waveLength))
        x, y = np.meshgrid(waveLength, decayTime)
        fig, ax = plt.subplots(subplot_kw = {"projection": "3d"})
        surf = ax.plot_surface(x, y, z, cmap = cm.coolwarm, linewidth = 0, antialiased = False)
        ax.set_xlabel('Wavelength (nm)', fontsize = 13)
        ax.set_ylabel(f'Time ({timeUnit})', fontsize = 13)
        ax.set_zlabel('ΔAbs.(a.u.)', fontsize = 13)
        fig.colorbar(surf, shrink = 0.5, aspect = 10, pad = 0.2)

        figWin = Toplevel()
        figWin.title(fileName)
        canvas = FigureCanvasTkAgg(fig, figWin)
        canvas.get_tk_widget().pack(expand = True, fill = 'both')
        toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).pack()

        #btnFrameTas = LabelFrame(figWin, padx = 20, pady = 10)
        #btnFrameTas.grid(padx = 10, pady = 10, sticky = W + E)
        #htmpBtn = Button()

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
            canvas3.get_tk_widget().pack(expand = True, fill = 'both')
            toolbar3 = NavigationToolbar2Tk(canvas3, figWin3, pack_toolbar = False).pack()

            fitFrame2 = LabelFrame(figWin3, text = 'Non-linear fitting', font = ('Helvetica', 16, 'bold'), padx = 10, pady = 10)
            fitFrame2.pack(fill = 'x')
            global fstOrFitIcon
            fstOrFitIcon = PhotoImage(file = r'assets/fit_icon_1.png')
            lifetimeBtn2 = Button(fitFrame2, image = fstOrFitIcon, command = lambda: mono_exp_decay(startTime, endTime, wavelen.get())).grid(row = 0, column = 0)
            global sndOrFitIcon
            sndOrFitIcon = PhotoImage(file = r'assets/fit_icon_2.png')
            lifetime2Btn2 = Button(fitFrame2, image = sndOrFitIcon, command = lambda: snd_exp_decay(startTime, endTime, wavelen.get())).grid(row = 0, column = 1)
            global trdOrFitIcon
            trdOrFitIcon = PhotoImage(file = r'assets/fit_icon_3.png')
            lifetime3Btn2 = Button(fitFrame2, image = trdOrFitIcon, command = lambda: trd_exp_decay(startTime, endTime, wavelen.get())).grid(row = 0, column = 2)

        def showHtmp():
            def motion4(event):  
                x1 = event.xdata
                y1 = event.ydata
                ln_v.set_xdata(x1)
                ln_h.set_ydata(y1)
                plt.draw()
            z = np.array(inTensity).reshape(len(decayTime), len(waveLength))
            x, y = np.meshgrid(waveLength, decayTime)
            fig, ax = plt.subplots()
            ax.pcolormesh(x, y, z, shading = 'gouraud')
            ax.set_xlabel('Wavelength (nm)', fontsize = 13)
            ax.set_ylabel(f'Time ({timeUnit})', fontsize = 13)
            ln_v = plt.axvline(midWave, linestyle = 'dashed', linewidth = 1, c = 'grey')
            ln_h = plt.axhline(0, linestyle = 'dashed', linewidth = 1, c = 'grey')
            plt.connect('motion_notify_event', motion4)  

            figWin = Toplevel()
            figWin.title(fileName)
            canvas = FigureCanvasTkAgg(fig, figWin)
            canvas.get_tk_widget().grid()
            toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).grid()

        def show2ddec():
            global fig_w, ax_w
            fig_w, ax_w = plt.subplots()

            def slide(var):
                global fig_w, ax_w
                plt.cla()
                for f in range(len(waveLength)):
                    if f != int(horizontal.get()):
                        ax_w.plot(decayTime, waveMatrix[waveLength[f]], c = 'grey', alpha = 0.2, linewidth = 0.5)
                ax_w.plot(decayTime, waveMatrix[waveLength[horizontal.get()]], c = 'red', linewidth = 0.5)
                ax_w.set_title(f'{waveLength[horizontal.get()]} nm')
                ax_w.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
                ax_w.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
                canvas_w.draw()

            figWinW = Toplevel()
            for g in range(len(waveLength)):
                ax_w.plot(decayTime, waveMatrix[waveLength[g]], linewidth = 0.5)
            ax_w.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
            ax_w.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
            canvas_w = FigureCanvasTkAgg(fig_w, figWinW)
            canvas_w.get_tk_widget().pack(expand = True, fill = 'both')
            toolbar_w = NavigationToolbar2Tk(canvas_w, figWinW, pack_toolbar = False).pack()
            horizontal = Scale(figWinW, from_ = 0, to = len(waveLength) - 1, orient = HORIZONTAL, command = slide, length = 500, showvalue = 0)
            horizontal.pack()

        def show2dtas():
            global fig_t, ax_t
            fig_t, ax_t = plt.subplots()

            def slide_t(var):
                global fig_t, ax_t
                plt.cla()
                for ff in range(len(decayTime)):
                    if ff != int(horizontal_t.get()):
                        ax_t.plot(waveLength, timeMatrix[decayTime[ff]], c = 'grey', alpha = 0.2, linewidth = 0.5)
                ax_t.plot(waveLength, timeMatrix[decayTime[horizontal_t.get()]], c = 'red', linewidth = 0.5)
                ax_t.set_title(f'{decayTime[horizontal_t.get()]} {timeUnit}')
                ax_t.set_xlabel('Wavelength (nm)', fontsize = 13)
                ax_t.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
                canvas_t.draw()

            fig_t, ax_t = plt.subplots()

            figWinT = Toplevel()
            for gg in range(len(waveLength)):
                ax_t.plot(waveLength, timeMatrix[decayTime[gg]], linewidth = 0.5)
            ax_t.set_xlabel('Wavelength (nm)', fontsize = 13)
            ax_t.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
            canvas_t = FigureCanvasTkAgg(fig_t, figWinT)
            canvas_t.get_tk_widget().pack(expand = True, fill = 'both')
            toolbar_t = NavigationToolbar2Tk(canvas_t, figWinT, pack_toolbar = False).pack()
            horizontal_t = Scale(figWinT, from_ = 0, to = len(decayTime) - 1, orient = HORIZONTAL, command = slide_t, length = 500, showvalue = 0)
            horizontal_t.pack()

        tasFrame = LabelFrame(figWin, padx = 20, pady = 10)
        tasFrame.pack(fill = 'x')
        wavelen = IntVar()
        wavelen.set(waveLength[0])
        #tasLbl = Label(tasFrame, text = "For time profile, choose a wavelength: ").grid(row = 0, column = 0)
        waveDrop = OptionMenu(tasFrame, wavelen, *waveLength).grid(row = 0, column = 1)
        decayWaveBtn = Button(tasFrame, text = 'Time Profile', command = showDecay2).grid(row = 0, column = 2)

        global htmpIcon
        htmpIcon = PhotoImage(file = r'assets/htmp_icon.png')
        Button(tasFrame, image = htmpIcon, command = showHtmp).grid(row = 0, column = 3)
        global tasIcon
        tasIcon = PhotoImage(file = r'assets/tas_icon.png')
        Button(tasFrame, image = tasIcon, command = show2dtas).grid(row = 0, column = 4)
        global decIcon
        decIcon = PhotoImage(file = r'assets/dec_icon.png')
        Button(tasFrame, image = decIcon, command = show2ddec).grid(row = 0, column = 5)
        #Label(tasFrame, text = '2D-Heat Map').grid(row = 1, column = 3)

proVer = '0.5.1β'
rlsDate = '2021-11-04'

root = Tk()
root.title(f'py.Kinetics v{proVer}')
#root.iconbitmap('assets/favicon.ico')

wideLogo = ImageTk.PhotoImage(Image.open('assets/pyKinetics_main.png'))
Label(image = wideLogo).grid(row = 0, column = 0, columnspan = 4)

proInfoFrame = LabelFrame(root, borderwidth = 0, highlightthickness = 0)
proInfoFrame.grid(row = 1, column = 0, columnspan = 4, sticky = W + E)
Label(proInfoFrame, text = f'\nVer. {proVer} ({rlsDate})', font = ('Helvetica', 16, 'bold')).pack()
Label(proInfoFrame, text = 'A Python program for kinetics analyses, \ndesigned for laser flash photosis measurements.').pack()
Label(proInfoFrame, text = 'More information on:\nhttps://wongzit.github.io/program/pykinetics/\n\n').pack()

waveLength, decayTime = [], []
waveMatrix, timeMatrix = {}, {}

fName = StringVar()
fileName = ''
filePathStatus = Label(root, textvariable = fName, bd = 1, width = 25, relief = SUNKEN, anchor = E, bg = 'old lace').grid(row = 4, column = 0, columnspan = 4, sticky = W + E)

def openweb():
    webbrowser.open('https://wongzit.github.io/program/pykinetics', new = 1)

openIcon = PhotoImage(file = r'assets/open_icon.png')
readIcon = PhotoImage(file = r'assets/read_icon.png')
quitIcon = PhotoImage(file = r'assets/quit_icon.png')
webIcon = PhotoImage(file = r'assets/web_icon.png')

openButton = Button(root, image = openIcon, padx = 28, pady = 6, command = import_csv_data).grid(row = 2, column = 0)
readButton = Button(root, image = readIcon, padx = 28, pady = 6, command = firstopen).grid(row = 2, column = 1)
quitButton = Button(root, image = quitIcon, padx = 28, pady = 8, command = sys.exit).grid(row = 2, column = 3)
webButton = Button(root, image = webIcon, padx = 28, pady = 6, command = openweb).grid(row = 2, column = 2)
Label(root, text = '1. Open', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 0)
Label(root, text = '2. Read', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 1)
Label(root, text = 'Quit', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 3)
Label(root, text = 'Help', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 2)

root.mainloop()
