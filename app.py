from flask import Flask, render_template
app = Flask(__name__)

tags = ["basics", "diy", "bestof", "doorbell", "explanation", "hardware", "ted"]

playlists = {
  "main": {
    "title": "Общие положения",
    "videos": [0, 5, 6, 7],
    "pic": "1.png"
  },
  "best": {
    "title": "Лучшие проекты",
    "videos": [1, 3, 4],
    "pic": "2.jpg"
  },
  "manuals": {
    "title": "Инструкции",
    "videos": [2, 8, 9],
    "pic": "3.jpg"
  }
}

videos = {
  0: {"id":"0", "title":"How It Works: Internet of Things", "videoid":"QSIPNhOiMoE", "tags":[0, 4]},
  1: {"id":"1", "title":"Top 10 IoT(Internet Of Things) Projects Of All Time | 2018", "videoid":"QL-6PdiDTeo", "tags":[1, 2]},
  2: {"id":"2", "title":"Diy Door Status Notifier", "videoid":"7s0RQDi6wdo", "tags":[1, 5]},
  3: {"id":"3", "title":"Top 5 IoT Hardware Platforms", "videoid":"vZNwkPe3gyQ", "tags":[1, 2, 5]},
  4: {"id":"4", "title":"Top 10 IoT(Internet Of Things) Projects Of All Time | 2019", "videoid":"ZPKDzLcgYOY", "tags":[1, 2, 5]},
  5: {"id":"5", "title":"Internet of Things (IoT) | What is IoT | How it Works | IoT Explained | Edureka", "videoid":"LlhmzVL5bm8", "tags":[4]},
  6: {"id":"6", "title":"Internet Of Things (IOT) easily Explained", "videoid":"MR_-tRnfFgs", "tags":[4]},
  7: {"id":"7", "title":"What is the Internet of Things? And why should you care? | Benson Hougland | TEDxTemecula", "videoid":"_AlcRoqS65E", "tags":[4, 6]},
  8: {"id":"8", "title":"How to make a DIY Smartwatch! || ESP8266 IoT Project", "videoid":"BjgFC0M3iMk", "tags":[1]},
  9: {"id":"9", "title":"DIY IoT Lamp for Home Automation || ESP8266 Tutorial", "videoid":"JzJkT3PNG1Q", "tags":[1]}
}


@app.route('/')
def main():
    output = render_template("main.html", tags_pick=tags, playlists_pick=playlists)
    return output


@app.route('/about')
def about():
    output = render_template("about.html")
    return output


@app.route('/videos/<id>')
def video(id):
    id_int = int(id)
    tag_list = []
    for tag_id in videos[id_int]["tags"]:
        tag_list.append(tags[tag_id])
    output = render_template("video.html", video_name=videos[id_int]["title"], tags=tag_list, videoid=videos[id_int]["videoid"])
    return output

@app.route('/playlists/<playlist_name>/')
def playlist(playlist_name):
    videos_in_playlist = []
    for video_number in playlists[playlist_name]["videos"]:
        videos_in_playlist.append({"id": videos[video_number]["id"], "title": videos[video_number]["title"]})
    if len(playlists[playlist_name]["videos"]) > 1:
        number_in_playlist = '1'
    else:
        number_in_playlist = '0'
    output = render_template("playlist.html", playlist_name_display=playlists[playlist_name]["title"],
                             current_video=videos[playlists[playlist_name]["videos"][0]]["title"],
                             current_videoid=videos[playlists[playlist_name]["videos"][0]]["videoid"],
                             videos_from_playlist=videos_in_playlist,
                             current_playlist=playlist_name,
                             next_number=number_in_playlist)
    return output

@app.route('/playlists/<playlist_name>/<number_in_playlist>/') #добавить обработку несуществующего видео
def playlist_video(playlist_name, number_in_playlist):
    videos_in_playlist = []
    for video_number in playlists[playlist_name]["videos"]:
        videos_in_playlist.append({"id": videos[video_number]["id"], "title": videos[video_number]["title"]})
    print(number_in_playlist)
    print(playlists[playlist_name]["videos"])
    print("number_in_playlist", number_in_playlist)
    print("len playlist", len(playlists[playlist_name]["videos"]))
    if int(number_in_playlist) < len(playlists[playlist_name]["videos"]) - 1:
        number_in_playlist_new = str(int(number_in_playlist)+1)
    else:
        number_in_playlist_new = number_in_playlist
    print(number_in_playlist_new)
    output = render_template("playlist.html", playlist_name_display=playlists[playlist_name]["title"],
                             current_video=videos[playlists[playlist_name]["videos"][int(number_in_playlist)]]["title"],
                             current_videoid=videos[playlists[playlist_name]["videos"][int(number_in_playlist)]]["videoid"],
                             videos_from_playlist=videos_in_playlist,
                             current_playlist=playlist_name,
                             next_number=number_in_playlist_new)
    return output

@app.errorhandler(404)
def page_not_found(error):
   return "Такой страницы нет"


@app.route('/tags/<tag>')
def the_tag(tag):
    if tag in tags:
        tag_number = tags.index(tag)
    videos_for_tag_pick = []
    for video_value in videos.keys():
        if tag_number in videos[video_value]["tags"]:
            video_for_tag = {}
            video_for_tag["id"] = videos[video_value]["id"]
            video_for_tag["name"] = videos[video_value]["title"]
            videos_for_tag_pick.append(video_for_tag)
            print(videos_for_tag_pick)
    output = render_template("tag.html", number_of_videos=len(videos_for_tag_pick), tag_name=tag, videos_for_tag=videos_for_tag_pick)
    return output



app.run('0.0.0.0', 81)