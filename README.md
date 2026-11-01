# 📚 Student Study Planner

A neon-themed student productivity web application built with **Python,
Streamlit, SQLite, Pandas, and Plotly**. It helps students organize
subjects, manage study tasks, track deadlines, monitor progress, and
explore their study data through an analytics dashboard.

## ✨ Features

### 1. Dashboard

-   View total, completed, and pending tasks.
-   Monitor overall task completion percentage.
-   See upcoming tasks and deadline summaries.
-   View a task distribution chart.

### 2. Manage Subjects

-   Add subjects.
-   View the subject list.
-   Delete a subject and its associated tasks.

### 3. Manage Tasks

-   Create tasks under a subject.
-   Set task deadlines.
-   Mark tasks as completed or pending.
-   Delete tasks.
-   View all tasks in a table.

### 4. My Progress

-   Track completed and pending tasks.
-   View overall completion progress.
-   Compare progress across subjects.

### 5. Data & Analytics

-   View the study-task dataset generated from the planner's SQLite
    database.
-   Inspect dataset dimensions, column names, and data types.
-   View a statistical summary using Pandas.
-   Check for missing values and duplicate rows.
-   Clean duplicate rows and handle missing values in the analytics
    copy.
-   Visualize task status, subject-wise tasks, and deadline
    distribution.
-   Download the original and cleaned datasets as CSV files.

> **Dataset note:** The analytics dataset is created from the subjects
> and tasks entered into the application. It is not an external or
> preloaded student dataset. Add subjects and tasks first to populate
> the analytics page.

## 🛠️ Technology Stack

  Technology   Purpose
  ------------ -------------------------------------------
  Python       Application logic
  Streamlit    Web application interface
  SQLite       Persistent storage for subjects and tasks
  Pandas       Dataset handling, cleaning, and analysis
  Plotly       Interactive data visualizations
  VS Code      Development environment
  GitHub       Source-code hosting and version control

## 📁 Project Structure

``` text
Student-Study-Planner/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Files excluded from Git
└── study_planner.db       # SQLite database (created automatically)
```

The database file is created automatically when the application runs for
the first time. Keep it locally if you want to preserve your saved
subjects and tasks.

## ⚙️ Installation and Setup

### Prerequisites

-   Python 3.9 or later
-   pip
-   Visual Studio Code (recommended)

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL with your GitHub repository URL.

### 2. Create a virtual environment (recommended)

**Windows PowerShell:**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can skip virtual-environment
activation and use `python -m pip` commands directly.

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Run the application

``` bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

``` text
http://localhost:8501
```

Open that URL in your browser.

## 📦 requirements.txt

Create a file named `requirements.txt` containing:

``` text
streamlit
pandas
plotly
```

SQLite is included with Python, so a separate SQLite package is not
required for this application.

## 📊 How to Use

1.  Open **Manage Subjects** and add subjects such as Python, DBMS, or
    Mathematics.
2.  Open **Manage Tasks** and create tasks with a subject and deadline.
3.  Mark tasks as completed when finished.
4.  Visit **Dashboard** and **My Progress** to monitor your study
    activity.
5.  Open **Data & Analytics** to inspect the dataset, review the
    cleaning report, explore charts, and download CSV files.

## 🧹 Data Analytics Workflow

``` text
Study tasks entered by the student
              |
              v
       SQLite database
              |
              v
       Pandas dataset
              |
              v
        Data cleaning
              |
              v
       Data analysis
              |
              v
     Plotly visualizations
              |
              v
         Data insights
```

## 🔮 Future Improvements

-   Add CSV upload to analyze external datasets.
-   Add search and filters for tasks and subjects.
-   Add reminders for approaching deadlines.
-   Add weekly and monthly study reports.
-   Add user authentication and individual student accounts.
-   Add export options for PDF reports.

## 🎓 Project Purpose

This project demonstrates how a practical student productivity
application can combine database management with basic data analysis and
visualization. It is suitable as a small college project and can be
extended with additional features.

## 👨‍💻 Author

**Krish Gupta**

-   GitHub:
    [krishgupta1702-subo.](https://github.com/krishgupta1702-sudo)

------------------------------------------------------------------------

⭐ If you find this project useful, consider giving the repository a
star.
