import io
import wave
import math
import array
import struct

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


def encode_morse(input_text: str) -> str:
    buf = io.StringIO()
    for ch in input_text:
        if ch not in ABC:
            return ""
        buf.write(ABC[ch])
        buf.write(' ')

    return buf.getvalue()


def get_sine(amp: float, duration: float, frequency: int) -> float:
    return amp * math.sin(2 * math.pi * duration * frequency)


def convert(ys: list[float]) -> bytes:
    samples = [round(sample * 32767) for sample in ys]
    raw_int = struct.pack("<%dh" % len(samples), *samples)

    return raw_int


def create_wave(raw_bytes: bytes) -> None:
    with wave.open('audio.wav', 'wb') as wf:
        wf.setparams((1, 2, SAMPLE_RATE, 0, "NONE", ""))
        wf.writeframes(raw_bytes)


def main() -> None:
    duration = float(input("Введите длительность: "))
    arr: list[float] = []
    freq = 440
    amp = 1
    for i in range(int(SAMPLE_RATE * duration)):
        t = (i + 0.0) / SAMPLE_RATE
        y = get_sine(amp, t, freq)
        arr.append(y)
    b = convert(arr)
    create_wave(b)
    print("Файл создан")


if __name__ == "__main__":
    main()
