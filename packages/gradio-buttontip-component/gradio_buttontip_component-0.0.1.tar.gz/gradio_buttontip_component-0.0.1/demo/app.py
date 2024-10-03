
import gradio as gr
from gradio_buttontip_component import buttontip_component


def button_click(a,b):
    return "Button clicked!"

demo = gr.Interface(
    title="Button with Tooltip",
    description="This interface showcases a button with a tooltip.",
    fn=button_click,
    inputs=[
        # Change X, Y values to position the tooltip
        buttontip_component(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="red",
            x=50,  # No horizontal offset
            y=-30,  # Above the button
            value="Top Button"
        ),
        buttontip_component(
            tooltip="Tooltip Text",
            tooltip_color="white",  # Custom color
            tooltip_background_color="green",
            x=140,  # No horizontal offset
            y=20,  # Below the button
            value="Bottom Button"
        )
    ],
    outputs="text",
)


if __name__ == "__main__":
    demo.launch()
