# 🏎️ ApexTelemetry – F1 Telemetry & Lap Performance Analyzer

A data-driven Formula 1 analytics dashboard built using Python and Streamlit to explore racing performance through real-world session data.

ApexTelemetry helps users compare driver performance, analyse lap times, and visualize speed telemetry using data from the OpenF1 API.

## 🚀 Features

- **F1 Session Selection:** Explore Formula 1 sessions by year, country, and session type.
- **Driver Performance Comparison:** Compare average and best lap times across drivers.
- **Lap Time Analysis:** Visualize driver lap-time performance.
- **Head-to-Head Comparison:** Compare two selected drivers across common lap numbers.
- **Speed Telemetry Visualization:** Analyse a selected driver's speed data over time.
- **Interactive Dashboard:** Explore session information and performance data through Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Requests | API communication |
| OpenF1 API | Formula 1 session and telemetry data |

## 📂 Project Structure

```text
ApexTelemetry/
│
├── assets/
│   └── driver_comparison.png
│
├── data/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── telemetry.py
│   └── speed_analysis.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/kalyaniikadam/ApexTelemetry.git
```

### 2. Navigate to the project folder

```bash
cd ApexTelemetry
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
.\venv\Scripts\Activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run main.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 📡 Data Source

This project uses the [OpenF1 API](https://openf1.org/) to retrieve Formula 1 session, lap, driver, and car telemetry data.

## 🎯 Project Objective

The objective of ApexTelemetry is to explore how data analytics and visualization can help understand Formula 1 racing performance.

It also provides practical experience with API integration, Python programming, data processing, and interactive dashboard development.

## 🔮 Future Improvements

- Sector-wise lap time analysis
- Tire strategy visualization
- Interactive circuit maps
- More advanced driver comparisons
- Historical race performance analysis

## 👩‍💻 Developed By

**Kalyani Kadam**

Computer Science and Engineering

[GitHub](https://github.com/kalyaniikadam)

[Email](mailto:kadamkalyanii01@gmail.com)

---

*Built with Python, data, and a passion for Formula 1.* 🏁