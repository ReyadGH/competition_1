import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz  # For time zone conversion

# Set page configuration
st.set_page_config(page_title="Submit Your Targets", page_icon="📤")

# Directory to save the submissions
SUBMISSIONS_DIR = os.path.join(".", "data", "submissions")
if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)  # Create the folder if it doesn't exist

# Saudi Arabian time zone (UTC+3)
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

# Secret array used for validation/scoring
SECRET_ARRAY = [75, 90, 85, 60, 95]

# Fixed length of the dataframe required
REQUIRED_LENGTH = 5  # You can adjust this value


def calculate_score(target: int, secret_array: list[int]) -> int:
    """
    Calculate the score based on the target and the secret array.

    target: int
    secret_array: list[int]
    returns: int
    description: computes the score based on the secret array logic
    """
    score = sum(1 for x in secret_array if target >= x)
    return (score / len(secret_array)) * 100


def process_submission(name: str, file) -> None:
    """
    Process the CSV file and add validated scores to the leaderboard.

    name: str
    file: UploadedFile
    description: validates the file, saves submission, and logs the result
    """
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(file)

        # Check if the CSV contains the required headers and length
        if (
            list(data.columns)
            == [
                "index",
                "target",
            ]
            and len(data) == REQUIRED_LENGTH
        ):
            total_score = 0
            for index, row in data.iterrows():
                target = row["target"]
                score = calculate_score(target, SECRET_ARRAY)
                total_score += score

            # Calculate average score
            average_score = total_score / REQUIRED_LENGTH

            # Get current time in Saudi Arabian time zone
            saudi_time = datetime.now(SAUDI_TZ).strftime("%Y-%m-%d_%H-%M-%S")
            submission_filename = f"{name}_{saudi_time}.csv"
            submission_filepath = os.path.join(SUBMISSIONS_DIR, submission_filename)

            submission_data = pd.DataFrame(
                {
                    "Name": [name],
                    "Entries": [REQUIRED_LENGTH],
                    "Score": [average_score],
                    "Submission Time": [saudi_time],
                }
            )
            submission_data.to_csv(submission_filepath, index=False)

            st.success(
                f"Thank you {name}, your submission has been processed with an average score of {average_score:.2f}!"
            )
        else:
            st.error(
                f"Invalid CSV format. Ensure the file contains 'index' and 'target' columns and exactly {REQUIRED_LENGTH} rows."
            )
    except Exception as e:
        st.error(f"Error processing file: {e}")


def submission_page() -> None:
    """Displays the submission form for students to upload their names and targets"""
    st.title("Submit Your Targets")

    # Explanatory text
    st.write("""
        Please follow the instructions below to submit your targets:
        
        1. Enter your name.
        2. Upload a CSV file with the following format:
           - The CSV file must contain exactly two columns: **index** and **target**.
           - The file must contain exactly 5 rows (you can change this requirement).
        
        The system will validate your file and calculate your score based on the targets provided.
    """)

    # Input for name
    name = st.text_input("Enter your name")

    # CSV file uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Submit button
    if st.button("Submit"):
        if name and uploaded_file:
            process_submission(name, uploaded_file)
        else:
            st.error(
                "Please make sure you have entered your name and uploaded a valid CSV file."
            )


# Call the submission page function
submission_page()
