# speech-to-text
Implement different speech-to-text solutions using available models or APIs.

## Whisper
Following [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg) I used the [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) reimplementation of OpenAI's Whisper model. Please refer to the linked tutorial for more detail.

## Google Cloud Speech-to-Text API
Google Speech-to-Text API has three main methods to perform speech recognition: synchronous, asynchronous, and streaming. More information about these three methods are available [here](https://cloud.google.com/speech-to-text/docs/speech-to-text-requests).

- To use the Google Cloud APIs, it is good to run the following shell commands in advance, to set the enviroment:
    - To login to your Google Cloud acount and setting the local Application Default Credentials:
    ```shell
    gcloud auth application-default login
    ```
    - To set your project property in the core section:
    ```shell
    gcloud config set project PROJECT_ID
    ```

- The file [google-cloud/subtitler.py](./google-cloud/subtitler.py) takes advantage of the async method, which by the time is the only method supporting the `.srt` output format. Before you run this code, remember to update the global variables with your own GCP account details.

- The file [google-cloud/streamer.py](./google-cloud/streamer.py) comes from [this documentation](https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio) and uses the streaming method to transcribe the speech comming from the microphone. It works with the `pyaudio` library, which could be tricky to setup. Please follow [this manual](https://medium.com/@niveditha.itengineer/learn-how-to-setup-portaudio-and-pyaudio-in-ubuntu-to-play-with-speech-recognition-8d2fff660e94) for the installation process in Ubuntu.