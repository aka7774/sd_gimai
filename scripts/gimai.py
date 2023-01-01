import gradio as gr

from scripts import project

from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks() as gimai:
        out_html = gr.HTML()
        with gr.Tabs() as tabs:
            with gr.TabItem("List"):
                input_dir = gr.Textbox(value=project.default_input_dir(), label="Input directory")
                voice_ext = gr.Textbox(value='wav', label="Voice ext")
                image_ext = gr.Textbox(value='webp', label="Image ext")

                reload_btn = gr.Button("Reload")
                table_html = gr.HTML()
            with gr.TabItem("Preview"):
                out_voice = gr.Audio()
                out_image = gr.Image()
                voice_btn = gr.Button(elem_id=f"gimai_voice_button", visible=False).style(container=False)
                image_btn = gr.Button(elem_id=f"gimai_image_button", visible=False).style(container=False)
            with gr.TabItem("Build"):
                build_dir = gr.Textbox(value=project.default_build_dir(), label="Output directory")
                build_btn = gr.Button("build")

        reload_btn.click(
            fn=project.reload_table,
            inputs=[input_dir, voice_ext, image_ext],
            outputs=[table_html]
        )
        build_btn.click(
            fn=project.build,
            inputs=[input_dir, voice_ext, image_ext, build_dir],
            outputs=[out_html]
        )

        title = gr.Text(elem_id=f"gimai_title", visible=False).style(container=False)
        voice_btn.click(
            fn=project.show_voice,
            inputs=[title],
            outputs=[out_voice],
        )
        image_btn.click(
            fn=project.show_image,
            inputs=[title],
            outputs=[out_image],
        )

    return (gimai, "Gimai", "gimai"),


script_callbacks.on_ui_tabs(on_ui_tabs)
