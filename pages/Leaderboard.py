import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Leaderboard", page_icon="🏅")

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


def leaderboard_page() -> None:
    """Displays the leaderboard with the highest submission for each user"""
    st.title("🏅 Leaderboard")

    # Load all submissions from the folder
    leaderboard_df = load_submissions()

    # Show only highest score per user and total number of entries
    if not leaderboard_df.empty:
        highest_scores_df = get_highest_scores(leaderboard_df)
        highest_scores_df = highest_scores_df.sort_values(
            by="Score", ascending=False
        )  # Sort by score
        st.table(highest_scores_df)

        # Display feedback for the top scorer
        top_scorer = highest_scores_df.iloc[0]
        st.markdown(
            f"**Top Scorer:** {top_scorer['Name']} with a score of {top_scorer['Score']:.2f}, total entries: {top_scorer['Entries']}!"
        )
    else:
        st.write("No submissions yet. Be the first to conquer the leaderboard!")


# Call the leaderboard page function
leaderboard_page()
