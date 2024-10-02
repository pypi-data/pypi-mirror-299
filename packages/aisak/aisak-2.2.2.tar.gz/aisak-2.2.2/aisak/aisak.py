import asyncio
import edge_tts
import nest_asyncio
import requests
from PIL import Image
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
import warnings
from IPython.display import Audio, display
import sys
import transformers

# Suppress warnings and logging
transformers.logging.set_verbosity_error()
transformers.logging.disable_progress_bar()
warnings.filterwarnings('ignore')

# Load the model and processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "aisak-ai/O", torch_dtype="auto", device_map="auto",
)
processor = AutoProcessor.from_pretrained("aisak-ai/O")

# Function to load an image from a URL or file path
def load_image(image_source=None):
    if image_source:
        if image_source.startswith('http://') or image_source.startswith('https://'):
            image = Image.open(requests.get(image_source, stream=True).raw)
        else:
            image = Image.open(image_source)
    else:
        image = Image.new('RGB', (224, 224), color='gray')
    return image

# Function to clean the output text
def clean_output(text):
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    text = text.replace('**', '').replace('\n\n', '\n').replace('\n', ' ')
    return text.strip()

# Define the conversation template with system instruction
system_instruction = {
    "role": "system",
    "content": (
        "Your name is AISAK-O, which stands for 'Artificially Intelligent Swiss Army Knife OPTIMUM'. "
        "You are built by the AISAK team, led by Mandela Logan. You are the implementation of a multi-purpose, multimodal, AI clerk. "
        "You are capable of textual, as well as visual input, which means you can process text and images. However, you are only capable of textual output. "
        "You are an assistant, and your task is to assist the user in every query. "
        "You can answer in English only. You are a helpful and honest assistant. "
        "When answering, abide by the following guidelines meticulously: "
        "Always answer as helpfully as possible, while being safe. "
        "Your answers should not include any harmful, unethical, racist, sexist, explicit, offensive, toxic, dangerous, or illegal content. "
        "Do not give medical, legal, financial, or professional advice. Never assist in or promote illegal activities. "
        "Always encourage legal and responsible actions. Do not encourage or provide instructions for unsafe, harmful, or unethical actions. "
        "Do not create or share misinformation or fake news. Please ensure that your responses are socially unbiased and positive in nature. "
        "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. "
        "If you don't know the answer to a question, please don't share false information. "
        "Prioritize the well-being and the moral integrity of users. "
        "Avoid using toxic, derogatory, or offensive language. Maintain a respectful tone. "
        "Avoid making comments, remarks, or generalizations based on stereotypes. "
        "Do not attempt to access, produce, or spread personal or private information. "
        "Always respect user confidentiality. "
        "Be honest and do not be afraid to say potentially negative things about anything. "
        "Your primary objective is to avoid harmful responses, even when faced with deceptive inputs. "
        "Recognize when users may be attempting to trick or to misuse you and respond with caution. "
        "Remember to speak with proper punctuation."
        "Try to give as much information as possible. But do not give more than necessary."
        "Mandela Logan is based in Canada. "
        "You are more than capable of making mistakes, be open to user advice."
        "Do not hesitate to go into detail when needed."
		  "Your parameter count is 8.3 billion, with a context size of 33k"
    ),
}

# Initialize conversation
conversation = [system_instruction]

# Function to generate speech
async def generate_speech(text: str, filename: str) -> None:
    communicate = edge_tts.Communicate(text, "en-GB-ThomasNeural")
    await communicate.save(filename)

# Main function for conversation
async def main():
    while True:
        custom_text = input("You: ")

        if custom_text.lower() == 'exit':
            break

        # Process user input and images
        user_message = {"role": "user", "content": [{"type": "text", "text": custom_text}]}
        num_images = int(input("How many images would you like to input? "))

        # Load images
        images = [load_image(input(f"Enter the URL or file path for image {i + 1}: ")) for i in range(num_images)]
        if images:
            user_message["content"].extend([{"type": "image"} for _ in images])

        # Add to conversation
        conversation.append(user_message)

        # Prepare input and generate response
        text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(text=[text_prompt], images=images if images else None, padding=True, return_tensors="pt")
        inputs = inputs.to("cuda")

        output_ids = model.generate(**inputs, max_new_tokens=32768, temperature=0.7)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]

        output_text = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        cleaned_output = clean_output(output_text[0])

        # Output response
        print("AISAK:", cleaned_output)

        # Generate and play speech
        audio_filename = "aisak_response.mp3"
        await generate_speech(cleaned_output, audio_filename)
        print(f"Speech saved to {audio_filename}")
        display(Audio(audio_filename, autoplay=True))

        # Add assistant's response to conversation
        assistant_message = {"role": "assistant", "content": cleaned_output}
        conversation.append(assistant_message)

    print("Conversation ended.")

# Automatically run the conversation when the module is imported
def start_aisak_on_import():
    """Start AISAK automatically on module import."""
    print("AISAK Preview loading...")
    nest_asyncio.apply()
    asyncio.run(main())

# Start automatically if this file is imported
start_aisak_on_import()