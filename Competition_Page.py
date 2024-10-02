import streamlit as st

st.set_page_config(page_title="AI Competition Week", page_icon="🔥")


def main_page() -> None:
    """Displays the main page with a welcome message"""
    st.title("🔥 End-of-Week AI Competition 🔥")
    st.write("""
        Welcome to the ultimate **End-of-Week AI Competition**!
        Put your skills to the test and compete against your peers. Submit your results,
        climb the leaderboard, and claim the glory of victory. Remember, only the best can reach the top! 🎯
    """)
    st.image(
        "https://example.com/competition-banner.jpg"
    )  # Example image to enhance engagement
    st.markdown("### 🏆 Good luck, and may the best AI win!")


# Call the main page function
main_page()
