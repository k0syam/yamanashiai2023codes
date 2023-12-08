from openai import OpenAI
import urllib.request
from dotenv import load_dotenv

### .envファイルにOPENAI_API_KEYを記入することでapi_keyのベタ書きを防ぐ
load_dotenv()


class Dalle2Communication(object):
    """DALLE II API向けのクラス。画像を取得をまとめる

    Args:
        object (_type_): _description_
    """

    def __init__(self, api_key=None, prompt_initial=None):
        self.model = "dall-e-3"
        if api_key == None:
            self.client = OpenAI()
        else:
            self.client = OpenAI(api_key=api_key)
        self.default_prompt = "a white siamese cat"
        if prompt_initial == None:
            self.messages = self.default_prompt
        else:
            self.messages = prompt_initial
        self.size = "1024x1024"
        self.quality = "standard"
        self.n = 1
        self.images_url = []

    def generate_image(self, prompt):
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )
        self.images_url.append(response.data[0].url)
        return self.images_url[-1]

    def download_latest_image(self, filename):
        if len(self.images_url) == 0:
            return "you need 1 image at least"
        else:
            image = self.images_url[-1]
            with urllib.request.urlopen(image) as web_file:
                data = web_file.read()
                with open(filename, mode="wb") as local_file:
                    local_file.write(data)


if __name__ == "__main__":
    d2c = Dalle2Communication()
    d2c.generate_image("a black siamese cat")
    d2c.download_latest_image("image_output.png")
