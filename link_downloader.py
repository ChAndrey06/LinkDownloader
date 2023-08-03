import aiohttp
from bs4 import BeautifulSoup
from pytube import YouTube

from io import BytesIO


class LinkDownloader:
    TiktokDownloaderUrl = 'https://savetik.co/api/ajaxSearch'
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    async def get_download_link(self, url: str, url_type: str) -> str | None:
        match url_type:
            case 'tiktok':
                return await self._download_tiktok(url)
            case 'youtube':
                return await self._download_youtube(url)
            case _:
                return None

    async def _download_tiktok(self, url):
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': self.UserAgent}
            data = {'q': url, 'lang': 'en'}

            async with session.post(self.TiktokDownloaderUrl, headers=headers, data=data) as response:
                if response.status != 200:
                    return None

                json_data = await response.json()
                html_content = json_data.get('data')

                if not html_content:
                    return None

                soup = BeautifulSoup(html_content, 'html.parser')
                download_link_tag = soup.find(
                    'a', class_='tik-button-dl button dl-success')

                if not download_link_tag:
                    return None

                return download_link_tag.get('href')

    async def _download_youtube(self, url):
        buffer = BytesIO()
        
        YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first().stream_to_buffer(buffer)

        return buffer
    
        # audio_stream = YouTube(url).streams.filter(only_audio=True).order_by('abr').desc().first()
        # audio_stream.download()

        # return audio_stream.get_file_path()


async def main():
    tiktok_downloader = LinkDownloader()
    url = 'https://vm.tiktok.com/ZGJb1sCmc/'
    download_link = await tiktok_downloader.get_download_link(url)
    print('Download link:', download_link)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
