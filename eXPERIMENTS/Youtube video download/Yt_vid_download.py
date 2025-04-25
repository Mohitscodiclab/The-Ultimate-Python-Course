from pytube import YouTube

def download_video():
    try:
        # Get video URL from user
        video_url = input("Enter YouTube video URL: ").strip()

        # Create YouTube object
        yt = YouTube(video_url)

        # Get the highest quality stream
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

        if not stream:
            print("\n❌ No downloadable video stream found.")
            return
        
        print(f"\n🎬 Downloading: {yt.title} ...")

        # Download video
        stream.download()
        
        print("\n✅ Download completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")

# Run the function
download_video()
