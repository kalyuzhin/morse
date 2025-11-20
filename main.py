import io
import wave
import math
import enum
import struct


class Sign(enum.Enum):
    DASH = "dash"
    DOT = "dot"
    HUSH = "hush"
    SPACE = "space"


ABC: dict[chr, str] = {
    'а': ".-",
    'б': "-...",
    'в': ".--",
    'г': "--.",
    'д': "-..",
    'е': ".",
    'ж': "...-",
    'з': "--..",
    'и': "..",
    'й': ".---",
    'к': "-.-",
    'л': ".-..",
    'м': "--",
    'н': "-.",
    'о': "---",
    'п': ".--.",
    'р': ".-.",
    'с': "...",
    'т': "-",
    'у': "..-",
    'ф': "..-.",
    'х': "....",
    'ц': "-.-.",
    'ч': "---.",
    'ш': "----",
    'щ': "--.-",
    'ы': "-.--",
    'ь': "-..-",
    'э': "..-..",
    'ю': "..--",
    'я': ".-.-",
}

SAMPLE_RATE = 44100
DOT_DURATION = 0.1
DASH_DURATION = DOT_DURATION * 3
PAUSE_BETWEEN_LETTERS = 0.5
PAUSE_BETWEEN_WORDS = 0.5


def create_wave(raw_bytes: bytes) -> None:
    with wave.open('audio.wav', 'wb') as wf:
        wf.setparams((1, 2, SAMPLE_RATE, 0, "NONE", ""))
        wf.writeframes(raw_bytes)


class Signal:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.dot_duration = DOT_DURATION
        self.dash_duration = DASH_DURATION
        self.pause_between_words = PAUSE_BETWEEN_WORDS
        self.pause_between_letters = PAUSE_BETWEEN_LETTERS

    @staticmethod
    def get_sine(amp: float, duration: float, frequency: int) -> float:
        return amp * math.sin(2 * math.pi * duration * frequency)

    @staticmethod
    def convert(ys: list[float]) -> bytes:
        samples = [round(sample * 32767) for sample in ys]
        raw_int = struct.pack("<%dh" % len(samples), *samples)

        return raw_int

    def make_bytes(self, amp: float, frequency: int, input_type: Sign) -> bytes:
        duration: float = self.dot_duration if input_type in (Sign.DOT, Sign.HUSH) else self.dash_duration
        ys: list[float] = []

        for i in range(int(SAMPLE_RATE * duration)):
            t = (i + 0.0) / SAMPLE_RATE
            y = self.get_sine(amp, t, frequency)
            ys.append(y)

        return self.convert(ys)

    @staticmethod
    def make_wave(raw_bytes: bytes) -> None:
        with wave.open('audio.wav', 'wb') as wf:
            wf.setparams((1, 2, SAMPLE_RATE, 0, "NONE", ""))
            wf.writeframes(raw_bytes)

    @staticmethod
    def encode_morse(input_text: str) -> str:
        input_text = input_text.lower()
        buf = io.StringIO()
        for ch in input_text:
            if ch not in ABC:
                return ""
            buf.write(ABC[ch])
            buf.write(' ')

        return buf.getvalue()

    def make_output_sound(self, input_message: str) -> str:
        morse_code = self.encode_morse(input_message)
        b: bytearray = bytearray()

        for ch in morse_code:
            if ch == ".":
                tmp = self.make_bytes(1, 180, Sign.DOT)
            elif ch == "-":
                tmp = self.make_bytes(1, 180, Sign.DASH)
            elif ch == " ":
                tmp = self.make_bytes(0, 180, Sign.SPACE)
            b.extend(tmp)
            tmp = self.make_bytes(0, 180, Sign.HUSH)
            b.extend(tmp)

        self.make_wave(b)

        return morse_code


def main() -> None:
    signal = Signal()
    signal.make_output_sound("Как")
    print("Конец")


if __name__ == "__main__":
    main()
