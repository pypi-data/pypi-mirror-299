import doctest


def test_delme():
    r"""

"""


    """
>>> import pyttsx3
>>> engine = pyttsx3.init()
>>> engine.save_to_file('Hello. How are you doing?', 'hello.wav')
>>> engine.runAndWait()  # The computer creates hello.wav.
>>> import os;assert os.path.exists('hello.wav') # TEST VERIFY
>>> import os;os.unlink('hello.wav')  # TEST CLEAN UP

>>> import whisper
>>> model = whisper.load_model('base')
>>> result = model.transcribe('audio.mp3')
>>> DUMMY = result['text']
>>> write_function = whisper.utils.get_writer('srt', '.')
>>> write_function(result, 'audio')
>>> import os;assert os.path.exists('audio.srt') # TEST VERIFY
>>> import os;os.unlink('audio.srt')  # TEST CLEAN UP


    """

if __name__ == '__main__':
    doctest.testmod()

