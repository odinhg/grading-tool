# Grading Tool

A simple grading tool based on Python and Streamlit.

## How to Run

Simply run the following command in the terminal and the tool will open in your browser (or you can copy the URL and paste it in your browser).

```bash
streamlit run app.py
```

## How to Use

1. Add tasks and grading criteria in a YAML file (see below).
2. Open the tool and select a task to grade.
3. Set scores and add reasoning for each grading criterion.
4. Click "Generate Report" to generate a report for the task that you can copy and paste into your grading document/platform.

## Adding Tasks and Grading Criteria

You can add tasks/questions and corresponding grading criteria as a YAML file. Take a look at the file `my_tasks.yaml` in the `tasks` directory for an example.


By default, the tools looks for all YAML files in the `tasks` directory. You can specify a different directory by using the `--tasks-dir` option.

```bash
streamlit run app.py -- --tasks-dir my_tasks_dir
```

