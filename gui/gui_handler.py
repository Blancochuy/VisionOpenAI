import tkinter as tk
import os
import sys
import logging
from tkinter import filedialog, Label, messagebox, Text, Scrollbar
from tkinter.scrolledtext import ScrolledText 
from PIL import Image, ImageTk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.gpt4v_api_handler import GPT4VAPIHandler

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(filename='logs/gpt4v_tester.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
# Configure logging to log info messages
logging.basicConfig(filename='logs/info.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GUIHandler:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.image_path = None
        self.image_display = None
        self.original_image = None
        self.api_handler = GPT4VAPIHandler("config/config.json")


    def setup_ui(self):
        # Window title and size
        self.root.title("GPT-4V Tester")
        self.root.minsize(600, 500)

        # Frame for image upload
        self.upload_frame = tk.Frame(self.root)
        self.upload_frame.pack(pady=10)

        # Button to upload image
        self.upload_button = tk.Button(self.upload_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        # Set initial size for the image label
        self.image_label = Label(self.root)
        self.image_label.pack(pady=10)

        # Use ScrolledText for the response area
        self.response_area = ScrolledText(self.root, height=10, width=50, font=("Consolas", 10), wrap=tk.WORD, padx=10, pady=10)
        self.response_area.pack(pady=10)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Get GPT-4V Response", command=self.get_response)
        self.submit_button.pack(pady=10)

    def upload_image(self):
        # Function to handle image upload, with file dialog
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        # If there's no image, do nothing
        if not self.original_image:
            return

        # Resize the image to a fixed size
        self.original_image.thumbnail((600, 500), Image.Resampling.LANCZOS)  # Resize to fit within a 600x500 area
        self.image_display = ImageTk.PhotoImage(self.original_image)

        # Update the label with the new image
        self.image_label.config(image=self.image_display)
        self.image_label.image = self.image_display  # Keep a reference to avoid garbage collection

    def get_response(self):
        if self.image_path:
            try:
                response = self.api_handler.get_response(self.image_path)
                # Assuming the response will be a dict with a 'choices' key
                if not isinstance(response, dict) or 'choices' not in response:
                    raise ValueError("Response format is not as expected.")
                self.display_response(response)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                logging.error(f"An error occurred: {e}")

    def display_response(self, response):
        # Clear the response area
        self.response_area.delete('1.0', tk.END)

        # Navigate the response data structure
        try:
            if 'choices' in response:
                choice = response['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    message_content = choice['message']['content']
                    self.response_area.insert(tk.END, message_content)
                    logging.info("API response received and displayed.")
                else:
                    raise ValueError("Content not found in response.")
            else:
                raise ValueError("Unexpected response format.")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            logging.error(f"Display Response Error: {ve}")
            self.response_area.insert(tk.END, "An error occurred while parsing the response.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUIHandler(root)
    root.mainloop()
