from youtube_autonomous.shortcodes.enums import ShortcodeType
from typing import Union


class ShortcodeTag:
    """
    Class that represent a shortcode tag to implement with
    the ShortcodeParser. This is just to let the parser know
    if it is a block-scoped shortcode tag, a simple shortcode
    tag and some more information needed.
    """
    def __init__(self, tag: str, type: Union[ShortcodeType, str]):
        """
        Initializes a shortcode tag object. The 'tag' parameter represents
        the shortcode name [tag], and the 'type' parameter is to point if
        the shortcode includes some text inside it [tag] ... [/tag] or if
        it is a simple one [tag].
        """
        if not tag:
            raise Exception('No "tag" provided.')
        
        if not type:
            raise Exception('No "type" provided.')

        if not isinstance(tag, str):
            raise Exception('Provided "tag" is not a string.')
        
        if not isinstance(type, (ShortcodeType, str)):
            raise Exception('Provided "type" is not a ShortcodeType.')
        
        if isinstance(type, str):
            if not ShortcodeType.is_valid(type):
                raise Exception('The "type" parameter provided is not a valid ShortcodeType string value.')
            
            type = ShortcodeType(type)
        
        self.tag = tag
        self.type = type

    def is_block_scoped(self):
        """
        Returns True if the shortcode is a block scoped one, that
        should look like this: [tag] ... [/tag], or False if not.
        """
        return self.type == ShortcodeType.BLOCK

