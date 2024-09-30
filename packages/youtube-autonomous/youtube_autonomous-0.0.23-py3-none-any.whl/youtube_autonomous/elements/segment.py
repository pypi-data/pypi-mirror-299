from youtube_autonomous.segments.enums import SegmentField, ElementBuildingField
from youtube_autonomous.elements.enhancement import Enhancement
from youtube_autonomous.elements.validator.element_validator import StringDuration
from youtube_autonomous.elements.rules.effect_element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode
from youtube_autonomous.segments.enhancement.edition_manual.edition_manual import EditionManual
from youtube_autonomous.elements.element import Element
from yta_general_utils.logger import print_completed
from bson.objectid import ObjectId
from typing import Union


class Segment(Element):
    @property
    def status(self):
        return super().status
    
    @status.setter
    def status(self, status: str):
        super().status = status

        if self._do_update_database:
            self.database_handler.update_project_segment_status(self.project_id, self.index, status)

    @property
    def audio_filename(self):
        return super().audio_filename
    
    @audio_filename.setter
    def audio_filename(self, audio_filename: Union[str, None]):
        super().audio_filename = audio_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.AUDIO_FILENAME.value, audio_filename)

    @property
    def video_filename(self):
        return super().video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        super().video_filename = video_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.VIDEO_FILENAME.value, video_filename)

    @property
    def full_filename(self):
        return super().full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        super().full_filename = full_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.FULL_FILENAME.value, full_filename)

    @property
    def audio_narration_filename(self):
        return super().audio_narration_filename
    
    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        super().audio_narration_filename = audio_narration_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, SegmentField.AUDIO_NARRATION_FILENAME.value, audio_narration_filename)

    @property
    def transcription(self):
        return super().transcription
    
    @transcription.setter
    def transcription(self, transcription: Union[dict, None]):
        super().transcription = transcription

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.TRANSCRIPTION.value, transcription, transcription)

    @property
    def shortcodes(self):
        return super().shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: Union[list[Shortcode], None]):
        super().shortcodes = shortcodes

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.SHORTCODES.value, shortcodes)

    @property
    def calculated_duration(self):
        return super().calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[float, int, None]):
        super().calculated_duration = calculated_duration

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, ElementBuildingField.CALCULATED_DURATION.value, calculated_duration)

    def __init__(self, project_id: Union[str, ObjectId], index: int, data: dict):
        super().__init__(index, data)

        self._do_update_database = False

        self.project_id = str(project_id)
        
        # TODO: This should go in 'self.data' (?)
        self.enhancements = []
        for index, enhancement in enumerate(data.get('enhancements', [])):
            self.enhancements.append(Enhancement(self.project_id, self, index, enhancement))

        self._do_update_database = True

    def validate(self):
        super().validate()

        # If 'enhancements' are invalid
        # TODO: self.enhancements doesn't exist yet
        for enhancement in self.enhancements:
            RulesChecker.check_need_rules(enhancement, ElementRules.get_subclass_by_type(enhancement['type']))

    # TODO: Remove this method below
    def prepare(self):
        # Check duration
        if self.data.duration and not self.calculated_duration:
            self.calculated_duration = self.data.duration

        # Generate narration audio
        if self.rules_checker.should_build_narration_rule(self.data) and not self.audio_clip:
            self.handle_narration()

        # Generate video
        if not self.video_clip:
            self.video_clip = self.builder.build_segment(self)
            # We write this video part to be able to recover it in the future
            segment_part_filename = self.__create_segment_file('video.mp4')
            self.video_clip.write_videofile(segment_part_filename)
            self.video_filename = segment_part_filename
            print_completed('Created basic video part and stored locally and in database.')

    # TODO: This below has to be in the common Object from wich Segment
    # and Enhancement will inherit
    def build_step_1_create_narration(self):
        # 1. Generate narration if needed
        self.handle_narration()

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
        filename = self.__create_segment_file('video.mov')
        self.video_clip.write_videofile(filename)
        self.video_filename = filename

    def build_step_5_update_enhancements_duration(self):
        # 5. Update enhancements duration according to base video
        # TODO: What if 'start' is after the end of the base video (?)
        for enhancement in self.enhancements:
            if enhancement['duration'] == StringDuration.SEGMENT_DURATION.value:
                enhancement['duration'] = self.video_clip.duration

            if enhancement['start'] >= self.video_clip.duration:
                raise Exception('The enhancement start moment is after the video_clip.duration')
            
    def build_step_6_build_enhancements(self):
        for enhancement in self.enhancements:
            enhancement_clip = enhancement.build(self)
            # TODO: Combine with our segment according to type

    def build(self):
        self.build_step_1_create_narration()
        self.build_step_2_extract_user_shortcodes()
        self.build_step_3_apply_edition_manual_shortcodes()
        self.build_step_4_build_base_content()
        self.build_step_5_update_enhancements_duration()
        self.build_step_6_build_enhancements()

    def apply_edition_manual(self):
        # TODO: I need to dynamically get the edition manual from somewhere
        # By now I'm forcing it
        test_edition_manual = 'C:/Users/dania/Desktop/PROYECTOS/youtube-autonomous/youtube_autonomous/segments/enhancement/edition_manual/example.json'
        edition_manual = EditionManual.init_from_file(test_edition_manual)
        enhancements = edition_manual.apply(self)
        print(enhancements)
        # TODO: Some enhancements could be incompatible
        self.enhancements += enhancements
        # TODO: What about this enhancements (?)


  