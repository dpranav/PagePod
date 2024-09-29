import os
import requests
from crewai_tools import tool

# Define the custom tool
@tool
def image_search_tool(summary: str, output_dir: str = "./downloaded_images") -> str:
    """
    Custom CrewAI tool that searches and downloads 10 images based on the summary provided.
    
    Args:
        summary (str): The 75-word summary for image search.
        output_dir (str): Directory to save the downloaded images.
    
    Returns:
        str: Path to the downloaded images.
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the Serper.dev API endpoint and headers
    api_url = "https://google.serper.dev/images"
    api_key = os.getenv("SERPER_API_KEY")  # Make sure to set the API key in your environment

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # Prepare the request payload with the search query (summary)
    payload = {
        "q": summary,
        "num": 10  # Limit to 10 images
    }

    # Make the request to the Serper.dev API
    response = requests.post(api_url, headers=headers, json=payload)

    # Check for successful response
    if response.status_code != 200:
        return f"Error: Unable to fetch images. Status code: {response.status_code}"

    # Extract image URLs from the API response
    image_data = response.json().get("images", [])
    if not image_data:
        return "No images found."

    image_paths = []

    # Loop through the image URLs and download them
    for idx, image_info in enumerate(image_data):
        image_url = image_info.get("thumbnailUrl") or image_info.get("url")
        if not image_url:
            continue

        # Download the image
        try:
            img_data = requests.get(image_url).content
            image_path = os.path.join(output_dir, f"image_{idx+1}.jpg")
            with open(image_path, 'wb') as img_file:
                img_file.write(img_data)
            image_paths.append(image_path)
        except Exception as e:
            print(f"Failed to download image {idx+1}: {e}")

    # Return the paths to the downloaded images
    if image_paths:
        return f"Images saved to {output_dir}. Paths: {', '.join(image_paths)}"
    else:
        return "Failed to download any images."
