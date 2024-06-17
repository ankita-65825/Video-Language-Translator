# Video Language Translator

This project allows you to translate the audio of a video from one language to another. 

Features:

* Supports various video formats (mp4, mov, avi, mkv)
* Leverages pre-trained multilingual models for translation (facebook/mbart-large-50-many-to-one-mmt)
* Offers speech recognition and text-to-speech functionality

**Requirements:**

* Python 3.6 or later
* Streamlit
* SpeechRecognition
* transformers
* gtts
* moviepy

**Installation:**

```bash
pip install streamlit speech_recognition transformers gtts moviepy
```

**Usage:**

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/video-language-translator.git
```

2. Navigate to the project directory:

```bash
cd video-language-translator
```

3. Run the application:

```bash
streamlit run main.py
```

4. Upload a video file and select the source and target languages.
5. Click the "Translate Video" button.
6. The translated video will be downloaded as "translated_video.mp4".

**Supported Languages:**

* English (en)
* French (fr)
* Spanish (es)
* German (de)
* Chinese (zh)
* Hindi (hi)
* Russian (ru)
* Portuguese (pt)
* Italian (it)

**Note:**
* The model may not provide accurate translations for all languages and scenarios.
* This project is for educational purposes only.

**Contributing:**

We welcome contributions to this project. Feel free to fork the repository and submit pull requests with your improvements.

Some Glimpse of it :

![image](https://github.com/ankita-65825/Video-Language-Translator/assets/91601431/66acf744-9e07-4820-ad7c-87ed6090edf5)

![image](https://github.com/ankita-65825/Video-Language-Translator/assets/91601431/3a3bf589-c720-4f74-bdc6-8cc67af843e1)



