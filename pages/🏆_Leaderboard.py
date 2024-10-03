import streamlit as st
import pandas as pd
import os
import zipfile
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="🏆 AI Competition Leaderboard", page_icon="🏅")

# Directory where submissions are stored
SUBMISSIONS_DIR = os.path.join(".", "data", "submissions")


def load_submissions() -> pd.DataFrame:
    """
    Load all submissions from the submissions folder into a single DataFrame.

    returns: pd.DataFrame
    description: reads all CSV files in the submissions directory and combines them into one DataFrame
    """
    all_submissions = []

    if os.path.exists(SUBMISSIONS_DIR):
        # Read all CSV files in the submissions folder
        for filename in os.listdir(SUBMISSIONS_DIR):
            if filename.endswith(".csv"):
                filepath = os.path.join(SUBMISSIONS_DIR, filename)
                submission_data = pd.read_csv(filepath)
                all_submissions.append(submission_data)

    # Combine all the submissions into one DataFrame
    if all_submissions:
        combined_df = pd.concat(all_submissions, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame(columns=["Name", "Score", "Submission Time"])


def get_highest_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the highest score for each user from the DataFrame, dynamically counting the number of entries.

    df: pd.DataFrame
    returns: pd.DataFrame
    description: groups by 'Name' and retrieves the highest score and dynamically counts submissions for each user
    """
    # Group by 'Name' and get the maximum score and latest submission time for each user
    highest_scores = df.groupby("Name", as_index=False).agg(
        Score=("Score", "max"),
        Submission_Time=("Submission Time", "max"),  # Get the latest submission time
    )

    # Dynamically count total entries for each user
    highest_scores["Entries"] = df.groupby("Name")["Name"].count().values

    return highest_scores


def create_zip_of_submissions() -> BytesIO:
    """
    Create a zip file containing all the files in the submissions directory.

    returns: BytesIO
    description: compresses all files in the submissions folder into a zip and returns a BytesIO object
    """
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for filename in os.listdir(SUBMISSIONS_DIR):
            if filename.endswith(".csv"):
                filepath = os.path.join(SUBMISSIONS_DIR, filename)
                zf.write(filepath, arcname=filename)

    zip_buffer.seek(0)
    return zip_buffer


def leaderboard_page() -> None:
    """Displays the leaderboard with the highest submission for each user, adds a download button, and enhances the visual effects."""
    st.title("🏆 AI Competition Leaderboard 🏅")

    # Load all submissions from the folder
    leaderboard_df = load_submissions()

    # Show the leaderboard as a table
    if not leaderboard_df.empty:
        highest_scores_df = get_highest_scores(leaderboard_df)
        highest_scores_df = highest_scores_df.sort_values(
            by="Score", ascending=False
        )  # Sort by score

        # Display the top 3 players' names above the table
        top_3 = highest_scores_df.head(3)
        st.markdown("### 🌟 Top 3 Competitors 🌟")
        for i, row in top_3.iterrows():
            st.markdown(f"**{row['Name']}** — F1 Score: {row['Score']:.2f}")

        # Trigger balloons effect for fun!
        st.balloons()

        # Display the leaderboard in a table format
        st.subheader("Leaderboard Table")
        st.dataframe(highest_scores_df)

        # Display feedback for the top scorer
        top_scorer = highest_scores_df.iloc[0]
        st.markdown(
            f"**Top Scorer:** {top_scorer['Name']} with an F1 score of {top_scorer['Score']:.2f}, total entries: {top_scorer['Entries']}!"
        )

        # Add a button to download all submissions as a zip file
        if st.button("Download All Submissions as ZIP"):
            zip_buffer = create_zip_of_submissions()
            st.download_button(
                label="Download ZIP",
                data=zip_buffer,
                file_name="submissions.zip",
                mime="application/zip",
            )
    else:
        st.info(
            "No submissions yet. Be the first to conquer the leaderboard and win the title!"
        )
    st.write("""
             ### Leaderboard Evaluation

The leaderboard ranks submissions based on their **Weighted F1 Score**, which takes into account the precision and recall for each class and adjusts the score based on class distribution. This means that your model's performance across all digit classes will be considered, giving more weight to classes with a higher number of examples.

We use the `f1_score(y_true, y_pred, average='weighted')` from `scikit-learn` to evaluate your submission. Make sure your model performs well across all digits to climb to the top!
             """)


# Call the leaderboard page function
leaderboard_page()
