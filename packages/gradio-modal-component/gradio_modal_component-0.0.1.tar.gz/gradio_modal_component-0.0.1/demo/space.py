
import gradio as gr
from app import demo as app
import os

_docs = {'modal_component': {'description': '', 'members': {'__init__': {'visible': {'type': 'bool', 'default': 'False', 'description': 'If False, modal will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional string or list of strings that are assigned as the class of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'allow_user_close': {'type': 'bool', 'default': 'True', 'description': 'If True, user can close the modal (by clicking outside, clicking the X, or the escape key).'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'close_on_esc': {'type': 'bool', 'default': 'True', 'description': 'If True, allows closing the modal with the escape key. Defaults to True.'}, 'close_outer_click': {'type': 'bool', 'default': 'True', 'description': 'If True, allows closing the modal by clicking outside. Defaults to True.'}, 'close_message': {'type': 'str | None', 'default': 'None', 'description': 'The message to show when the user tries to close the modal. Defaults to None.'}, 'bg_blur': {'type': 'int | None', 'default': '4', 'description': 'The percentage of background blur. Should be a float between 0 and 1. Defaults to None.'}, 'width': {'type': 'int | None', 'default': 'None', 'description': 'Modify the width of the modal.'}, 'height': {'type': 'int | None', 'default': 'None', 'description': 'Modify the height of the modal.'}}, 'postprocess': {}}, 'events': {'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the modal_component is unfocused/blurred.'}}}, '__meta__': {'additional_interfaces': {}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_modal_component`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_modal_component
```

## Usage

```python

import gradio as gr
from gradio_modal_component import modal_component


def display_image(img):
    return img


def get_blur_value(selected_blur):
    return selected_blur


with gr.Blocks() as demo:
    gr.Markdown("# Image Modal Demonstration")

    with gr.Tab("Tab 1"):
        gr.Markdown(
            \"\"\"
        - Fixed close icon (X) is overlapped by the image. or big components.

        \"\"\"
        )
        show_btn = gr.Button("Show Modal")
        gr.Markdown(
            \"\"\"
        - Enable the `allow_user_close` parameter to allow the user to close the modal by clicking outside, clicking the X, or pressing the escape key. In this case `allow_user_close = False` (Modal 1 is true), If not set defaults to `True`.
        - Enale the `esc_close` parameter to allow the user to close the modal by pressing the escape key.
        \"\"\"
        )
        show_btn2 = gr.Button("Show Modal 2")

        gr.Markdown(
            \"\"\"
        - Enale the `close_outer_click` parameter to allow the user to close the modal by click on the blur. Defaults to `True`, in this case `close_outer_click = False` (Modal 3 is true).
        \"\"\"
        )
        show_btn3 = gr.Button("Show Modal 3")

        gr.Markdown(
            \"\"\"
        - Enale the `close_message` parameter to show a message when the user tries to close the modal. Defaults to `None`.
        \"\"\"
        )
        show_btn4 = gr.Button("Show Modal 4")

        gr.Markdown(
            \"\"\"
        - Handle Z-index.
        \"\"\"
        )

        show_btn5 = gr.Button("Show Modal 5")

        gr.Markdown(
            \"\"\"
        - Add `bg_blur` option to dynamically change the background blur of the modal.
        \"\"\"
        )

        # Dropdown for selecting blur level
        blur_level = gr.Dropdown(
            [0, 4, 8, 12, 16],
            label="Blur Level",
            value=4,  # Default value
            interactive=True,
        )

        show_btn6 = gr.Button("Show Modal 6")

        with gr.Row():
            width_input = gr.Textbox(label="Width", placeholder="Enter width")
            height_input = gr.Textbox(label="Height", placeholder="Enter height")

        show_btn7 = gr.Button("Show Modal 7")

    with modal_component(visible=False, allow_user_close=True) as modal:
        gr.Image(
            "https://images.unsplash.com/photo-1612178537253-bccd437b730e",
            label="Random Image",
        )

    with modal_component(visible=False, allow_user_close=False, close_on_esc=True) as modal2:
        with gr.Column():
            upload_img = gr.Image(label="Upload Image", type="pil")
            display_btn = gr.Button("Display Image")
            output_img = gr.Image(label="Displayed Image")
        display_btn.click(fn=display_image, inputs=upload_img, outputs=output_img)

    with modal_component(visible=False, close_outer_click=False) as modal3:
        with gr.Column():
            upload_img = gr.Image(label="Upload Image", type="pil")
            display_btn = gr.Button("Display Image")
            output_img = gr.Image(label="Displayed Image")
        display_btn.click(fn=display_image, inputs=upload_img, outputs=output_img)

    with modal_component(
        visible=False,
        close_outer_click=True,
        close_message="Are you sure want to close ?",
    ) as modal4:
        with gr.Column():
            upload_img = gr.Image(label="Upload Image", type="pil")
            display_btn = gr.Button("Display Image")
            output_img = gr.Image(label="Displayed Image")
        display_btn.click(fn=display_image, inputs=upload_img, outputs=output_img)

    with modal_component(visible=False, close_outer_click=True) as modal5:
        with modal_component(
            visible=False,
            close_outer_click=True,
            close_message="Are you sure want to close ?",
        ) as modal51:
            with gr.Column():
                upload_img = gr.Image(label="Upload Image", type="pil")
                display_btn = gr.Button("Display Image")
                output_img = gr.Image(label="Displayed Image")
            display_btn.click(fn=display_image, inputs=upload_img, outputs=output_img)

        gr.Markdown(
            \"\"\"
        # Handling Z-index for Modal
        \"\"\"
        )

        show_btn51 = gr.Button("Show Sub Modal 5")

    with modal_component(visible=False) as modal6:
        gr.Markdown(
            f\"\"\"
            # View Background Blur Level
            \"\"\"
        )

    show_btn.click(lambda: modal_component(visible=True), None, modal)
    show_btn2.click(lambda: modal_component(visible=True), None, modal2)
    show_btn3.click(lambda: modal_component(visible=True), None, modal3)
    show_btn4.click(lambda: modal_component(visible=True), None, modal4)
    show_btn5.click(lambda: modal_component(visible=True), None, modal5)
    show_btn51.click(lambda: modal_component(visible=True), None, modal51)

    show_btn6.click(
        lambda blur: modal_component(visible=True, bg_blur=blur),
        inputs=blur_level,
        outputs=modal6,
    )


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `modal_component`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["modal_component"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["modal_component"]["events"], linkify=['Event'])







    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {};
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
