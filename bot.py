
import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
JAMENDO_CLIENT_ID = os.environ["JAMENDO_CLIENT_ID"]
CHANNEL_ID = "@Remixmmw"

API_URL = "https://api.jamendo.com/v3.0/tracks/"


def find_track():
    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "limit": 50,
        "fuzzytags": "phonk trap",
        "include": "licenses",
        "audioformat": "mp32",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    tracks = response.json().get("results", [])

    for track in tracks:
        license_url = track.get("license_ccurl", "").lower()
        audio_url = track.get("audiodownload", "")

        # فقط مجوزهای قابل بازنشر با ذکر نام هنرمند
        allowed_license = (
            "creativecommons.org/licenses/by/" in license_url
            or "creativecommons.org/licenses/by-sa/" in license_url
        )

        if allowed_license and track.get("audiodownload_allowed") and audio_url:
            return track

    return None


def main():
    track = find_track()

    if not track:
        print("آهنگی با مجوز مناسب پیدا نشد.")
        return

    title = track.get("name", "Phonk")
    artist = track.get("artist_name", "Unknown artist")
    license_url = track.get("license_ccurl", "")
    audio_url = track["audiodownload"]

    caption = (
        f"🎧 {title}\n"
        f"🎤 هنرمند: {artist}\n"
        f"📜 مجوز: {license_url}\n\n"
        "🎵 Для скачивания нажми сюда 👇\n"
        "https://t.me/SpotyBlackBot"
    )

    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"

    result = requests.post(
        api,
        data={
            "chat_id": CHANNEL_ID,
            "audio": audio_url,
            "caption": caption[:1024],
            "title": title[:64],
            "performer": artist[:64],
        },
        timeout=60,
    )
    result.raise_for_status()

    if not result.json().get("ok"):
        raise RuntimeError(result.json())

    print(f"منتشر شد: {title} - {artist}")


if __name__ == "__main__":
    main()

