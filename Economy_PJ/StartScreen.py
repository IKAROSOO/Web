from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from dotenv import load_dotenv
from tkinter import ttk
import pandas as pd
import datetime
import requests
import json
import os
import sys
import tkinter as tk

mpl.rcParams['path.simplify'] = False

# 폰트 설정
def set_korean_font():
    font_name = None
    if sys.platform == "darwin": font_name = 'AppleGothic'
    elif sys.platform == "win32": font_name = 'Malgun Gothic'
    
    if font_name and font_name in [f.name for f in fm.fontManager.ttflist]:
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False
set_korean_font()

# Tk 설정
root = tk.Tk()
root.geometry("1500x900")
root.title("경제 지표 확인")
# 윈도우 최소 크기 제한
root.minsize(900, 600)

contentFrame = tk.Frame(root)
contentFrame.pack(fill='both', expand=True)

# 전역 변수
comboWidgets = []
currencyDict = {}
FRED_API_KEY = ""
URL = {}

# 최대 그래프 칸 제한
MAX_CELLS = 6

def get_grid_size(n):
    if n == 1:
        return 1, 1
    elif n == 2:
        return 1, 2
    elif n <= 4:
        return 2, 2
    else:
        return 2, 3

# Frame 내부를 정리하는 함수
def clearFrame(container):
    for widget in container.winfo_children():
        widget.destroy()

# 마우스 클릭 이벤트 함수
def onClick(number, currencyOptions):
    createLayout(contentFrame, number, currencyOptions)

def createLayout(screen, selection, currencyOptions):
    clearFrame(screen)
    comboWidgets.clear()

    # screen이 창 크기 변경을 받도록 설정
    screen.rowconfigure(0, weight=1)
    screen.columnconfigure(0, weight=1)

    main = tk.Frame(screen, padx=20, pady=20)
    main.grid(row=0, column=0, sticky="nsew")

    main.rowconfigure(0, weight=1)
    main.columnconfigure(0, weight=1)

    grid = tk.Frame(main)
    grid.grid(row=0, column=0, sticky="nsew")

    # 🔥 selection에 따라 grid 크기 결정
    rows, cols = get_grid_size(selection)

    for r in range(rows):
        grid.rowconfigure(r, weight=1)
    for c in range(cols):
        grid.columnconfigure(c, weight=1)

    cells = []

    # 🔥 필요한 grid 개수만 생성
    for i in range(rows * cols):
        r, c = divmod(i, cols)
        cell = tk.Frame(
            grid,
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=10
        )
        cell.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
        cells.append(cell)

    # 🔥 selection 개수만큼만 그래프/콤보 생성
    for i in range(selection):
        cell = cells[i]
        tk.Label(cell, text=f"그래프 {i+1}").pack()
        combo = ttk.Combobox(cell, values=currencyOptions, state="readonly")
        combo.set("선택 안 함")
        combo.pack(pady=5)
        comboWidgets.append(combo)

    # 그래프 생성 버튼
    btn = tk.Button(
        screen,
        text="그래프 생성",
        command=graphDisplay,
        font=("Malgun Gothic", 15, "bold"),
        bg="skyblue"
    )
    btn.grid(sticky="ew", padx=20, pady=10)


def getExchangeList(API_KEY, data):
    URL_LIST = data["FRED_CurrencyList"]
    params = {'category_id': 95, 'api_key': API_KEY, 'file_type': 'json'}
    response = requests.get(URL_LIST, params=params)
    if response.status_code == 200:
        data_json = response.json()
        return {item['title']: item['id'] for item in data_json.get('seriess', [])}
    return {}

def drawGraph(cell, series_id, title):
    clearFrame(cell)

    if series_id.startswith("EX"):
        series_id = "D" + series_id

    # cell 내부를 grid로 분할 (그래프 / 툴바)
    cell.rowconfigure(0, weight=1)
    cell.rowconfigure(1, weight=0)
    cell.columnconfigure(0, weight=1)

    graphFrame = tk.Frame(cell)
    graphFrame.grid(row=0, column=0, sticky="nsew")

    toolbarFrame = tk.Frame(cell)
    toolbarFrame.grid(row=1, column=0, sticky="ew")

    today = datetime.date.today()
    past = (today - datetime.timedelta(days=365*15)).strftime("%Y-%m-%d")

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": past,
        "frequency": "d"
    }

    try:
        res = requests.get(URL['FRED_Exchange'], params=params)
        data = res.json()['observations']

        df = pd.DataFrame(data)[["date", "value"]]
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df.dropna(inplace=True)

        fig = Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(
            df.index,
            df["value"],
            linewidth=0.8,
            marker='.',
            markersize=2
        )
        ax.set_title(title)
        ax.grid(True, linestyle="--", alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, graphFrame)
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.pack(fill="both", expand=True)

        # 그래프 프레임 크기에 맞춰 Figure 리사이즈
        def resize_figure(event):
            w, h = event.width, event.height
            if w > 10 and h > 10:
                fig.set_size_inches(w / fig.dpi, h / fig.dpi)
                canvas.draw_idle()

        graphFrame.bind("<Configure>", resize_figure)

        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

    except Exception as e:
        tk.Label(cell, text=f"오류: {e}").grid(row=0, column=0, sticky="nsew")

def graphDisplay():
    print("--- 3단계 진입: 데이터 수집 및 그래프 생성 ---")
    
    tasks = []

    for combo in comboWidgets:
        if combo.winfo_exists():
            choice = combo.get()
            if choice != '선택 안 함':
                tasks.append((combo.master, currencyDict[choice], choice))
        
    for cell, sid, name in tasks:
        drawGraph(cell, sid, name)

def main():
    global currencyDict, FRED_API_KEY, URL
    current_dir = os.path.dirname(os.path.abspath(__file__))
    url_path = os.path.join(current_dir, 'urls.json')
    env_path = os.path.join(current_dir, 'apikey.env')

    try:
        with open(url_path, 'r', encoding='utf-8') as f: URL = json.load(f)
    except FileNotFoundError: sys.exit(1)
    
    load_dotenv(dotenv_path=env_path)
    FRED_API_KEY = os.getenv("FRED_API")
    
    currencyDict = getExchangeList(FRED_API_KEY, URL)
    currencyList = list(currencyDict.keys()) + ["선택 안 함"]

    btnContainer = tk.Frame(contentFrame)
    btnContainer.pack(pady=20)

    for i in range(1, 7):
        btn = tk.Button(btnContainer, text=str(i), 
                        command=lambda n=i: onClick(n, currencyList), 
                        font=("Malgun Gothic", 20, 'bold'), padx=20, pady=10, width=10)
        btn.pack(side='left', padx=5, pady=20)

    root.mainloop()

if __name__ == '__main__': main()