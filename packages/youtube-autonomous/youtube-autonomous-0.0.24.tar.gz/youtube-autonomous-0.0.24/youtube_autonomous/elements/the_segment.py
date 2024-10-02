from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.validator.element_validator import StringDuration
from youtube_autonomous.segments.enhancement.edition_manual.edition_manual import EditionManual
from youtube_autonomous.elements.enhancement import Enhancement
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER
from yta_multimedia.audio.voice.transcription.stt.whisper import get_transcription_with_timestamps
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.temp import get_temp_filename
from yta_general_utils.logger import print_completed
from moviepy.editor import AudioFileClip, VideoFileClip


class Segment:
    index: int
    status = ""

    audio_filename: str
    audio_clip = None
    video_filename: str
    video_clip = None
    full_filename: str
    full_clip = None

    audio_narration_filename: str
    voice: str
    narration_text: str

    text: str

    duration: float = None

    filename: str
    url: str

    calculated_duration: float = None
    narration_text_sanitized_without_shortcodes: str
    narration_text_with_simplified_shortcodes: str
    narration_text_sanitized: str
    transcription = None
    shortcodes = None

    @property
    def audio_filename(self):
        return self.audio_filename

    @audio_filename.setter
    def audio_filename(self, audio_filename):
        self.audio_filename = audio_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.audio_filename:
            self.audio_clip = AudioFileClip(self.video_filename)

    @property
    def video_filename(self):
        return self.video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename):
        self.video_filename = video_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.video_filename:
            self.video_clip = VideoFileClip(self.video_filename)

    @property
    def full_filename(self):
        return self.full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename):
        self.full_filename = full_filename

        # TODO: Check is valid or reset (in database) and raise
        # Exception (?)
        if self.full_filename:
            self.video_clip = VideoFileClip(self.full_filename)

    def __init__(self, project_id, index: int, data: dict):
        self.project_id = project_id
        self.index = index

        for key in data:
            self[key] = data[key]

        self.rules = ElementRules.get_subclass_by_type(data['type'])()
        self.builder = ElementBuilder.get_subclass_by_type(data['type'])()
        self.rules_checker = RulesChecker(self.rules)

        self.database_handler = DatabaseHandler()
        # TODO: Set shortcode tags please (read Notion)
        self.shortcode_parser = ShortcodeParser([])

    # TODO: This below has been moved because inheritance is working strangely

    def create_segment_file(self, filename: str):
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
    
    def create_narration(self):
        """
        Creates the audio narration (if needed) by generating an AI audio
        narration with provided 'voice' and 'audio_narration_text'
        parameters or by using the 'audio_narration_filename'.

        This method will set the 'audio_filename' to be able to build the
        audio clip in a near future.
        """
        if self.audio_narration_filename:
            segment_part_filename = self.create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
            copy_file(self.audio_narration_filename, segment_part_filename)
            print_completed('Original voice narration file copied to segment parts folder')
            self.audio_narration_filename = segment_part_filename
            self.audio_filename = segment_part_filename
        else:
            segment_part_filename = self.create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            self.audio_filename = self.builder.build_narration(self.narration_text_sanitized_without_shortcodes, output_filename = segment_part_filename)
            print_completed('Voice narration created successfully')

    def create_transcription(self):
        """
        Creates the transcription of the generated audio narration
        that would be stored in 'self.audio_filename'.
        
        This method returns a words array containing, for each word,
        a 'text', 'start' and 'end' field to be able to use the 
        transcription timestamps.
        """
        transcription = get_transcription_with_timestamps(self.audio_filename, initial_prompt = self.narration_text_sanitized_without_shortcodes)

        # We join all words together as we don't need segments, just words with time
        words = []
        for transcription_segment in transcription['segments']:
            words += transcription_segment['words']
        self.transcription = words

    # TODO: This above has been moved because inheritance is working strangely

    # TODO: This below has to be in the common Object from wich Segment
    # and Enhancement will inherit
    def build_step_1_create_narration(self):
        # 1. Generate narration if needed
        self.create_narration()

    def build_step_2_create_transcription(self):
        # 2. Generate narration transcription
        self.create_transcription()

    def build_step_2_extract_user_shortcodes(self):
        # 2. Extract manually written shortcodes in 'narration_text'
        self.shortcode_parser.parse(self.narration_text)
        self.shortcodes = self.shortcode_parser.shortcodes
        # TODO: Turn shortcodes into enhancements
        enhancements = [shortcode.to_enhancement_element(self.transcription) for shortcode in self.shortcodes]
        print(enhancements)

    def build_step_3_apply_edition_manual_shortcodes(self):
        # 3. Apply shortcodes from Edition Manual and 'narration_text'
        self.apply_edition_manual()

    def build_step_4_build_base_content(self):
        # 4. Build base video
        self.video_clip = self.builder.build_from_segment(self)
        filename = self.create_segment_file('video.mp4')
        self.video_clip.write_videofile(filename)
        self.video_filename = filename

    def build_step_5_update_enhancements_duration(self):
        # 5. Update enhancements duration according to base video
        # TODO: What if 'start' is after the end of the base video (?)
        for enhancement in self.enhancements:
            if enhancement.duration == StringDuration.SEGMENT_DURATION.name:
                enhancement.duration = self.video_clip.duration

            if enhancement.start >= self.video_clip.duration:
                raise Exception('The enhancement start moment is after the video_clip.duration')
            
            end = enhancement.start + enhancement.duration
            if end > self.video_clip.duration:
                enhancement.duration = self.video_clip.duration - enhancement.start
            
    def build_step_6_build_enhancements(self):
        for enhancement in self.enhancements:
            enhancement_clip = enhancement.build()
            # TODO: Combine with our segment according to type

    def build(self):
        if self.rules_checker.should_build_narration_rule(self):
            if not self.audio_filename:
                self.build_step_1_create_narration()

            # We are forcing duration here
            self.duration = self.audio_clip.duration

            if not self.transcription:
                self.build_step_2_create_transcription()

            # TODO: Handle this (maybe status (?))
            self.build_step_2_extract_user_shortcodes()

            self.build_step_3_apply_edition_manual_shortcodes()

        # TODO: What about duration here that is not set (?)
        if self.audio_clip:
            self.calculated_duration = self.audio_clip.duration

        print(self.video_clip)
        
        if not self.video_clip:
            print('Building base content step 4')
            self.build_step_4_build_base_content()

        # Make the base video to apply enhancements on it
        if self.audio_clip:
            self.video_clip = self.video_clip.set_audio(self.audio_clip)

        self.build_step_5_update_enhancements_duration()
        self.build_step_6_build_enhancements()

    def apply_edition_manual(self):
        # TODO: I need to dynamically get the edition manual from somewhere
        # By now I'm forcing it
        test_edition_manual = 'C:/Users/dania/Desktop/PROYECTOS/youtube-autonomous/youtube_autonomous/segments/enhancement/edition_manual/example.json'
        edition_manual = EditionManual.init_from_file(test_edition_manual)
        dict_enhancements_found = edition_manual.apply(self.transcription)
        # Turn dict enhancements found into Enhancement objects
        for index, dict_enhancement_found in enumerate(dict_enhancements_found):
            # TODO: What do we do with 'index' here (?)
            print(type(dict_enhancement_found))
            index = 100 + index
            self.enhancements.append(Enhancement(self.project_id, self.index, index, dict_enhancement_found))
        # TODO: Some enhancements could be incompatible due to collisions
        # or things like that

        # TODO: What about this enhancements (?)
