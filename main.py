from predictor import create_gradio_interface, MODEL


print("🚀 Starting Crypto News Analyzer...")
print(f"📡 Make sure Ollama is running and <<< {MODEL} >>> model is installed!")
print(f"💡 To install the model: ollama pull <<< {MODEL} >>>")
print("-" * 70)

# Create and launch interface
interface = create_gradio_interface()
interface.launch(
    share=True,  # Set to True if you want a public link
    server_name="127.0.0.1",
    server_port=7860,
    show_api=False
)