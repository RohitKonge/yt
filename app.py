from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_file = None
    if request.method == 'POST':
        url = request.form['url']
        unique_id = str(uuid.uuid4())[:8]  # To avoid filename conflicts
        ydl_opts = {
            'format': 'bestvideo[height=1080]+bestaudio/best[height=1080]',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'%(title)s_{unique_id}.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            video_file = f"{title}_{unique_id}.mp4"
    return render_template('index.html', video_file=video_file)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
