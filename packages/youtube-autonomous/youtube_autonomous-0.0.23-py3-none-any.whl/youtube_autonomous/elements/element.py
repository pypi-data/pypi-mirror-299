from youtube_autonomous.elements.element_data import ElementData
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.logger import print_completed
from moviepy.editor import AudioFileClip, VideoFileClip
from typing import Union


class Element:
    @property
    def type(self):
        return self.data.type

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index: int):
        self._index = index

    @property
    def status(self):
        return self.data.status
    
    @status.setter
    def status(self, status: str):
        self.data.status = status

    @property
    def audio_filename(self):
        audio_filename = self.data.audio_filename

        if audio_filename and not self.audio_clip:
            self.audio_clip = AudioFileClip(audio_filename)

        return audio_filename
    
    @audio_filename.setter
    def audio_filename(self, audio_filename: Union[str, None]):
        self.data.audio_filename = audio_filename

        if self.data.audio_filename:
            self.audio_clip = AudioFileClip(self.data.audio_filename)

    @property
    def video_filename(self):
        video_filename = self.data.video_filename

        if video_filename and not self.video_clip:
            self.video_clip = VideoFileClip(video_filename)

        return video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        self.data.video_filename = video_filename

        if self.data.video_filename:
            self.video_clip = VideoFileClip(self.data.video_filename)

    @property
    def full_filename(self):
        full_filename = self.data.full_filename

        if full_filename and not self.full_clip:
            self.full_clip = VideoFileClip(full_filename)

        return full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        self.data.full_filename = full_filename

        if self.data.full_filename:
            self.full_clip = VideoFileClip(self.data.full_filename)

    @property
    def audio_narration_filename(self):
        return self.data.audio_narration_filename
    
    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        self.data.audio_narration_filename = audio_narration_filename

    @property
    def transcription(self):
        return self.data.transcription
    
    @transcription.setter
    def transcription(self, transcription: Union[dict, None]):
        self.data.transcription = transcription

    @property
    def shortcodes(self):
        return self.data.shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: Union[list['Shortcode'], None]):
        self.data.shortcodes = shortcodes

    @property
    def calculated_duration(self):
        return self.data.calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[float, int, None]):
        self.data.calculated_duration = calculated_duration

    @property
    def text(self):
        return self.data.text
    
    @property
    def narration_text(self):
        return self.data.narration_text
    
    def __init__(self, index: int, data: dict):
        self.index = index
        self.data = ElementData(data)
        self.rules = ElementRules.get_subclass_by_type(data['type'])
        self.builder = ElementBuilder.get_subclass_by_type(data['type'])
        self.rules_checker = RulesChecker(self.rules)

        self.database_handler = DatabaseHandler()
        self.shortcode_parser = ShortcodeParser()

    def __create_segment_file(self, filename: str):
        """
        Creates a filename within the definitive segments folder
        to keep the generated file locally to recover it in the
        next project execution if something goes wrong. The 
        definitive filename will be built using the provided
        'filename' and adding some more information in the name.

        This method will generate a temporary filename that uses
        the current segment index in its name and is placed in 
        segment parts folder.

        This method returns the final filename created.
        """
        if not filename:
            raise Exception('No "filename" provided.')

        temp_filename = get_temp_filename(filename)

        return f'{DEFAULT_SEGMENT_PARTS_FOLDER}/segment_{self.index}_{temp_filename}'
    
    def validate(self):
        """
        Validates that the main data of the Element is correctly
        set, all required fields are provided, there are no
        unexpected shortcodes and more stuff.

        This method will raise an Exception if something is wrong.
        """
        # TODO: Move this to a external validator (?)
        # If 'text' have shortcodes
        self.shortcode_parser.parse(self.text)

        # If 'narration_text' have invalid shortcodes
        self.shortcode_parser.parse(self.narration_text)

        # If element has not necessary parameters
        self.rules_checker.check_this_need_rules(self.data)

    def handle_narration(self):
        """
        Handles the audio narration by using the 'audio_narration_filename'
        if provided or by generating an AI audio narration with 'voice' and
        'audio_narration_text'.

        This method will set the 'audio_filename' to be able to build the
        audio clip in a near future.
        """
        if self.audio_narration_filename:
            segment_part_filename = self.__create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
            copy_file(self.audio_narration_filename, segment_part_filename)
            print_completed('Original voice narration file copied to segment parts folder')
            self.audio_narration_filename = segment_part_filename
            self.audio_filename = segment_part_filename
        else:
            segment_part_filename = self.__create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            self.audio_filename = self.builder.build_narration(self.data.narration_text_sanitized_without_shortcodes, output_filename = segment_part_filename)
            print_completed('Voice narration created successfully')