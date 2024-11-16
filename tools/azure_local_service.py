import azure.cognitiveservices.speech as speechsdk


class AzureTextToSpeech:
    def __init__(self, subscription_key, region):
        """
        初始化Azure文本转语音服务

        Args:
            subscription_key (str): Azure订阅密钥
            region (str): Azure服务所在的区域
        """
        speech_config = speechsdk.SpeechConfig(
            subscription=subscription_key, region=region)
        self.speech_config = speech_config

    def text_to_speech(self, text, output_file, voice_name="zh-CN-XiaoxiaoNeural"):
        """
        将文本转换为语音并保存到指定文件

        Args:
            text (str): 要转换的文本
            output_file (str): 输出音频文件的路径
        """
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

        self.speech_config.speech_synthesis_voice_name = voice_name

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text(text)

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(
                    cancellation_details.error_details))



