import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Competition Week", page_icon="🔥")


# Page Title
st.title("🚀 Welcome to the Weekly AI Challenge!")

# Exciting Description
st.write(f"""
**Get ready for this week's epic AI battle!** 🧠✨ Your mission is to build a model that can accurately predict the handwritten digits. You'll train your model using the provided training data and upload your predictions based on the test data.

### Dataset Problem Description:
This week's challenge involves a dataset of handwritten digits, where each image represents a digit between 0 and 9. Your task is to build a model that accurately classifies these digits. The goal is to train your model using the provided training data and submit your predictions based on the test data.

You can use either traditional machine learning algorithms or artificial neural networks (ANN) to solve the problem. However, advanced models like convolutional neural networks (CNNs) are not allowed.


### Here's how it works:
1. **Download the training dataset** using [this link]({st.secrets['LINK_TRAIN']}) to train your model.
2. **Download the test dataset** using [this link]({st.secrets['LINK_TEST']}) where you'll make your predictions.
3. **Fill in your predictions** in the required format: `index, target`, and submit them to see how high you can climb on the leaderboard!



⚠️ **Important:** Since the platform is in beta, make sure to save your submissions locally—just in case!
""")

# Example Submission File
example_data = pd.DataFrame({"index": [0, 1, 2, 3], "target": [7, 2, 1, 0]})

# Create CSV download button for example submission
csv = example_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📝 Download Example Submission",
    data=csv,
    file_name="example_submission.csv",
    mime="text/csv",
)

st.write("""
### Leaderboard Evaluation

The leaderboard ranks submissions based on their **Weighted F1 Score**, which takes into account the precision and recall for each class and adjusts the score based on class distribution. This means that your model's performance across all digit classes will be considered, giving more weight to classes with a higher number of examples.

We use the `f1_score(y_true, y_pred, average='weighted')` from `scikit-learn` to evaluate your submission. Make sure your model performs well across all digits to climb to the top!
         """)

# Additional description
st.write(
    "⚡ Ready to take on the challenge? Fill the test data with your predictions, and submit it to see how high you can climb on the leaderboard! 🏆"
)
