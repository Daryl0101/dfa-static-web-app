# Import libraries and modules
# Run pip install gradio and wonderwords in terminal
import gradio as gr
import pandas as pd
from wonderwords import RandomSentence
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


# Generate examples || RandomSentence is not the best way to generate examples || Should be replaced with self-generated examples
def generateExamples():
    s = RandomSentence()
    examples = []
    for i in range(3):
        examples.append(s.sentence())
    return examples


# Color match function
def color_match(text: gr.Textbox):
    print(type(text))
    colored_text = []
    pointer = 0

    # Get the result of the DFA check on the input text
    match_dict = dfa.check(text)

    # Flatten the match_dict into a list of tuples and sort by the start index
    matches = sorted(
        (start, end, word)
        for word, indices in match_dict.items()
        for start, end in indices
    )

    for start, end, word in matches:
        colored_text.append(text[pointer:start])
        # print(f"Start: {start}, End: {end}, Word: {word}")
        # End need to be incremented by 1 to include the last character
        colored_text.append(f'<span style="color:red;">{text[start:end + 1]}</span>')
        # print(f"Colored Text: {colored_text}")
        # Move the pointer to the end of the match
        pointer = end + 1

    # Add remaining text
    colored_text.append(text[pointer:])
    # print(f"Text before merge: {colored_text}")
    # Combine the strings
    colored_text = "".join(colored_text)
    # print(f"Colored Text after merging: {colored_text}")

    # Call getPositions function and get the DataFrame
    positions_df = getPositions(text)
    # print(f"Positions_df: {positions_df}")

    return colored_text, positions_df


# Get positions function
def getPositions(text):
    match_dict = dfa.check(text)
    positions_df = pd.DataFrame(columns=["Words", "Positions", "Occurences"])
    for word, positions in match_dict.items():
        # Convert the list of tuples to a string
        positions_str = ", ".join(map(str, positions))
        print(f"Word: {word}, Positions: {positions_str}")
        # Store the word and the positions string in the wordPositions dictionary
        # wordPositions[word] = {"Position": positions_str, "Occurences": len(positions)}
        positions_df.loc[len(positions_df)] = [word, positions_str, len(positions)]
        print(f"Word Positions: {positions_df}")

    return positions_df


# Search and display function
def search_and_display(search_query):
    # Filter the DataFrame based on the search query
    filtered_df = df[df["Words"].str.contains(search_query)]
    # print(f"Filtered text: {filtered_df}")
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
        "<h1 style='color: gold; margin-bottom: 0px font-weight:bold'>English Conjuction Finder</h1>"
    )
    with gr.Accordion("Accepted Words", open=False):
        description = gr.HTML(
            "<p style='color: #fef9c3;'>Enter a text and see the words that are accepted by the DFA highlighted in red.</p>"
        )

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

    # Adding a line break
    line_break = gr.HTML("<br>")

    # Text block for DFA and color match
    textTitle = gr.HTML("<h2>Try it here!</h2>")
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
        cancel_btn = gr.ClearButton(text, variant="stop", interactive=False)
        submit_btn = gr.Button(value="Submit", variant="primary", interactive=False)

    text.change(
        text_change_test,
        inputs=[text],
        outputs=[cancel_btn, submit_btn],
    )

    # Result block
    resultTitle = gr.HTML("<h2 style='color: gold; margin-bottom: 5px'>Result</h2>")
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

# Launch the app
demo.launch(share=True)
