import logging
from typing import List, Optional
from presidio_analyzer import Pattern, PatternRecognizer
import re

logger = logging.getLogger("presidio-analyzer")


class PhoneBRRecognizer(PatternRecognizer):
    """
    Recognize Brazilian Mobile Phone Numbers.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    This can allow a greater variety in input, for example by removing dashes or spaces.
    """

    PATTERNS = [
        Pattern(
            "Número de telefone celulares no Brasil",
            # r"(\+?55)?(\d{2})?\d{5}-?\d{4}\b",
            r"(\+?55)?\s?(\(\d{2,3}\))?\s?(\d{2})?\s?(\d{4,5})-?\s?\d{4}",
            0.01,
        ),
    ]

    CONTEXT = ["telefone", "número", "celular"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "BR_PHONE_NUMBER",
    ):
        # self.replacement_pairs = (
        #    replacement_pairs if replacement_pairs else [("-", ""), (" ", "")]
        # )
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    def validate_result(self, pattern_text: str) -> bool:
        """
        Check if a Brazilian Mobile Phone Number is valid.
        """

        phone_number = "".join(re.findall(r"\d", pattern_text))

        if len(phone_number) < 8:
            return False

        if len(phone_number) >= 9:
            # In Brazil, mobile phone numbers start with 9 or 8
            if phone_number[-9] == "9" or phone_number[-9] == "8":
                return True

        elif len(phone_number) == 8:
            # Non-mobile phones and corner cases of mobile phones
            #    ("My phone is (51) 9 9559-7959  test1 test2", 1),
            #    ("My phone is (18)3217-3161 test1 test2", 1),
            if phone_number[-8] == "3" or phone_number[-8] == "9":
                return True

        return False
