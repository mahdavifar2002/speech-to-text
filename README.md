# speech-to-text
Implement different speech-to-text solutions using available models or APIs.

## Whisper
Following [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg) I used the [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) reimplementation of OpenAI's Whisper model. Please refer to the linked tutorial for more detail.

## Google Cloud Speech-to-Text API
Google Speech-to-Text API has three main methods to perform speech recognition: synchronous, asynchronous, and streaming. More information about these three methods are available [here](https://cloud.google.com/speech-to-text/docs/speech-to-text-requests).

The file [google-cloud/subtitler.py](./google-cloud/subtitler.py) takes advantage of the async method, which by the time is the only method supporting the `.srt` output format. Before you run this code, remember to:

- Update the global variables with your own GCP account details.
- Login to your Google Cloud account using this shell command:
  ```shell
  gcloud auth application-default login
  ```
