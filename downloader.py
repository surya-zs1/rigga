import yt_dlp
import os

DOWNLOAD_DIR="/downloads"


def get_formats(url):

    with yt_dlp.YoutubeDL({"quiet":True}) as ydl:

        info=ydl.extract_info(url,download=False)

    formats=[]

    for f in info["formats"]:

        if f.get("height"):

            formats.append({
                "id":f["format_id"],
                "res":f"{f['height']}p"
            })

    return formats[:6]


def download_video(url,format_id,progress_hook):

    def hook(d):

        if d["status"]=="downloading":

            percent=d.get("_percent_str","0%")
            speed=d.get("_speed_str","0")
            eta=d.get("_eta_str","0")

            progress_hook(percent,speed,eta)

    ydl_opts={
        "format":format_id,
        "outtmpl":f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "progress_hooks":[hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([url])
