def progress_bar(percent):

    percent=float(percent.replace("%",""))

    total=20

    filled=int(percent/100*total)

    bar="█"*filled + "░"*(total-filled)

    return f"[{bar}] {percent:.1f}%"
