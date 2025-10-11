from fastapi import FastAPI, Response
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

app = FastAPI()

@app.get("/time-image")
def get_time_image():
    # Current time and date
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a blank image
    img = Image.new("RGB", (400, 100), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)

    # Load a font (fallback to default if unavailable)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 32)
    except:
        font = ImageFont.load_default()

    # Draw the text
    draw.text((20, 30), now, fill=(255, 255, 255), font=font)

    # Convert to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return as image response
    return Response(content=buffer.getvalue(), media_type="image/png")
