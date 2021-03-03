import base64
import requests
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

apiKey=config.get('credentials', 'apiKey')


def UploadImage(image_url):
    #with open(filePath, "rb") as file:
        #url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": apiKey,
        "image": image_url,
        "expiration":60
    }
    res = requests.post("https://api.imgbb.com/1/upload", payload)
        
    if res.status_code == 200:
        print("Server Response: " + str(res.status_code))
        print("Image Successfully Uploaded ")
        final_url = res.json()['data']['url']
    else:
        print("ERROR")
        print("Server Response: " + str(res.status_code))

    return final_url


def imgbb_main(image_url):
    print("imgBB API Uploader")
    print("API Key: " + apiKey)
    #fileLocation = req.iter_content(8192)
    final_url = UploadImage(image_url)
    return final_url


if __name__ == '__main__':
    main()
