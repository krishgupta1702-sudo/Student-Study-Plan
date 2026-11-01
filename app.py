
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Student Study Planner",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# 2. NEON CSS
# =====================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080B16, #101426);
    color: #F8FAFF;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11162B, #17152D);
    border-right: 1px solid #292E55;
}

.main-title {
    font-size: 38px;
    font-weight: 850;
    color: #00F5FF;
    text-shadow: 0 0 14px #00F5FF80;
}

.subtitle {
    color: #A5B4D4;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(145deg, #171E39, #11172B);
    border: 1px solid #00E5FF70;
    border-radius: 16px;
    padding: 20px;
    min-height: 135px;
    box-shadow: 0 0 12px #00E5FF20;
}

.metric-card:hover {
    border-color: #00F5FF;
    box-shadow: 0 0 20px #00E5FF60;
}

.metric-label {
    color: #B5C5E9;
    font-size: 13px;
}

.metric-value {
    color: #00F5FF;
    font-size: 32px;
    font-weight: 850;
    margin-top: 10px;
    text-shadow: 0 0 10px #00F5FF70;
}

div[data-testid="stForm"] {
    background: #141A30;
    padding: 20px;
    border: 1px solid #8B5CF680;
    border-radius: 15px;
}

.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(90deg, #6D28D9, #2563EB);
    color: white;
    border: 1px solid #A78BFA;
    border-radius: 10px;
    font-weight: bold;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(90deg, #9333EA, #06B6D4);
    box-shadow: 0 0 15px #00F5FF70;
    color: white;
}

[data-testid="stMetricValue"] {
    color: #00F5FF;
}

[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #9333EA, #00F5FF);
}

h1, h2, h3 {
    color: #F8FAFF;
}

hr {
    border-color: #343B65;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE
# =====================================================

conn = sqlite3.connect(
    "study_planner.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject_id INTEGER,
    deadline TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")

conn.commit()


# =====================================================
# 4. DATABASE FUNCTIONS
# =====================================================

def get_subjects():
    return pd.read_sql_query(
        "SELECT * FROM subjects ORDER BY name",
        conn
    )


def get_tasks():
    return pd.read_sql_query("""
        SELECT
            tasks.id,
            tasks.title,
            subjects.name AS subject,
            tasks.deadline,
            tasks.completed
        FROM tasks
        LEFT JOIN subjects
        ON tasks.subject_id = subjects.id
        ORDER BY tasks.deadline
    """, conn)


def metric_card(icon, label, value):
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:25px">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def neon_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8E9FF"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    return fig


# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        "<h2 style='color:#00F5FF'>🎓 Study Planner</h2>",
        unsafe_allow_html=True
    )

    st.caption("YOUR PERSONAL STUDY ASSISTANT")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Manage Subjects",
            "Manage Tasks",
            "My Progress",
            "Data & Analytics"
        ]
    )

    st.divider()

    st.markdown("### 📚 Student Study Planner")
    st.caption("Version 4.0")
    st.caption("Python + Streamlit + SQLite + Pandas + Plotly")


# =====================================================
# 6. COMMON DATA
# =====================================================

subjects = get_subjects()
tasks = get_tasks()

today = date.today()
today_string = today.isoformat()

total = len(tasks)
completed = int(tasks["completed"].sum()) if total else 0
pending = total - completed

percentage = completed / total * 100 if total else 0


# =====================================================
# 7. HEADER
# =====================================================

st.markdown(
    '<div class="main-title">📚 Student Study Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Organize your studies, manage deadlines and track your progress.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 8. DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("## 📊 Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("📋", "TOTAL TASKS", total)

    with c2:
        metric_card("✅", "COMPLETED", completed)

    with c3:
        metric_card("⏳", "PENDING", pending)

    with c4:
        metric_card("📈", "COMPLETION", f"{percentage:.1f}%")

    st.divider()

    st.markdown("## 🎯 Overall Study Progress")

    st.progress(int(percentage))

    st.caption(
        f"You completed {completed} out of {total} tasks."
    )

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown("### 📅 Upcoming Tasks")

        if total:

            upcoming = tasks[
                (tasks["completed"] == 0) &
                (tasks["deadline"] >= today_string)
            ].head(5)

            if not upcoming.empty:
                st.dataframe(
                    upcoming[["title", "subject", "deadline"]],
                    width="stretch",
                    hide_index=True
                )
            else:
                st.success("No upcoming pending tasks!")

        else:
            st.info("Add subjects and tasks to get started.")

    with right:

        st.markdown("### ⏰ Deadline Summary")

        overdue = len(tasks[
            (tasks["completed"] == 0) &
            (tasks["deadline"] < today_string)
        ])

        due_today = len(tasks[
            (tasks["completed"] == 0) &
            (tasks["deadline"] == today_string)
        ])

        due_soon = len(tasks[
            (tasks["completed"] == 0) &
            (tasks["deadline"] > today_string) &
            (tasks["deadline"] <=
             (today + timedelta(days=7)).isoformat())
        ])

        st.error(f"🔴 Overdue: {overdue}")
        st.warning(f"🟡 Due Today: {due_today}")
        st.success(f"🟢 Due in 7 Days: {due_soon}")

    st.divider()

    st.markdown("### 📊 Task Distribution")

    if total:

        df = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [completed, pending]
        })

        fig = px.pie(
            df,
            names="Status",
            values="Count",
            hole=0.6,
            color="Status",
            color_discrete_map={
                "Completed": "#00F5FF",
                "Pending": "#FF4DDB"
            }
        )

        st.plotly_chart(neon_chart(fig), width="stretch")

    else:
        st.info("Your charts will appear after adding tasks.")


# =====================================================
# 9. MANAGE SUBJECTS
# =====================================================

elif page == "Manage Subjects":

    st.markdown("## 📖 Manage Subjects")

    with st.form("subject_form"):

        subject_name = st.text_input(
            "Subject Name",
            placeholder="Example: Python Programming"
        )

        submitted = st.form_submit_button(
            "➕ Add Subject",
            width="stretch"
        )

        if submitted:

            if subject_name.strip():

                try:
                    cursor.execute(
                        "INSERT INTO subjects (name) VALUES (?)",
                        (subject_name.strip(),)
                    )

                    conn.commit()
                    st.success("Subject added successfully!")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Subject already exists.")

            else:
                st.warning("Enter a subject name.")

    st.divider()

    subjects = get_subjects()

    st.markdown("### Your Subjects")

    st.metric("Total Subjects", len(subjects))

    if not subjects.empty:

        st.dataframe(
            subjects,
            width="stretch",
            hide_index=True
        )

        delete_subject = st.selectbox(
            "Select subject to delete",
            subjects["name"].tolist()
        )

        if st.button("🗑️ Delete Subject"):

            subject_id = int(
                subjects.loc[
                    subjects["name"] == delete_subject,
                    "id"
                ].iloc[0]
            )

            cursor.execute(
                "DELETE FROM tasks WHERE subject_id = ?",
                (subject_id,)
            )

            cursor.execute(
                "DELETE FROM subjects WHERE id = ?",
                (subject_id,)
            )

            conn.commit()
            st.success("Subject and its tasks deleted.")
            st.rerun()

    else:
        st.info("No subjects available.")


# =====================================================
# 10. MANAGE TASKS
# =====================================================

elif page == "Manage Tasks":

    st.markdown("## 📝 Manage Tasks")

    subjects = get_subjects()

    if subjects.empty:

        st.warning("Please add a subject first.")

    else:

        subject_options = dict(
            zip(subjects["name"], subjects["id"])
        )

        with st.form("task_form"):

            title = st.text_input(
                "Task Title",
                placeholder="Complete Python Assignment"
            )

            selected_subject = st.selectbox(
                "Select Subject",
                list(subject_options.keys())
            )

            deadline = st.date_input(
                "Deadline",
                value=date.today(),
                min_value=date.today()
            )

            submitted = st.form_submit_button(
                "➕ Create Task",
                width="stretch"
            )

            if submitted:

                if title.strip():

                    cursor.execute("""
                        INSERT INTO tasks
                        (title, subject_id, deadline)
                        VALUES (?, ?, ?)
                    """, (
                        title.strip(),
                        subject_options[selected_subject],
                        deadline.isoformat()
                    ))

                    conn.commit()
                    st.success("Task created successfully!")
                    st.rerun()

                else:
                    st.warning("Enter a task title.")

    st.divider()

    st.markdown("### 📋 All Tasks")

    tasks = get_tasks()

    if not tasks.empty:

        display = tasks.copy()

        display["Status"] = display["completed"].map({
            0: "⏳ Pending",
            1: "✅ Completed"
        })

        st.dataframe(
            display[["id", "title", "subject", "deadline", "Status"]],
            width="stretch",
            hide_index=True
        )

        st.markdown("### Update Task Status")

        options = {
            f"{row['title']} (ID: {row['id']})": row["id"]
            for _, row in tasks.iterrows()
        }

        selected_task = st.selectbox(
            "Select Task",
            list(options.keys())
        )

        task_id = options[selected_task]

        task_status = int(
            tasks.loc[tasks["id"] == task_id, "completed"].iloc[0]
        )

        if task_status == 0:

            if st.button("✅ Mark as Completed"):
                cursor.execute(
                    "UPDATE tasks SET completed = 1 WHERE id = ?",
                    (task_id,)
                )

                conn.commit()
                st.success("Task completed!")
                st.rerun()

        else:

            if st.button("↩️ Mark as Pending"):
                cursor.execute(
                    "UPDATE tasks SET completed = 0 WHERE id = ?",
                    (task_id,)
                )

                conn.commit()
                st.success("Task marked as pending.")
                st.rerun()

        if st.button("🗑️ Delete Selected Task"):

            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

            conn.commit()
            st.success("Task deleted.")
            st.rerun()

    else:
        st.info("No tasks available.")


# =====================================================
# 11. MY PROGRESS
# =====================================================

elif page == "My Progress":

    st.markdown("## 📈 My Study Progress")

    if total:

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Completed Tasks", completed)

        with col2:
            st.metric("Pending Tasks", pending)

        st.markdown(f"### Completion: {percentage:.1f}%")

        st.progress(int(percentage))

        st.divider()

        subject_progress = tasks.groupby(
            "subject"
        ).agg(
            Total=("id", "count"),
            Completed=("completed", "sum")
        ).reset_index()

        subject_progress["Progress (%)"] = (
            subject_progress["Completed"] /
            subject_progress["Total"] * 100
        ).round(1)

        fig = px.bar(
            subject_progress,
            x="subject",
            y="Progress (%)",
            color="subject",
            range_y=[0, 100],
            text="Progress (%)",
            title="Subject-wise Progress",
            color_discrete_sequence=[
                "#00F5FF", "#A855F7",
                "#FF4DDB", "#39FF9C"
            ]
        )

        fig.update_layout(showlegend=False)

        st.plotly_chart(neon_chart(fig), width="stretch")

        st.dataframe(
            subject_progress,
            width="stretch",
            hide_index=True
        )

    else:
        st.info("Add tasks to see your progress.")


# =====================================================
# 12. DATA & ANALYTICS
# =====================================================

elif page == "Data & Analytics":

    st.markdown("## 📊 Dataset & Analytics")

    st.caption(
        "Explore, clean, analyze and visualize your study data."
    )

    # DATASET

    raw_data = get_tasks()

    if raw_data.empty:

        st.warning(
            "Your dataset is empty. Please add subjects and tasks "
            "from Manage Subjects and Manage Tasks."
        )

        st.info(
            "Once you add tasks, dataset information, cleaning "
            "and visualization will appear here."
        )

    else:

        # DATASET INFORMATION

        st.markdown("### 📁 Dataset Information")

        a, b, c, d = st.columns(4)

        with a:
            metric_card("📋", "TOTAL RECORDS", len(raw_data))

        with b:
            metric_card("📊", "TOTAL COLUMNS", len(raw_data.columns))

        with c:
            metric_card(
                "✅", "COMPLETED",
                int(raw_data["completed"].sum())
            )

        with d:
            metric_card(
                "⏳", "PENDING",
                int((raw_data["completed"] == 0).sum())
            )

        st.divider()

        # DATASET PREVIEW

        st.markdown("### 🗂️ Dataset Preview")

        st.dataframe(
            raw_data,
            width="stretch",
            hide_index=True
        )

        csv_data = raw_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Dataset CSV",
            data=csv_data,
            file_name="student_study_dataset.csv",
            mime="text/csv",
            width="stretch"
        )

        st.divider()

        # DATA INFORMATION

        st.markdown("### 🔍 Data Information")

        info1, info2 = st.columns(2)

        with info1:

            st.markdown("#### Dataset Shape")

            st.write(f"Rows: {raw_data.shape[0]}")
            st.write(f"Columns: {raw_data.shape[1]}")

            st.markdown("#### Column Names")

            for col in raw_data.columns:
                st.write(f"• {col}")

        with info2:

            st.markdown("#### Data Types")

            types = pd.DataFrame({
                "Column": raw_data.columns,
                "Data Type": raw_data.dtypes.astype(str).values
            })

            st.dataframe(
                types,
                width="stretch",
                hide_index=True
            )

        st.markdown("#### Statistical Summary")

        st.dataframe(
            raw_data.describe(include="all").fillna("-"),
            width="stretch"
        )

        st.divider()

        # DATA CLEANING

        st.markdown("### 🧹 Data Cleaning")

        cleaned_data = raw_data.copy()

        missing_before = int(
            cleaned_data.isnull().sum().sum()
        )

        duplicates_before = int(
            cleaned_data.duplicated().sum()
        )

        clean1, clean2, clean3 = st.columns(3)

        with clean1:
            st.metric("Missing Values", missing_before)

        with clean2:
            st.metric("Duplicate Rows", duplicates_before)

        with clean3:
            st.metric("Rows Before Cleaning", len(cleaned_data))

        # Clean column names and duplicates

        cleaned_data.columns = (
            cleaned_data.columns.str.strip().str.lower()
        )

        cleaned_data = cleaned_data.drop_duplicates()

        # Handle missing values

        for col in cleaned_data.columns:

            if cleaned_data[col].isnull().any():

                if pd.api.types.is_numeric_dtype(cleaned_data[col]):
                    cleaned_data[col] = cleaned_data[col].fillna(
                        cleaned_data[col].median()
                    )
                else:
                    cleaned_data[col] = cleaned_data[col].fillna(
                        "Unknown"
                    )

        st.success("Data cleaning process completed.")

        st.write(
            f"Rows after cleaning: **{len(cleaned_data)}**"
        )

        st.write(
            f"Duplicates removed: **{duplicates_before}**"
        )

        st.write(
            f"Missing values handled: **{missing_before}**"
        )

        with st.expander("View Cleaned Dataset"):

            st.dataframe(
                cleaned_data,
                width="stretch",
                hide_index=True
            )

        cleaned_csv = cleaned_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Cleaned Dataset",
            data=cleaned_csv,
            file_name="cleaned_study_dataset.csv",
            mime="text/csv"
        )

        st.divider()

        # DATA VISUALIZATION

        st.markdown("### 📈 Data Visualization")

        # PIE CHART

        st.markdown("#### 1. Task Completion Distribution")

        status_df = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [
                int(cleaned_data["completed"].sum()),
                int((cleaned_data["completed"] == 0).sum())
            ]
        })

        fig1 = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.55,
            color="Status",
            color_discrete_map={
                "Completed": "#00F5FF",
                "Pending": "#FF4DDB"
            }
        )

        st.plotly_chart(neon_chart(fig1), width="stretch")

        # BAR CHART

        st.markdown("#### 2. Subject-wise Task Analysis")

        subject_data = cleaned_data.groupby(
            "subject"
        ).agg(
            Completed=("completed", "sum"),
            Total=("id", "count")
        ).reset_index()

        subject_data["Pending"] = (
            subject_data["Total"] - subject_data["Completed"]
        )

        fig2 = px.bar(
            subject_data,
            x="subject",
            y=["Completed", "Pending"],
            barmode="group",
            color_discrete_map={
                "Completed": "#00F5FF",
                "Pending": "#FF4DDB"
            }
        )

        fig2.update_layout(
            xaxis_title="Subject",
            yaxis_title="Number of Tasks"
        )

        st.plotly_chart(neon_chart(fig2), width="stretch")

        # HISTOGRAM

        st.markdown("#### 3. Task Distribution Histogram")

        fig3 = px.histogram(
            cleaned_data,
            x="deadline",
            color="completed",
            nbins=10,
            color_discrete_map={
                0: "#FF4DDB",
                1: "#00F5FF"
            },
            labels={
                "completed": "Completion Status",
                "deadline": "Deadline"
            }
        )

        st.plotly_chart(neon_chart(fig3), width="stretch")

        # DATA INSIGHTS

        st.divider()

        st.markdown("### 💡 Data Insights")

        completion_rate = (
            cleaned_data["completed"].mean() * 100
        )

        st.info(
            f"Overall task completion rate: "
            f"{completion_rate:.1f}%"
        )

        if not subject_data.empty:

            best = subject_data.loc[
                subject_data["Completed"].idxmax(),
                "subject"
            ]

            st.success(
                f"Subject with the most completed tasks: {best}"
            )

        st.caption(
            "Analytics generated using Pandas and Plotly."
        )


# =====================================================
# 13. FOOTER
# =====================================================

st.divider()

st.caption(
    "📚 Student Study Planner | "
    "Developed using Python, Streamlit, SQLite, Pandas and Plotly"
)
