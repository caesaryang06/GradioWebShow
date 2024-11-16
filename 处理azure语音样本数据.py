from tools import customer_common_funcs as ccf
from tools.azure_local_service import AzureTextToSpeech
import os

# 获取密钥
subscription_key = os.environ.get('AZURE_SUBSCRIPTION_KEY')
# 获取分区
region = os.environ.get('AZURE_REGION')
tts = AzureTextToSpeech(subscription_key, region)




def read_pre():
    with open('data.txt') as file:
        lines = file.readlines()
        for line in lines:
            list = line.split(",")
            Voice = list[0].replace("Voice Name: ", "")
            Gender = list[1].replace(" Gender: SynthesisVoiceGender.", "")
            Language = list[2].replace(" Locale: ", "").replace("\n", "")
            if Language == "en-US":
                text = "Hard work pays off. Keep pushing forward and you'll achieve your goals."
                audio = "{}.wav".format(Voice.replace(':', '_'))
                audio_file = f"data/azure_voice_samples/{Language}/{Gender}/{audio}"
                tts.text_to_speech(text, audio_file,Voice )
                Language = "美式英语"
                print(
                    f"Voice Name: {Voice}, Gender: {Gender}, Locale: {Language}")
            elif Language == "zh-CN":
                text = "春天来了，大地复苏，处处洋溢着生机与活力。"
                audio = "{}.wav".format(Voice.replace(':', '_'))
                audio_file = f"data/azure_voice_samples/{Language}/{Gender}/{audio}"
                tts.text_to_speech(text, audio_file, Voice)
                print(
                    f"Voice Name: {Voice}, Gender: {Gender}, Locale: {Language}")
            





if __name__ == "__main__":
    read_pre()