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

def sysSetting():
    setWin = Toplevel()
    setWin.title('Setting Panel')
    plotStyleFrame = LabelFrame(setWin, text = ' Time Trace Plot Style ', font = ('Helvetica', 15, 'bold'), padx = 20, pady = 20)
    plotStyleFrame.pack(padx = 20, pady = 20, fill = 'x')

    global plotStyle
    plotStyle.set('tableau-colorblind10')

    global style1Pic
    global style2Pic
    global style3Pic
    global style4Pic
    global style5Pic
    global style6Pic
    global style7Pic
    global style8Pic
    global style9Pic
    global style10Pic
    style1Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/tableau-colorblind10.png').resize((200, 177)))
    Label(plotStyleFrame, image = style1Pic).grid(row = 0, column = 0)
    style2Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/seaborn-ticks.png').resize((200, 177)))
    Label(plotStyleFrame, image = style2Pic).grid(row = 0, column = 1)
    style3Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/seaborn-whitegrid.png').resize((200, 177)))
    Label(plotStyleFrame, image = style3Pic).grid(row = 0, column = 2)
    style4Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/Solarize_Light2.png').resize((200, 177)))
    Label(plotStyleFrame, image = style4Pic).grid(row = 0, column = 3)
    style5Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/grayscale.png').resize((200, 177)))
    Label(plotStyleFrame, image = style5Pic).grid(row = 0, column = 4)
    style6Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/dark_background.png').resize((200, 177)))
    Label(plotStyleFrame, image = style6Pic).grid(row = 2, column = 0)
    style7Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/seaborn-darkgrid.png').resize((200, 177)))
    Label(plotStyleFrame, image = style7Pic).grid(row = 2, column = 1)
    style8Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/ggplot.png').resize((200, 177)))
    Label(plotStyleFrame, image = style8Pic).grid(row = 2, column = 2)
    style9Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/bmh.png').resize((200, 177)))
    Label(plotStyleFrame, image = style9Pic).grid(row = 2, column = 3)
    style10Pic = ImageTk.PhotoImage(Image.open('assets/2d_style/seaborn-dark.png').resize((200, 177)))
    Label(plotStyleFrame, image = style10Pic).grid(row = 2, column = 4) 

    style1 = Radiobutton(plotStyleFrame, text = 'Tableau', variable = plotStyle, value = 'tableau-colorblind10').grid(row = 1, column = 0)
    style2 = Radiobutton(plotStyleFrame, text = 'Ticks', variable = plotStyle, value = 'seaborn-ticks').grid(row = 1, column = 1)
    style3 = Radiobutton(plotStyleFrame, text = 'White Grid', variable = plotStyle, value = 'seaborn-whitegrid').grid(row = 1, column = 2)
    style4 = Radiobutton(plotStyleFrame, text = 'Solarize', variable = plotStyle, value = 'Solarize_Light2').grid(row = 1, column = 3)
    style5 = Radiobutton(plotStyleFrame, text = 'Gray Scale', variable = plotStyle, value = 'grayscale').grid(row = 1, column = 4)
    style6 = Radiobutton(plotStyleFrame, text = 'Dark BG', variable = plotStyle, value = 'dark_background').grid(row = 3, column = 0)
    style7 = Radiobutton(plotStyleFrame, text = 'Dark Grid', variable = plotStyle, value = 'seaborn-darkgrid').grid(row = 3, column = 1)
    style8 = Radiobutton(plotStyleFrame, text = 'ggplot', variable = plotStyle, value = 'ggplot').grid(row = 3, column = 2)
    style9 = Radiobutton(plotStyleFrame, text = 'BMH', variable = plotStyle, value = 'bmh').grid(row = 3, column = 3)
    style10 = Radiobutton(plotStyleFrame, text = 'Dark', variable = plotStyle, value = 'seaborn-dark').grid(row = 3, column = 4)    

    lineFrame = LabelFrame(setWin, text = ' Line Width & Color Style ', font = ('Helvetica', 15, 'bold'), padx = 20, pady = 20)
    lineFrame.pack(padx = 20, pady = 20, fill = 'x')    

    Label(lineFrame, text = 'Transient absorption spectrum :').grid(row = 0, column = 0)
    Label(lineFrame, text = ',  Time traces :').grid(row = 0, column = 2)   

    global tasLW
    tasLW.set('0.5')
    Spinbox(lineFrame, textvariable = tasLW, from_ = 0.5, to = 5, increment = 0.5, format = '%1.1f', width = 5).grid(row = 0, column = 1)
    global decLW
    decLW.set('0.5')
    Spinbox(lineFrame, textvariable = decLW, from_ = 0.5, to = 5, increment = 0.5, format = '%1.1f', width = 5).grid(row = 0, column = 3)   

    Label(lineFrame, text = ',  Line color :').grid(row = 0, column = 4)
    global lineColorVal
    lineColorVal.set('tab:blue')
    lineColorE = Entry(lineFrame, textvariable = lineColorVal, width = 10).grid(row = 0, column = 5)    

    Label(lineFrame, text = ',  Heatmap color style :').grid(row = 0, column = 6)
    global campVal
    campVal.set('plasma')
    campE = Entry(lineFrame, textvariable = campVal, width = 10).grid(row = 0, column = 7)  

    paraFrame = LabelFrame(setWin, text = ' Initial Guess of Line Fitting ', font = ('Helvetica', 15, 'bold'), padx = 20, pady = 20)
    paraFrame.pack(padx = 20, pady = 20, fill = 'x')    

    Label(paraFrame, text = 'y = p1 + p3*exp(-t/p4)', font = ('Helvetica', 13, 'bold')).grid(row = 0, column = 0, columnspan = 14)
    Label(paraFrame, text = 'y = p1 + p3*exp(-t/p4) + p5*exp(-t/p6)', font = ('Helvetica', 13, 'bold')).grid(row = 1, column = 0, columnspan = 14)
    Label(paraFrame, text = 'y = p1 + p3*exp(-t/p4) + p5*exp(-t/p6) + p7*exp(-t/p8)\n', font = ('Helvetica', 13, 'bold')).grid(row = 2, column = 0, columnspan = 14)    

    Label(paraFrame, text = 'p1 =').grid(row = 3, column = 0)
    Label(paraFrame, text = ', p3 =').grid(row = 3, column = 2)
    Label(paraFrame, text = ', p4 =').grid(row = 3, column = 4)
    Label(paraFrame, text = ', p5 =').grid(row = 3, column = 6)
    Label(paraFrame, text = ', p6 =').grid(row = 3, column = 8)
    Label(paraFrame, text = ', p7 =').grid(row = 3, column = 10)
    Label(paraFrame, text = ', p8 =').grid(row = 3, column = 12)    

    global p1Val
    global p3Val
    global p4Val
    global p5Val
    global p6Val
    global p7Val
    global p8Val

    p1Val.set('0')
    p3Val.set('10')
    p4Val.set('10')
    p5Val.set('10')
    p6Val.set('10')
    p7Val.set('10')
    p8Val.set('10')

    p1E = Entry(paraFrame, textvariable = p1Val, width = 3).grid(row = 3, column = 1)
    p3E = Entry(paraFrame, textvariable = p3Val, width = 3).grid(row = 3, column = 3)
    p4E = Entry(paraFrame, textvariable = p4Val, width = 3).grid(row = 3, column = 5)
    p5E = Entry(paraFrame, textvariable = p5Val, width = 3).grid(row = 3, column = 7)
    p6E = Entry(paraFrame, textvariable = p6Val, width = 3).grid(row = 3, column = 9)
    p7E = Entry(paraFrame, textvariable = p7Val, width = 3).grid(row = 3, column = 11)
    p8E = Entry(paraFrame, textvariable = p8Val, width = 3).grid(row = 3, column = 13)  

    def ok():
        global plot_style
        global tas_lw
        global dec_lw
        global line_color
        global cmap_color
        global p1_guess
        global p3_guess
        global p4_guess
        global p5_guess
        global p6_guess
        global p7_guess
        global p8_guess
        plot_style = 'seaborn-darkgrid'
        tas_lw = 0.5
        dec_lw = 0.5
        line_color = 'tab:blue'
        cmap_color = 'plasma'
        p1_guess = 0.0
        p3_guess = 10.0
        p4_guess = 10.0
        p5_guess = 10.0
        p6_guess = 10.0
        p7_guess = 10.0
        p8_guess = 10.0
        plot_style = str(plotStyle.get())
        tas_lw = float(tasLW.get())
        dec_lw = float(decLW.get())
        line_color = str(lineColorVal.get())
        cmap_color = str(campVal.get())
        p1_guess = float(p1Val.get())
        p3_guess = float(p3Val.get())
        p4_guess = float(p4Val.get())
        p5_guess = float(p5Val.get())
        p6_guess = float(p6Val.get())
        p7_guess = float(p7Val.get())
        p8_guess = float(p8Val.get())
        setWin.destroy()

    okBtn = Button(setWin, text = 'OK', command = ok, padx = 6, pady = 6).pack()

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
        global p3_guess
        p3_guess = float(p3Val.get())
        global p4_guess
        p4_guess = float(p4Val.get())
        global p1_guess
        p1_guess = float(p1Val.get())
        A0, K0, C0 = p3_guess, p4_guess, p1_guess
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

        global plot_style
        plt.style.use(plot_style)
        fig_f, ax_f = plt.subplots()

        global dec_lw
        global line_color
        ax_f.plot(decayTime, waveMatrix[wavel], c = line_color, linewidth = dec_lw)
        ax_f.plot(fit_x, diffY, c = 'tab:green', linewidth = dec_lw, alpha = 0.9)
        ax_f.plot(fit_x, fittedY, c = 'tab:red', linewidth = dec_lw, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f$' % (A1, K1, C1))
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
        global p5_guess
        p5_guess = float(p5Val.get())
        global p6_guess
        p6_guess = float(p6Val.get())
        global p3_guess
        p3_guess = float(p3Val.get())
        global p4_guess
        p4_guess = float(p4Val.get())
        global p1_guess
        p1_guess = float(p1Val.get())
        A0, K0, C0, B0, L0 = p3_guess, p4_guess, p1_guess, p5_guess, p6_guess
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

        global plot_style
        plt.style.use(plot_style)
        fig_f2, ax_f2 = plt.subplots()

        global dec_lw
        global line_color
        ax_f2.plot(decayTime, waveMatrix[wavel], c = line_color, linewidth = dec_lw)
        ax_f2.plot(fit_x, diffY2, c = 'green', linewidth = dec_lw, alpha = 0.9)
        ax_f2.plot(fit_x, fittedY2, c = 'red', linewidth = dec_lw, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f$' % (A2, K2, B2, L2, C2))
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
        global p7_guess
        p7_guess = float(p7Val.get())
        global p8_guess
        p8_guess = float(p8Val.get())
        global p5_guess
        p5_guess = float(p5Val.get())
        global p6_guess
        p6_guess = float(p6Val.get())
        global p3_guess
        p3_guess = float(p3Val.get())
        global p4_guess
        p4_guess = float(p4Val.get())
        global p1_guess
        p1_guess = float(p1Val.get())
        A0, B0, C0, D0, K0, L0, M0 = p3_guess, p5_guess, p7_guess, p1_guess, p4_guess, p6_guess, p8_guess
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
        
        global plot_style
        plt.style.use(plot_style)
        fig_f3, ax_f3 = plt.subplots()

        global dec_lw
        global line_color
        ax_f3.plot(decayTime, waveMatrix[wavel], c = line_color, linewidth = dec_lw)
        ax_f3.plot(fit_x, diffY3, c = 'green', linewidth = dec_lw, alpha = 0.9)
        ax_f3.plot(fit_x, fittedY3, c = 'red', linewidth = dec_lw, label = 'Fitted Function:\n $y = %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f e^{-t/%0.4f} + %0.4f$' % (A3, K3, B3, L3, C3, M3, D3))
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
        global plot_style
        plt.style.use(plot_style)
        fig, ax = plt.subplots()
        
        global dec_lw
        global line_color
        ax.plot(decayTime, inTensity, c = line_color, linewidth = dec_lw)
        ax.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
        ax.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
        ax.set_title(f'{waveLength[0]} nm')
        ln_v = plt.axvline(0, linestyle = 'dashed', linewidth = 0.5, c = 'tab:grey')
        plt.connect('motion_notify_event', motion)
        startLn = plt.axvline(0, linewidth = 0.5, color = 'tab:red')
        endLn = plt.axvline(0, linewidth = 0.5, color = 'tab:green')
        plt.connect('motion_notify_event', motion3)

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
        plt.style.use('default')
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
            
            global plot_style
            plt.style.use(plot_style)
            fig3, ax3 = plt.subplots()
            startLn = plt.axvline(0, linewidth = 0.5, color = 'tab:red')
            endLn = plt.axvline(0, linewidth = 0.5, color = 'tab:green')
            plt.connect('motion_notify_event', motion3)

            global dec_lw
            global line_color
            ax3.plot(decayTime, waveMatrix[wavelen.get()], c = line_color, linewidth = dec_lw)
            ax3.set_ylabel('ΔAbs.(a.u.)', fontsize = 13)
            ax3.set_xlabel(f'Time ({timeUnit})', fontsize = 13)
            ax3.set_title(f'{wavelen.get()} nm')

            ln_v2 = plt.axvline(0, linestyle = 'dashed', linewidth = 0.5, c = 'tab:grey')
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
            plt.style.use('default')
            fig, ax = plt.subplots()
            global cmap_color
            ax.pcolormesh(x, y, z, shading = 'gouraud', cmap = cmap_color)
            ax.set_xlabel('Wavelength (nm)', fontsize = 13)
            ax.set_ylabel(f'Time ({timeUnit})', fontsize = 13)
            ln_v = plt.axvline(midWave, linestyle = 'dashed', linewidth = 0.5, c = 'tab:grey')
            ln_h = plt.axhline(0, linestyle = 'dashed', linewidth = 0.5, c = 'tab:grey')
            plt.connect('motion_notify_event', motion4)  

            figWin = Toplevel()
            figWin.title(fileName)
            canvas = FigureCanvasTkAgg(fig, figWin)
            canvas.get_tk_widget().grid()
            toolbar = NavigationToolbar2Tk(canvas, figWin, pack_toolbar = False).grid()

        def show2ddec():
            global fig_w, ax_w
            plt.style.use('default')
            fig_w, ax_w = plt.subplots()

            def slide(var):
                global fig_w, ax_w
                plt.cla()
                global tas_lw
                for f in range(len(waveLength)):
                    if f != int(horizontal.get()):
                        ax_w.plot(decayTime, waveMatrix[waveLength[f]], c = 'tab:grey', alpha = 0.2, linewidth = tas_lw)
                ax_w.plot(decayTime, waveMatrix[waveLength[horizontal.get()]], c = 'tab:red', linewidth = tas_lw)
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
            plt.style.use('default')
            fig_t, ax_t = plt.subplots()

            def slide_t(var):
                global fig_t, ax_t
                plt.cla()
                global tas_lw
                for ff in range(len(decayTime)):
                    if ff != int(horizontal_t.get()):
                        ax_t.plot(waveLength, timeMatrix[decayTime[ff]], c = 'tab:grey', alpha = 0.2, linewidth = tas_lw)
                ax_t.plot(waveLength, timeMatrix[decayTime[horizontal_t.get()]], c = 'tab:red', linewidth = tas_lw)
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
        Label(tasFrame, text = '       Show time trace at').grid(row = 0, column = 3)
        waveDrop = OptionMenu(tasFrame, wavelen, *waveLength).grid(row = 0, column = 4)
        Label(tasFrame, text = ' nm').grid(row = 0, column = 5)
        global decayWaveIcon
        decayWaveIcon = PhotoImage(file = r'assets/decayWaveIcon.png')
        decayWaveBtn = Button(tasFrame, image = decayWaveIcon, command = showDecay2).grid(row = 0, column = 6)

        global htmpIcon
        htmpIcon = PhotoImage(file = r'assets/htmp_icon.png')
        Button(tasFrame, image = htmpIcon, command = showHtmp).grid(row = 0, column = 0)
        global tasIcon
        tasIcon = PhotoImage(file = r'assets/tas_icon.png')
        Button(tasFrame, image = tasIcon, command = show2dtas).grid(row = 0, column = 1)
        global decIcon
        decIcon = PhotoImage(file = r'assets/dec_icon.png')
        Button(tasFrame, image = decIcon, command = show2ddec).grid(row = 0, column = 2)

proVer = '1.0.0'
rlsDate = '2021-11-10'

root = Tk()
root.title(f'py.Kinetics v{proVer}')

wideLogo = ImageTk.PhotoImage(Image.open('assets/pyKinetics_main.png'))
Label(image = wideLogo).grid(row = 0, column = 0, columnspan = 5)

proInfoFrame = LabelFrame(root, borderwidth = 0, highlightthickness = 0)
proInfoFrame.grid(row = 1, column = 0, columnspan = 5, sticky = W + E)
Label(proInfoFrame, text = f'\nVer. {proVer} ({rlsDate})', font = ('Helvetica', 16, 'bold')).pack()
Label(proInfoFrame, text = 'A Python program for kinetics analyses, \ndesigned for laser flash photosis measurements.\n').pack()
#Label(proInfoFrame, text = '--- Authors ---', font = ('Helvetica', 13, 'bold')).pack()
Label(proInfoFrame, text = 'Copyright © 2021 Zhe Wang & Takuma Miyamura\nat Reaction organic chemistry, Hiroshima Univ.\n\n').pack()

waveLength, decayTime = [], []
waveMatrix, timeMatrix = {}, {}

fName = StringVar()
fileName = ''
filePathStatus = Label(root, textvariable = fName, bd = 1, width = 25, relief = SUNKEN, anchor = E, bg = 'old lace').grid(row = 4, column = 0, columnspan = 5, sticky = W + E)

def openweb():
    webbrowser.open('https://wongzit.github.io/program/pykinetics', new = 1)

plot_style = 'tableau-colorblind10'
tas_lw = 0.5
dec_lw = 0.5
line_color = 'tab:blue'
cmap_color = 'plasma'
A_guess = 0.0
B_guess = 10.0
C_guess = 10.0
D_guess = 10.0
K_guess = 10.0
L_guess = 10.0
M_guess = 10.0

plotStyle = StringVar()
tasLW = StringVar()
decLW = StringVar()
lineColorVal = StringVar()
campVal = StringVar()
plotStyle.set('tableau-colorblind10')
tasLW.set('0.5')
decLW.set('0.5')
lineColorVal.set('tab:blue')
campVal.set('plasma')

p1Val = StringVar()
p3Val = StringVar()
p4Val = StringVar()
p5Val = StringVar()
p6Val = StringVar()
p7Val = StringVar()
p8Val = StringVar()

p1Val.set('0')
p3Val.set('10')
p4Val.set('10')
p5Val.set('10')
p6Val.set('10')
p7Val.set('10')
p8Val.set('10')

openIcon = PhotoImage(file = r'assets/open_icon.png')
readIcon = PhotoImage(file = r'assets/read_icon.png')
setIcon = PhotoImage(file = r'assets/set_icon.png')
webIcon = PhotoImage(file = r'assets/web_icon.png')
quitIcon = PhotoImage(file = r'assets/quit_icon.png')

openButton = Button(root, image = openIcon, padx = 20, pady = 6, command = import_csv_data).grid(row = 2, column = 0)
readButton = Button(root, image = readIcon, padx = 20, pady = 6, command = firstopen).grid(row = 2, column = 1)
quitButton = Button(root, image = setIcon, padx = 20, pady = 6, command = sysSetting).grid(row = 2, column = 2)
webButton = Button(root, image = webIcon, padx = 20, pady = 6, command = openweb).grid(row = 2, column = 3)
quitButton = Button(root, image = quitIcon, padx = 20, pady = 8, command = sys.exit).grid(row = 2, column = 4)

Label(root, text = '1. Open', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 0)
Label(root, text = '2. Read', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 1)
Label(root, text = 'Setting', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 2)
Label(root, text = 'Help', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 3)
Label(root, text = 'Quit', font = ('Helvetica', 13, 'bold')).grid(row = 3, column = 4)

root.mainloop()
