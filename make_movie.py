ocr_img_dir = "/content/ocr"

!ffmpeg -framerate 1 -i "$ocr_img_dir/%04d.jpg" "/content/ocr_movie.mp4"

!ffmpeg -i ocr_movie.mp4 -r 30 ocr_movie_30.mp4

!ffmpeg -i JP_movie.mp4 -i ocr_movie_30.mp4 -filter_complex "hstack" out.mp4
