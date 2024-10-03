import subprocess
import warnings
from functools import lru_cache
from pathlib import Path

import requests
from rich.console import Console
from rich.progress import Progress
from rich.text import Text

from ak_transcribe.utils.config_parser import Config

_config = Config()
console = Console()


class _WhisperParser:
    def __init__(self) -> None:
        self._results: dict | None = None
        self.__mp3path: Path | None = None

    @property
    def txt(self) -> str:
        assert isinstance(self._results, dict), "Results not set yet"
        return "\n".join(
            [line["text"].strip() for line in self._results["segments"]]  # type: ignore
        )

    @property
    def srt(self) -> str:
        assert isinstance(self._results, dict), "Results not set yet"
        count = 0
        text_blob = ""
        for segment in self._results.get("segments", []):
            count += 1
            _timestamp_start: str = f"{count}\n{self.__srt_time(segment['start'])}"
            _timestamp_end: str = f"{self.__srt_time(segment['end'])}\n"
            _text: str = f"{segment['text'].replace('-->', '->').strip()}"
            text_blob += f"{_timestamp_start} --> {_timestamp_end}{_text}\n\n"
        return text_blob

    @staticmethod
    def __srt_time(_seconds: float) -> str:
        """Convert seconds into SRT (SubRip Text) time format."""
        assert _seconds >= 0, "non-negative timestamp expected"
        milliseconds: int = round(_seconds * 1000.0)
        hours: int = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000
        minutes: int = milliseconds // 60_000
        milliseconds -= minutes * 60_000
        seconds: int = milliseconds // 1_000
        milliseconds -= seconds * 1_000
        return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"


class TempMp3:
    def __init__(self, filepath: Path):
        self.__unique_mp3file: bool = False
        self.__mp3path: Path | None = None
        self.__ffmpeg_path: Path | str = Path(
            _config.get(keys=("ffmpeg", "cmd"), default="ffmpeg")
        )
        self.filepath = filepath

    def __enter__(self) -> Path:
        self.__unique_mp3file = self.filepath.suffix.casefold() != ".mp3"
        if self.__unique_mp3file:
            self.__mp3path = self.__convert_to_audio(file=self.filepath)
        else:
            self.__mp3path = self.filepath
        return self.__mp3path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__unique_mp3file and self.__mp3path is not None:
            self.__mp3path.unlink()
        if exc_type is not None:
            console.print(f"[red]An exception occurred:[/red] {exc_type} - {exc_value}")
        return False

    def __convert_to_audio(self, file: Path) -> Path:
        """Convert the given audio file to an MP3 format."""
        outputpath = (
            Path(_config.get(keys=("ffmpeg", "transcode_dir"), default="."))
            / f"{file.stem}.mp3"
        )
        command = f'"{self.__ffmpeg_path}" -loglevel quiet -stats -hide_banner -i "{file}" "{outputpath}" -y'
        with console.status("Converting to MP3...") as status:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode != 0:
                raise Exception("Conversion to `.mp3` failed.")
        console.print(
            f"[green]Conversion successful![/green] Output saved to: {outputpath}"
        )
        return outputpath


class _OpenAI_CPU(_WhisperParser):
    def __init__(self) -> None:
        try:
            import whisper  # type: ignore
        except ModuleNotFoundError:
            raise Exception(
                (
                    "Whisper not installed. "
                    "Install using `pip install openai-whisper@git+https://github.com/openai/whisper.git`"
                )
            )

        model = _config.get(keys=("whisper", "model"), default="small.en")
        device = _config.get(keys=("whisper", "device"), default="cpu")
        self.__whisper = whisper.load_model(model, device=device)
        super().__init__()

    def process(self, filepath: Path):
        """Process the file and save results to `self._results`"""
        with TempMp3(filepath=filepath) as file:
            with warnings.catch_warnings(action="ignore"):
                console.print(f"[yellow]Processing file:[/yellow] {file}")
                self._results = self.__whisper.transcribe(str(file))
                console.print(f"[green]Processing complete![/green]")


class _OpenAI_webserver(_WhisperParser):
    def __init__(self) -> None:
        self.__base_url: str = _config.get(keys=("whisper", "url"), default="")
        assert self.__base_url != "", "Make sure [whisper][url] is set in `config.toml`"
        requests.get(self.__base_url).raise_for_status()

        self.__transcript_url = f"{self.__base_url.rstrip('/')}/asr?encode=true&task=transcribe&word_timestamps=true&output=json"

    def process(self, filepath: Path):
        """Process the file and save results to `self._results`"""
        with TempMp3(filepath=filepath) as file:
            audio_file_path = str(file)
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
            _files = {
                "audio_file": (
                    audio_file_path,
                    audio_data,
                    "audio/mpeg",
                )
            }
            with console.status("Sending request to server...") as status:
                response = requests.post(self.__transcript_url, files=_files)
                response.raise_for_status()
                self._results = response.json()
            console.print(f"[green]Received transcription successfully![/green]")


@lru_cache(maxsize=1)
def _get_processor() -> _OpenAI_webserver | _OpenAI_CPU:
    try:
        return _OpenAI_webserver()
    except Exception as e:
        console.print(f"[red]Web server processor failed:[/red] {e}")
        return _OpenAI_CPU()


Transcriber: _OpenAI_webserver | _OpenAI_CPU = _get_processor()
