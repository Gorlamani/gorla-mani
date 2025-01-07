from flask import Flask, render_template, request, jsonify
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Pexels API for videos
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"  # Replace with your API key
PEXELS_VIDEO_API = "https://api.pexels.com/videos/search"

# Example videos from Pexels
DEMO_VIDEOS = {
    'anime': {
        'english': [
            'https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c0fd273d2c6d9a064f3ae35579b2bbdf&profile_id=139&oauth2_token_id=57447761',
            'https://player.vimeo.com/external/403295268.sd.mp4?s=3446f36ca57399e7bf3d5f760688eb8c9a9069fb&profile_id=139&oauth2_token_id=57447761'
        ]
    },
    'cinematic': {
        'english': [
            'https://player.vimeo.com/external/434045526.sd.mp4?s=c27595335c6cf1e0ce4a0937b26e38493b20c7d1&profile_id=139&oauth2_token_id=57447761',
            'https://player.vimeo.com/external/446766429.sd.mp4?s=c175355bbf182c4dd2892f195b4650cc58a3b540&profile_id=139&oauth2_token_id=57447761'
        ]
    }
}

# Example music from public sources
DEMO_MUSIC = {
    'electronic': {
        'english': [
            'https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6ff1bab.mp3',
            'https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3'
        ]
    },
    'classical': {
        'english': [
            'https://cdn.pixabay.com/download/audio/2022/02/22/audio_c8c0c57202.mp3',
            'https://cdn.pixabay.com/download/audio/2022/02/07/audio_d0c6a2c483.mp3'
        ]
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate/music', methods=['POST'])
def generate_music():
    try:
        genre = request.json.get('genre', 'electronic')
        language = request.json.get('language', 'english')
        
        # Get available songs for the genre and language
        available_songs = DEMO_MUSIC.get(genre, {}).get(language, [])
        if not available_songs:
            return jsonify({"error": f"No {genre} music available in {language}"})
            
        # Select a random song
        selected_song = random.choice(available_songs)
        
        return jsonify({
            "status": "success",
            "music": {
                "url": selected_song,
                "genre": genre,
                "language": language,
                "mood": "energetic",
                "duration": "1:30",
                "waveform": "https://www.soundviz.com/sites/default/files/2020-10/waveform-soundviz-black-background.png"
            }
        })
    except Exception as e:
        print(f"Music error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate/video', methods=['POST'])
def generate_video():
    try:
        style = request.json.get('style', 'anime')
        language = request.json.get('language', 'english')
        prompt = request.json.get('prompt', '')
        
        # Get available videos for the style and language
        available_videos = DEMO_VIDEOS.get(style, {}).get(language, [])
        if not available_videos:
            return jsonify({"error": f"No {style} videos available in {language}"})
            
        # Select a random video
        selected_video = random.choice(available_videos)
        
        return jsonify({
            "status": "success",
            "video": {
                "url": selected_video,
                "thumbnail": "https://i.vimeocdn.com/video/371433846_295x166.jpg",
                "style": style,
                "language": language,
                "prompt": prompt
            }
        })
    except Exception as e:
        print(f"Video error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
