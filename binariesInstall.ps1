echo "----------------------------------------------------------------------------------------------------------------------"
echo "Welcome to vtunes. This installer will download the FFMPEG & yt-dlp binary for you automatically in utils/. Please ensure you have enough space and a stable internet connection."
echo "----------------------------------------------------------------------------------------------------------------------"

cd utils

echo "Starting download for FFMPEG..."

curl.exe -L 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -o 'ffmpeg.zip' -#
Expand-Archive .\ffmpeg.zip
Remove-Item .\ffmpeg.zip

Get-ChildItem -Recurse -Path "./ffmpeg" -Filter *.exe | ForEach-Object {
    Move-Item $_.FullName -Destination "./ffmpeg"
}
Get-ChildItem -Recurse -Path "./ffmpeg" -Exclude "*.exe" | Remove-Item -Force -Recurse

echo "FFMPEG Binary successfully downloaded."
echo "Starting download for yt-dlp..."

New-Item -Path '.\yt-dlp' -ItemType Directory
curl.exe -L 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe' -o '.\yt-dlp\yt-dlp.exe' --silent -#

echo "YT-DLP Binary successfully downloaded."
pause