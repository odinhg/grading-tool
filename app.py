import streamlit as st
import yaml
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--task_dir", type=str, default="tasks", help="Directory containing task YAML files"
)
args = parser.parse_args()

# Load tasks from YAML files
tasks = {}
for task_file in pathlib.Path(args.task_dir).glob("*.yaml"):
    with open(task_file, "r") as f:
        task = yaml.safe_load(f)
        tasks[task["title"]] = task

task_names = list(tasks.keys())

# Streamlit setup
st.set_page_config(layout="wide")
st.title("🎓 Cool Grading Tool")
st.markdown(
    """
    <style>
           .block-container {
               padding-top: 2.4rem;
               padding-bottom: 0rem;
            }
    </style>
    """,
    unsafe_allow_html=True,
)


task_name = st.selectbox("**Select task**", task_names, key="task_name")
task = tasks[task_name]

with st.form("grading_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"### {task_name} – {task['subtitle']}")
    with col2:
        with st.expander("**See question**"):
            st.markdown(task["question"])
    with col3:
        with st.expander("**See grading instructions**"):
            st.write(task["grading_instructions"])

    st.write("#### 📝 Grading criteria")
    results = []
    columns = st.columns(len(task["criteria"]))
    for i, criterion in enumerate(task["criteria"]):
        with columns[i]:
            st.write(f"###### {i+1:02}. {criterion['title']}")
            score = st.number_input(
                f"**Score** (out of {criterion['max_score']})",
                min_value=0.0,
                max_value=float(criterion["max_score"]),
                step=float(criterion["step"]),
                key=f"score_{i}",
            )
            custom_reason = st.text_area(
                "**Custom reasons (one per line)**", key=f"reason_{i}", height=80
            )
            template_reasons = st.pills(
                "**Template reasons to add**",
                criterion["reasons"],
                key=f"reasons_{i}",
                selection_mode="multi",
                format_func=lambda x: x,
            )
            st.markdown(criterion["description"])
            results.append(
                {
                    "title": criterion["title"],
                    "score": score,
                    "max_score": criterion["max_score"],
                    "reasons": custom_reason.splitlines() + template_reasons,
                }
            )

    submitted = st.form_submit_button(
        "Generate Report", icon="🚀", use_container_width=True
    )

    if submitted:
        total_score = min(
            sum([result["score"] for result in results]), task["max_score"]
        )
        st.markdown(
            f"**Total Score: {total_score}** (out of {tasks[task_name]['max_score']})"
        )
        st.write("#### Grading Notes\nClick upper right corner to copy to clipboard.")
        note_string = "Criteria:\n\n"
        for result in results:
            note_string += f"- {result['title']}: {result['score']} (out of {result['max_score']})\n"
            for reason in result["reasons"]:
                if reason:
                    note_string += f"\t- {reason}\n"
        note_string += (
            f"\nTotal Score: {total_score} (out of {tasks[task_name]['max_score']})"
        )
        st.code(note_string, language=None)
