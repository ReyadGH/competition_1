import streamlit as st
import pandas as pd
import os
from datetime import datetime
from sklearn.metrics import f1_score
import pytz

# set up the page configuration
st.set_page_config(page_title="Submit Your Predictions", page_icon="📤")

SUBMISSIONS_DIR = os.path.join(".", "data", "submissions")
if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

# saudi time zone (utc+3)
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

y_true = st.secrets["Y_TRUE"]

REQUIRED_LENGTH = len(y_true)


def process_submission(name: str, file) -> None:
    """
    process the uploaded file, validate it, and calculate the f1 score.

    name: str
    file: UploadedFile
    """
    try:
        # load the submitted csv file
        data = pd.read_csv(file)

        # ensure proper format and row count
        if list(data.columns) == ["index", "target"] and len(data) == REQUIRED_LENGTH:
            y_pred = data[
                "target"
            ]  # we're now using the 'target' column as the predictions

            # calculate the f1 score using weighted average to handle unbalanced data
            score = f1_score(y_true, y_pred, average="weighted")

            saudi_time = datetime.now(SAUDI_TZ).strftime("%Y-%m-%d_%H-%M-%S")
            submission_filename = f"{name}_{saudi_time}.csv"
            submission_filepath = os.path.join(SUBMISSIONS_DIR, submission_filename)

            # save submission with score and time
            submission_data = pd.DataFrame(
                {
                    "Name": [name],
                    "target": [list(y_pred)],
                    "Score": [score],
                    "Submission Time": [saudi_time],
                }
            )
            submission_data.to_csv(submission_filepath, index=False)

            st.success(
                f"thanks {name}, your submission has been processed! your f1 score is {score:.2f}."
            )
        else:
            st.error(
                f"invalid file format. we need columns 'index' and 'target' with exactly {REQUIRED_LENGTH} rows."
            )
    except Exception as e:
        st.error(f"error processing file: {e}")


def submission_page() -> None:
    """
    handles the submission form, where users enter their name and upload a csv.
    """
    st.title("submit your predictions")

    st.write("""
        here's what you need to do:
        
        1. enter your name.
        2. upload a csv with two columns: **index** and **target**.
        3. the file should have exactly the right number of rows to match the true values.
        
        we'll calculate your f1 score once you hit submit!
    """)

    name = st.text_input("enter your name")
    uploaded_file = st.file_uploader("choose your csv file", type=["csv"])

    if st.button("submit"):
        if name and uploaded_file:
            process_submission(name, uploaded_file)
        else:
            st.error("please provide both your name and a valid file!")
    st.write("""
             ### Leaderboard Evaluation

The leaderboard ranks submissions based on their **Weighted F1 Score**, which takes into account the precision and recall for each class and adjusts the score based on class distribution. This means that your model's performance across all digit classes will be considered, giving more weight to classes with a higher number of examples.

We use the `f1_score(y_true, y_pred, average='weighted')` from `scikit-learn` to evaluate your submission. Make sure your model performs well across all digits to climb to the top!
             """)


# run the submission page
submission_page()
