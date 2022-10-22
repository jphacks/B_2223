import os

src_img_dir = "/content/divide"

if not os.path.exists(src_img_dir):
    os.makedirs(src_img_dir)

!ffmpeg -i "JP_movie.mp4" -vf fps=1 "$src_img_dir/%04d.jpg"
