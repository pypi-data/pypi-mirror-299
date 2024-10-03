import logging
from typing import List, Optional
from presidio_analyzer import Pattern, PatternRecognizer
import re

logger = logging.getLogger("presidio-analyzer")


class CPFRecognizer(PatternRecognizer):
    """
    Recognize Brazilian CPF number.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    This can allow a greater variety in input, for example by removing dashes or spaces.
    """

    PATTERNS = [
        Pattern(
            "Cadastro de Pessoa Física (CPF) - 1",
            r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            0.01,
        ),
    ]

    CONTEXT = ["cpf", "número cpf", "cadastro de pessoa física"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CPF",
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

    def validate_result(self, pattern_text: str) -> bool:  # noqa D102
        """
        Check if a CPF number is valid.
        """
        cpf = "".join(re.findall(r"\d", pattern_text))
        if len(cpf) != 11:
            return False

        # Check if all CPF digits are the same
        if len(set(cpf)) == 1:
            return False

        # Check first CPF check digit
        sum = 0
        for i in range(9):
            sum += int(cpf[i]) * (10 - i)
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[9]):
            return False

        # Check second CPF check digit
        sum = 0
        for i in range(10):
            sum += int(cpf[i]) * (11 - i)
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[10]):
            return False

        return True
