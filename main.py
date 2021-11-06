from fastapi import FastAPI, Header
from fastapi.responses import Response
from os import getcwd, path

app = FastAPI()

PORTION_SIZE = 1024 * 1024

current_directory = getcwd() + "/"

@app.get("/video/{name_video}")
def get_video(name_video: str, range: str = Header(None)):
    # bytes=0-
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(start + PORTION_SIZE)

    # LEEMOS LA POSICION EXACTA DEL ARCHIVO

    with open(current_directory + name_video, "rb") as myfile:
        myfile.seek(start)
        data = myfile.read(end - start)
        size_video = str(path.getsize(current_directory + name_video))

        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{size_video}',
            'Accept-Ranges': 'bytes'
        }
        return Response(content=data, status_code=206, headers=headers, media_type="video/mp4")