import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = "https://anubhav.cognitiveservices.azure.com/"
    key =  ""
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Get a caption for the image. This will be a synchronously (blocking) call.
result = client.analyze_from_url(
    image_url="https://miro.medium.com/v2/resize:fit:1200/1*EcjtaXo5HUVfIObxs0-I3A.jpeg",
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
    gender_neutral_caption=True,  # Optional (default is False)
)

print("Image analysis results:")
# Print caption results to the console
print(" Caption:")
if result.caption is not None:
    print(f"{result.caption.text}")

# Print text (OCR) analysis results to the console
print(" Read:")
if result.read is not None:
    for line in result.read.blocks[0].lines:
        print(f"Line: {line.text}")
        for word in line.words:
            print(f"{word.text}")