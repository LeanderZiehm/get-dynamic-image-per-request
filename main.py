from fastapi import FastAPI, Response
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import sqlite3

app = FastAPI()

# Initialize the database
conn = sqlite3.connect("views.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS time_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT
)
""")
conn.commit()

@app.get("/")
def get_time_image():
    # Record the view in the database
    now_dt = datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO time_views (timestamp) VALUES (?)", (now_str,))
    conn.commit()

    # Get total view count
    cursor.execute("SELECT COUNT(*) FROM time_views")
    count = cursor.fetchone()[0]

    # Create a blank image
    img = Image.new("RGB", (500, 120), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)

    # Load a font (default font)
    font = ImageFont.load_default(size=32)

    # Define text positions
    time_text = f"Time: {now_str}"
    views_text = f"Views: {count}"

    # Draw time on top
    draw.text((20, 20), time_text, fill=(255, 255, 255), font=font)
    # Draw views underneath
    draw.text((20, 60), views_text, fill=(255, 255, 255), font=font)

    # Convert to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(content=buffer.getvalue(), media_type="image/png")
