from fastapi import FastAPI, Response, Depends
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal

# Create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_time_image(response: Response, db: Session = Depends(get_db)):
    now_dt = datetime.now()

    # Record the view
    new_view = models.TimeView(timestamp=now_dt)
    db.add(new_view)
    db.commit()

    # Get total view count
    count = db.query(models.TimeView).count()

    # Create an image
    img = Image.new("RGB", (500, 120), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)
    font_size = 32
    font = ImageFont.load_default(size=font_size)

    time_text = f"Time: {now_dt.strftime('%Y-%m-%d %H:%M:%S')}"
    views_text = f"Views: {count}"

    draw.text((20, 20), time_text, fill=(255, 255, 255), font=font)
    draw.text((20, 60), views_text, fill=(255, 255, 255), font=font)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    return Response(content=buffer.getvalue(), media_type="image/png", headers=headers)
