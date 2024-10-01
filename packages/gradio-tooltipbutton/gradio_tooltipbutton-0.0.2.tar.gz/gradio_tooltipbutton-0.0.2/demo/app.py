import gradio as gr
from gradio_tooltipbutton import TooltipButton

example = TooltipButton().example_value()

demo = gr.Interface(
    lambda x: x,
    TooltipButton(tooltip="test"),  # interactive version of your component
    TooltipButton(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
