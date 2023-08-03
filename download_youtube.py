from pytube import YouTube


class DownloadYoutube:
    pass


async def main():
    yt = YouTube('https://music.youtube.com/watch?v=Yk9K2ifx7bw&list=RDAMVMYk9K2ifx7bw')
    print(yt.streams.filter(only_audio=True).order_by('abr').desc().first().url)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())