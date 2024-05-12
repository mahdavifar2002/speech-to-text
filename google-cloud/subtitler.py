import os
import ffmpeg

from google.cloud import storage
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

input_video = "input.mp4"
loglevel = "error"

def extract_audio():
    ffmpeg.input(input_video).output("stereo.wav", loglevel=loglevel).run(overwrite_output=True)
    ffmpeg.input("stereo.wav").output("mono.wav", ac=1, loglevel=loglevel).run(overwrite_output=True)

def transcribe(
    project_id: str,
    bucket_name: str,
    file_name: str,
) -> cloud_speech.BatchRecognizeResults:
    """Transcribes audio from a Google Cloud Storage URI.

    Args:
        project_id: The Google Cloud project ID.
        gcs_uri: The Google Cloud Storage URI.
        gcs_output_path: The Cloud Storage URI to which to write the transcript.

    Returns:
        The BatchRecognizeResults message.
    """
    # Instantiates a Cloud Storage client
    storage_client = storage.Client(project=project_id)

    # Uploading the audio file to the Cloud Storage
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(f"audio/{file_name}")
    result = blob.upload_from_filename(file_name)
    print("Audio uploaded to the cloud.", result)

    # Generate the gsc links
    gcs_uri = f"gs://{bucket_name}/audio/{file_name}"

    # Instantiates a client
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["fa-IR"],
        model="chirp",
        features=cloud_speech.RecognitionFeatures(
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True,
        ),

    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/europe-west4/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
            output_format_config=cloud_speech.OutputFormatConfig(
                srt=cloud_speech.SrtOutputFileFormatConfig(),
            )
        ),
    )

    # Transcribes the audio into text
    client_options_var = ClientOptions(api_endpoint="europe-west4-speech.googleapis.com")
    client = SpeechClient(client_options=client_options_var)
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    # Generate the .srt file
    subtitle_filename = "subtitle.srt"

    with open(subtitle_filename, "w") as subtitle_file:
        subtitle_file.write(response.results[gcs_uri].inline_result.srt_captions)
    
    return subtitle_filename

def add_subtitle_to_video(soft_subtitle, subtitle_file,  subtitle_language):

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = "output.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"},
            loglevel="error"
        )
        ffmpeg.run(stream, overwrite_output=True)
    
    else:
        subtitle_style = "FontName=Vazirmatn,FontSize=22,BorderStyle=4,BackColour=&H80000000,MarginV=20"
        subtitle_font_dir = "ttf"

        stream = ffmpeg.input(input_video).output(
            output_video,
            vf=f"subtitles={subtitle_file}:fontsdir={subtitle_font_dir}:force_style='{subtitle_style}'",
            loglevel=loglevel)
        ffmpeg.run(stream, overwrite_output=True)

def run():
    print("\nExtracting audio from the input video...\n")
    extracted_audio = extract_audio()

    print("\nTranscribing the auido...\n")
    # subtitle_file = "subtitle.srt"
    subtitle_file = transcribe("protean-vigil-368221", "mahdavifar", "mono.wav")

    print("\nAdding the subtitle to the video...\n")
    add_subtitle_to_video(
         soft_subtitle=True,
         subtitle_file=subtitle_file,
         subtitle_language="fa"
    )

    print("\nRemoving extra files generated...\n")
    os.remove("stereo.wav")
    os.remove("mono.wav")
    os.remove(f"subtitle.srt")

run()