# SweeTube
Sweetest YouTube ever. Developed for 2020 Fall KAIST CS489 (Computer Ethics).

## Project Tree
```
.
├── chrome                    # React base Chrome Extension
│   └── src                   # source code folder
├── sweetube                  # Caption handling Web server 
├── pyproject.toml            # Package dependency
└── README.md
```
## Load SweeTube To your Chrome
```
cd ./chrome
yarn install
yarn build
```
Now you can load `build` directory to your Chrome. Watch [This Document](https://developer.chrome.com/docs/extensions/mv2/getstarted/#manifest) to see how to load built chrome extension.

After you run web server on local, you can try SweeTube.
## Web Server Usage

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
