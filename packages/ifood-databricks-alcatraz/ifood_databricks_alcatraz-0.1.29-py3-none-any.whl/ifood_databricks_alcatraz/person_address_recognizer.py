import logging
from typing import List, Optional
from presidio_analyzer import Pattern, PatternRecognizer
from unidecode import unidecode
import importlib.resources as pkg_resources
from . import resources

logger = logging.getLogger("presidio-analyzer")


class PersonAddressRecognizer(PatternRecognizer):
    """
    Recognize Person names and Addresses.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    This can allow a greater variety in input, for example by removing dashes or spaces.
    """

    PATTERNS = [
        Pattern(
            "Valid word in Portuguese",
            r"\b[a-zA-ZÀ-ÖØ-öø-ÿ]+\b",
            0.01,
        ),
    ]

    CONTEXT = ["rua", "avenida", "alameda", "quadra", "bloco"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "PERSON_OR_ADDRESS",
    ):
        # self.replacement_pairs = (
        #    replacement_pairs if replacement_pairs else [("-", ""), (" ", "")]
        # )

        self.person_or_address_set = set()
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

        with pkg_resources.open_text(resources, "pt_BR_names.txt") as file:
            name_count = 0
            for line in file:
                self.person_or_address_set.add(line.rstrip())
                name_count += 1
            # print(f'Processed names: {name_count} names.')

        with pkg_resources.open_text(resources, "pt_BR_address-words.txt") as file:
            name_count = 0
            for line in file:
                self.person_or_address_set.add(line.rstrip())
                name_count += 1
            # print(f'Processed address words: {name_count}.')

    def validate_result(self, pattern_text: str) -> bool:
        """
        Check if a given pattern_text is a valid person name or address.
        """
        normalized_name = unidecode(pattern_text.lower())
        return normalized_name in self.person_or_address_set
