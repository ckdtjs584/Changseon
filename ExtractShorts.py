from googleapiclient.discovery import build # pip3 install google-api-python-client
import isodate # pip3 install isodate
import tkinter as tk


def get_shorts_from_channel(channel_id):

    # 1. 채널의 업로드 재생목록 ID 가져오기
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2. 업로드 재생목록에서 모든 동영상 가져오기
    videos = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response["items"]:
            videos.append(item["contentDetails"]["videoId"])

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    # 3. 쇼츠 필터링 (길이 <= 60초)
    shorts = []
    for i in range(0, len(videos), 50):  # API 호출당 최대 50개
        video_ids = ",".join(videos[i:i+50])
        video_response = youtube.videos().list(
            part="contentDetails,snippet,statistics",
            id=video_ids
        ).execute()

        for video in video_response["items"]:
            duration = isodate.parse_duration(video["contentDetails"]["duration"]).total_seconds()
            if duration <= 60:  # 쇼츠 조건
                shorts.append({
                    "title": video["snippet"]["title"],
                    "view_count": video["statistics"]["viewCount"]
                })

    return shorts

def quit_root():
    global channel_name
    channel_name = channel_name_entry.get()
    
    root.quit()


if __name__ == "__main__":
    channel_name = ""

    root = tk.Tk()
    channel_name = ""
    channel_name_entry = tk.Entry(root, width=15, relief='solid')
    button_entry = tk.Button(root, width=15, relief='solid', command=quit_root)

    channel_name_entry.pack()
    button_entry.pack()
    root.mainloop()


    DEVELOPER_KEY = 'AIzaSyAGju-uIGYJvpK-jhfhOIEbCGcqGxrbJJ8'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
    q = channel_name,
    order = "relevance",
    part = "snippet",
    maxResults = 1
    ).execute()

    # 채널 아이디 가져오기
    channel_id =search_response['items'][0]['id']['channelId']
    shorts = get_shorts_from_channel(channel_id)

    for short in shorts:
        print(f"제목: {short['title']}, 조회수: {short['view_count']}")


