import gradio as gr

from scripts import project, moegoe, ffmpeg, settings

from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks() as gimai:
        out_html = gr.HTML()
        with gr.Tabs() as tabs:
            with gr.TabItem("Settings"):
                cfg = settings.load_settings()
                save_settings = gr.Button("Save settings")
                with gr.Box():
                    input_dir = gr.Textbox(value=cfg['input_dir'], label="Input directory")
                    voice_ext = gr.Textbox(value=cfg['voice_ext'], label="Voice ext")
                    image_ext = gr.Textbox(value=cfg['image_ext'], label="Image ext")

                with gr.Box():
                    moegoe_path = gr.Textbox(value=cfg['moegoe_path'], label="[Optional] Path to MoeGoe.exe (CLI)")
                    moegoe_model_dir = gr.Textbox(value=cfg['moegoe_model_dir'], label="VITS saved_model directory")
                    moegoe_dr = gr.Textbox(value=cfg['moegoe_dr'], label="Duration ratio(話速)")
                    moegoe_nr = gr.Textbox(value=cfg['moegoe_nr'], label="Noise ratio(音高)")
                    moegoe_nb = gr.Textbox(value=cfg['moegoe_nb'], label="Noise bias(抑揚)")
                    moegoe_ja = gr.Textbox(value=cfg['moegoe_ja'], label="Add Tags", placeholder='[JA]')
                    moegoe_generate = gr.Button("Generate MoeGoe All")
                    #moegoe_allplay = gr.Button("All Play")
                with gr.Box():
                    ffmpeg_path = gr.Textbox(value=cfg['ffmpeg_path'], label="[Optional] Path to ffmpeg.exe (CLI)")
                    ffmpeg_generate = gr.Button("Generate mp4 aac All")

                with gr.Box():
                    build_dir = gr.Textbox(value=cfg['build_dir'], label="Output directory")
                    build_btn = gr.Button("build")

            with gr.TabItem("Project Viewer"):
                reload_btn = gr.Button("Reload")
                out_voice = gr.Audio()
                table_html = gr.HTML()

                voice_btn = gr.Button(elem_id=f"gimai_voice_button", visible=False).style(container=False)
                image_btn = gr.Button(elem_id=f"gimai_image_button", visible=False).style(container=False)
            with gr.TabItem("MoeGoe Actors"):
                reload_model = gr.Button("Reload")
                model_html = gr.HTML()
            with gr.TabItem("Image Preview"):
                out_image = gr.Image()

        reload_model.click(
            fn=moegoe.reload_table,
            inputs=[moegoe_model_dir],
            outputs=[model_html]
        )
        moegoe_generate.click(
            fn=moegoe.generate_all,
            inputs=[input_dir, voice_ext, image_ext, moegoe_model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja],
            outputs=[out_html]
        )
        ffmpeg_generate.click(
            fn=ffmpeg.generate_all,
            inputs=[input_dir, voice_ext, image_ext, ffmpeg_path],
            outputs=[out_html]
        )

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
            inputs=[title, input_dir, moegoe_model_dir, moegoe_path, moegoe_dr, moegoe_nr, moegoe_nb, moegoe_ja],
            outputs=[out_voice],
        )
        image_btn.click(
            fn=project.show_image,
            inputs=[title],
            outputs=[out_image],
        )
        moegoe_allplay.click(
            fn=moegoe.get_all_paths,
            inputs=[input_dir, voice_ext, image_ext],
            outputs=[out_voice],
        )

        save_settings.click(
            fn=settings.save_settings,
            inputs=[
                input_dir,
                voice_ext,
                image_ext,
                moegoe_path,
                moegoe_model_dir,
                moegoe_dr,
                moegoe_nr,
                moegoe_nb,
                moegoe_ja,
                ffmpeg_path,
                build_dir,
            ],
            outputs=[out_html])

    return (gimai, "Gimai", "gimai"),


script_callbacks.on_ui_tabs(on_ui_tabs)
