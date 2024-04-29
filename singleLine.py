import tkinter as tk
from PIL import Image, ImageTk
from picamera import PiCamera
import cv2
import pytesseract
from googletrans import Translator
import sys
from io import StringIO

targLangs = ["latin based", "ara", "rus", "hin", "chi_sim", "jpn"]
#0 latin based, #1 arabic, #2 russian
#3 hindi, #4 chinese simplified, #5 japanese
destLangs = ["en", "es", "fr", "de", "it", "pt-PT", "ar", "ru", "hi", "zh-CN", "ja"]
#0- en,english #1- es,spanish #2- fr,french
#3- de,german #4- it,italian #5- pt-PT portugal portuguese
#6- ar,arabic #7- ru,russian #8- hi,hindi
#9- zh-CN,chinese #10- ja,japanese


class RedirectedText:
    def __init__(self, widget):
        self.widget = widget
        self.buffer = StringIO()

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):
        pass  # No need to flush for this implementation

class OCRApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OCR Application")
        self.geometry("1000x600")

        self.target_langs = ["Latin Based", "Arabic", "Russian", "Hindi", "Chinese Simplified", "Japanese"]
        self.dest_langs = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Arabic", "Russian", "Hindi", "Chinese", "Japanese"]

        self.target_lang_index = 0
        self.dest_lang_index = 0

        self.camera = None  # Define camera instance

        self.create_widgets()

        # Redirect standard output to textbox
        self.redirected_text = RedirectedText(self.result_text)
        sys.stdout = self.redirected_text

    def create_widgets(self):
        self.target_lang_buttons = []
        self.dest_lang_buttons = []

        # Target Language Selection Frame
        self.target_lang_frame = tk.Frame(self)
        self.target_lang_frame.pack(expand=True, fill="both")

        for i, lang in enumerate(self.target_langs):
            lang_button = tk.Button(self.target_lang_frame, text=lang, command=lambda idx=i: self.on_target_lang_selected(idx))
            lang_button.grid(row=0, column=i, padx=10, pady=10)
            self.target_lang_buttons.append(lang_button)

        # Destination Language Selection Frame
        self.dest_lang_frame = tk.Frame(self)
        self.dest_lang_frame.pack(expand=True, fill="both")

        for i, lang in enumerate(self.dest_langs):
            lang_button = tk.Button(self.dest_lang_frame, text=lang, command=lambda idx=i: self.on_dest_lang_selected(idx))
            lang_button.grid(row=0, column=i, padx=10, pady=10)
            self.dest_lang_buttons.append(lang_button)

        # Capture Mode Frame
        self.capture_frame = tk.Frame(self)
        self.capture_frame.pack(expand=True, fill="both")

        # Image Output
        self.image_output = tk.Label(self.capture_frame)
        self.image_output.pack(side="left", padx=10, pady=10)

        # Text Output with Scrollbar
        self.text_output_frame = tk.Frame(self.capture_frame)
        self.text_output_frame.pack(side="right", fill="both", expand=True)

        self.result_text = tk.Text(self.text_output_frame, wrap=tk.WORD, width=50)
        self.result_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.text_output_frame, command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Reset, Pause, Stop Buttons
        self.control_frame = tk.Frame(self)
        self.control_frame.pack()

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left", padx=10)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=10)

    def on_target_lang_selected(self, index):
        self.target_lang_index = index
        self.hide_target_lang_buttons()
        self.show_dest_lang_buttons()

    def on_dest_lang_selected(self, index):
        self.dest_lang_index = index
        self.hide_dest_lang_buttons()
        self.start_capture_mode()

    def hide_target_lang_buttons(self):
        self.target_lang_frame.pack_forget()

    def show_dest_lang_buttons(self):
        self.dest_lang_frame.pack(expand=True, fill="both")

    def hide_dest_lang_buttons(self):
        self.dest_lang_frame.pack_forget()

    def start_capture_mode(self):
        self.capture_frame.pack(expand=True, fill="both")
        self.camera = PiCamera()  # Initialize camera instance
        self.capture_image()

    def reset(self):
        if self.camera:
            self.camera.close()  # Close camera instance
        self.destroy()
        app = OCRApp()
        app.mainloop()

    def pause(self):
        # Implement pause functionality
        pass

    def stop(self):
        if self.camera:
            self.camera.close()  # Close camera instance
        self.destroy()

    def capture_image(self):
        # Capture image using PiCamera
        if not self.camera:
            self.camera = PiCamera()  # Initialize camera if not already initialized
        self.camera.resolution = (800, 600)  # Set camera resolution
        self.camera.capture("/home/seniordesign/Documents/seniordesign/pic.jpg")

        # Load and display image in GUI
        image = Image.open("/home/seniordesign/Documents/seniordesign/pic.jpg")
        image.thumbnail((400, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_output.configure(image=photo)
        self.image_output.image = photo  # To prevent garbage collection

	# Perform OCR and translation
        if(self.target_lang_index == 0):
        	img = cv2.imread("/home/seniordesign/Documents/seniordesign/pic.jpg")
        	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        	threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        	text = pytesseract.image_to_string(img, config='--psm 7')
#        	text = pytesseract.image_to_string(img)

        	confidences = []
        	data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        	for i in range(len(data['text'])):
        		word = data['text'][i]
        		conf = int(data['conf'][i])
        		if word != "":
        			confidences.append((word, conf))

        else:
        	img = cv2.imread("/home/seniordesign/Documents/seniordesign/pic.jpg")
        	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        	threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        	text = pytesseract.image_to_string((img), lang = targLangs[self.target_lang_index], config='--psm 7')
        	#text = pytesseract.image_to_string((img), lang = targLangs[self.target_lang_index])

        	confidences = []
        	data = pytesseract.image_to_data(img, lang = targLangs[self.target_lang_index], output_type=pytesseract.Output.DICT)
        	for i in range(len(data['text'])):
        		word = data['text'][i]
        		conf = int(data['conf'][i])
        		if word != "":
        			confidences.append((word, conf))

        translation = Translator().translate(text, dest=self.dest_langs[self.dest_lang_index])
        if len(translation.text) > 1:
#                translations_string = ""
                first_confidence = 0
                for word, conf in confidences:
#                        translation2 = Translator().translate(word, dest=self.dest_langs[self.dest_lang_index])
#                        if len(translation2.text) > 1 and conf > 75:
#                                translations_string += f"{translation2.text} "
                        if(first_confidence == 0):
                                first_confidence = conf
                if(first_confidence > 50):
                        resultText = translation.text.replace("|", "")
                        self.result_text.insert(tk.END, f"{resultText}\n {first_confidence}%\n")

	# Schedule the next capture after 1000ms (1 second)
        self.after(1000, lambda: self.capture_image())

if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
