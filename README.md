# sweetube
Sweetest YouTube ever. Developed for KAIST CS489 (Computer Ethics).

## Usage

Install poetry and run `make init` first, to install dependencies and pretrained model.

```sh
python ./cli.py YOUR_YOUTUBE_URL_OR_VIDEO_ID
```

OR


```sh
make run
curl http://127.0.0.1:5000/videos/<video_id>
```

(Recommend running the server rather than using cli. It might take quite a long time...)
