# Import libraries and modules
# Run pip install gradio and essential_generators in terminal
import gradio as gr
import pandas as pd
from essential_generators import DocumentGenerator
from main import generate_dfa

# DataFrame
words = []
with open("words.txt") as file:
    words = file.read().splitlines()
    words = [word.strip() for word in words]

    df = pd.DataFrame(
        {
            "Words": words,
        }
    )

# DFA function call
dfa = generate_dfa(words)


# Generate examples
def generateExamples():
    gen = DocumentGenerator()
    examples = []
    for i in range(3):
        examples.append(gen.paragraph())
    return examples


# Color match function
def color_match(text: gr.Textbox):
    colored_text = []
    pointer = 0

    # Get the result of the DFA check on the input text
    match_dict = dfa.check(text)

    if not match_dict:
        return (
            '<div style="background-color: #dc2626; color: #fff; text-align: center; width: 100%; padding: 10px; font-weight:800; font-size:1.5rem">Rejected</div>',
            None,
            None,
        )

    # Flatten the match_dict into a list of tuples and sort by the start index
    matches = sorted(
        (start, end, word)
        for word, indices in match_dict.items()
        for start, end in indices
    )

    for start, end, word in matches:
        colored_text.append(text[pointer:start])
        # End need to be incremented by 1 to include the last character
        colored_text.append(f"<span style='color:#4ade80'>{text[start:end + 1]}</span>")
        # Move the pointer to the end of the match
        pointer = end + 1

    # Add remaining text
    colored_text.append(text[pointer:])
    # Combine the strings
    colored_text = "".join(colored_text)

    # Call getPositions function and get the DataFrame
    positions_df = getPositions(text)

    return colored_text, positions_df


# Get positions function
def getPositions(text):
    match_dict = dfa.check(text)
    positions_df = pd.DataFrame(columns=["Words", "Positions", "Occurences"])
    for word, positions in match_dict.items():
        # Convert the list of tuples to a string
        positions_str = ", ".join(map(str, positions))
        # Store the word and the positions string in the wordPositions dictionary
        positions_df.loc[len(positions_df)] = [word, positions_str, len(positions)]

    return positions_df


# Search and display function
def search_and_display(search_query):
    # Filter the DataFrame based on the search query
    filtered_df = df[df["Words"].str.contains(search_query)]
    return filtered_df


def text_change_search(text: gr.Textbox):
    if text == "":
        return gr.update(interactive=False)
    else:
        return gr.update(interactive=True)


def text_change_test(text: gr.Textbox):
    if text == "":
        return gr.update(interactive=False), gr.update(interactive=False)
    else:
        return gr.update(interactive=True), gr.update(interactive=True)


def remove_output(result, position):
    return None, None


# CSS styling
# css = """
# warning {background-color: #FFCCCB}
# .feedback textarea {font-size: 24px !important}
# """

# Example to apply CSS styling
# with gr.Blocks(css=css) as demo:
#     box1 = gr.Textbox(value="Good Job", elem_classes="feedback")
#     box2 = gr.Textbox(value="Failure", elem_id="warning", elem_classes="feedback")

# Gradio UI
with gr.Blocks() as demo:
    # Title block
    # Apply CSS styling to the title
    title = gr.HTML(
        "<h1 style='color: #2563eb; font-weight:bold'>English Conjuction Finder</h1>"
    )
    with gr.Accordion("Accepted Words", open=False):
        # Search block
        search = gr.Textbox(
            label="Search",
            placeholder="Search accepted words here",
            lines=1,
            info="List of accpetable words in DFA",
            show_copy_button=True,
        )
        with gr.Row():
            cancel_btn = gr.ClearButton(search, variant="stop", interactive=False)
            search_btn = gr.Button(value="Search", variant="primary")
        resultSearch = gr.Dataframe(df, height=300, col_count=1, headers=["Words"])

        search.change(
            text_change_search,
            inputs=[search],
            outputs=[cancel_btn],
        )

        search_btn.click(
            search_and_display, inputs=[search], outputs=[resultSearch], api_name=False
        )

    # Text block for DFA and color match
    textTitle = gr.HTML("<h2 style='color: #2563eb;'>Try it here!</h2>")
    description = gr.HTML(
        "<p style='color: #a78bfa;'>Enter a text and see the words that are accepted by the DFA highlighted in <span style='color:#4ade80'>green</span>.</p>"
    )
    text = gr.Textbox(
        autofocus=True,
        label="Text",
        placeholder="Enter text here",
        info="Enter text to check for DFA match",
        show_copy_button=True,
    )

    # Examples block
    examples_data = generateExamples()
    examples = gr.Examples(
        examples=examples_data,
        inputs=[text],
    )
    with gr.Row():
        cancel_btn = gr.ClearButton([text], variant="stop", interactive=False)
        submit_btn = gr.Button(value="Submit", variant="primary", interactive=False)

    text.change(
        text_change_test,
        inputs=[text],
        outputs=[cancel_btn, submit_btn],
    )

    # Result block
    resultTitle = gr.HTML("<h2 style='color: #2563eb;'>Result</h2>")
    result = gr.HTML("<p></p>")

    # Position block
    # positionTitle = gr.HTML("<h2 style='color: gold;'>Position</h2>")
    position = gr.Dataframe(
        show_label=True, col_count=3, headers=["Words", "Positions", "Occurences"]
    )

    submit_btn.click(
        color_match,
        inputs=[text],
        outputs=[result, position],
        api_name=False,
    )
    cancel_btn.click(
        remove_output,
        inputs=[result, position],
        outputs=[result, position],
    )

# Launch the app
demo.launch()
