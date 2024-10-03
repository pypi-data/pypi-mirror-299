from enum import Enum
from typing import List, Optional

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from pyspark.sql import DataFrame, SparkSession, Column
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

from .person_address_recognizer import PersonAddressRecognizer
from .cpf_recognizer import CPFRecognizer
from .phone_br_recognizer import PhoneBRRecognizer


class Entities(Enum):
    """
    The entities to be anonymized
    """

    CPF = "CPF"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    BR_PHONE_NUMBER = "BR_PHONE_NUMBER"
    IP_ADDRESS = "IP_ADDRESS"
    PERSON_OR_ADDRESS = "PERSON_OR_ADDRESS"


class IFoodAnonymizer:
    """
    Anonymize the personal information in a DataFrame column
    """

    def __init__(self):
        """
        Initialize the anonymizer
        """

        # Uncomment the following code to use the Spacy models
        """configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "en", "model_name": "en_core_web_lg"},
                {"lang_code": "pt", "model_name": "pt_core_news_lg"},
            ],
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)

        nlp_engine = provider.create_engine()
        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine, supported_languages=["en", "pt"]
        )
        """

        self.analyzer = AnalyzerEngine()
        self.analyzer.registry.add_recognizer(CPFRecognizer())
        self.analyzer.registry.add_recognizer(PhoneBRRecognizer())
        self.analyzer.registry.add_recognizer(PersonAddressRecognizer())
        self.anonymizer = AnonymizerEngine()

    def anonymize_dataframe_column(
        self, df: DataFrame, column: str, entities: Optional[List[Entities]] = None
    ) -> DataFrame:
        """
        Anonymize the personal information in a DataFrame column
        :param df: The target DataFrame
        :param column: The target column of the DataFrame
        :param entities: The entities to be anonymized
        :return: A DataFrame containing the anonymized data
        """
        spark = SparkSession.builder.getOrCreate()
        sc = spark.sparkContext

        broadcasted_analyzer = sc.broadcast(self.analyzer)
        broadcasted_anonymizer = sc.broadcast(self.anonymizer)

        if not isinstance(df.schema[column].dataType, StringType):
            raise ValueError("Column must be of StringType")

        # By default, anonymize all entities
        entities = entities or [
            Entities.CPF,
            Entities.EMAIL_ADDRESS,
            Entities.BR_PHONE_NUMBER,
            Entities.IP_ADDRESS,
            Entities.PERSON_OR_ADDRESS,
        ]

        for entity in entities:
            if not hasattr(entity, "name"):
                raise ValueError(
                    "Invalid entity. The available entities are: {}".format(
                        [e.name for e in Entities]
                    )
                )
            if not hasattr(Entities, entity.name):
                raise ValueError(
                    "Invalid entity. The available entities are: {}".format(
                        [e.name for e in Entities]
                    )
                )

        def anonymize_text(text, entity_type, replacement):
            language = "en"

            if text is None:
                return text

            if entity_type == Entities.EMAIL_ADDRESS and "@" not in text:
                return text
            if entity_type == Entities.BR_PHONE_NUMBER and not any(
                char.isdigit() for char in text
            ):
                return text
            if entity_type == Entities.IP_ADDRESS and not any(
                char.isdigit() for char in text
            ):
                return text
            if entity_type == Entities.CPF and sum(c.isdigit() for c in text) < 11:
                return text

            analyzer = broadcasted_analyzer.value
            anonymizer = broadcasted_anonymizer.value
            results = analyzer.analyze(
                text=text, entities=[entity_type.value], language=language
            )
            anonymized_result = anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators={
                    "DEFAULT": OperatorConfig("replace", {"new_value": replacement})
                },
            )
            return anonymized_result.text

        anonymization_udfs = {
            "BR_PHONE_NUMBER": udf(
                lambda text: anonymize_text(
                    text, Entities.BR_PHONE_NUMBER, "<ANONYMIZED_PHONE>"
                ),
                StringType(),
            ),
            "EMAIL_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.EMAIL_ADDRESS, "<ANONYMIZED_EMAIL>"
                ),
                StringType(),
            ),
            "IP_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.IP_ADDRESS, "<ANONYMIZED_IP_ADDRESS>"
                ),
                StringType(),
            ),
            "CPF": udf(
                lambda text: anonymize_text(text, Entities.CPF, "<ANONYMIZED_CPF>"),
                StringType(),
            ),
            "PERSON_OR_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.PERSON_OR_ADDRESS, "<ANONYMIZED_PERSON_OR_ADDRESS>"
                ),
                StringType(),
            ),
        }

        for entity in entities:
            df = df.withColumn(column, anonymization_udfs[entity.name](df[column]))

        return df

    def anonymize_column(
        self, df_col: Column, entities: Optional[List[Entities]] = None
    ) -> Column | None:
        """
        Anonymize the personal information in a DataFrame column
        :param df_col: The target DataFrame column
        :param entities: The entities to be anonymized
        :return: Column containing the anonymized data
        """
        if df_col is None:
            return None

        # By default, anonymize all entities
        entities = entities or [
            Entities.CPF,
            Entities.EMAIL_ADDRESS,
            Entities.BR_PHONE_NUMBER,
            Entities.IP_ADDRESS,
            Entities.PERSON_OR_ADDRESS,
        ]

        if not all(isinstance(entity, Entities) for entity in entities):
            raise ValueError(
                "Invalid entity. The available entities are: {}".format(
                    [e.name for e in Entities]
                )
            )

        spark = SparkSession.builder.getOrCreate()
        sc = spark.sparkContext

        broadcasted_analyzer = sc.broadcast(self.analyzer)
        broadcasted_anonymizer = sc.broadcast(self.anonymizer)

        def anonymize_text(text, entity_type, replacement):
            language = "en"

            if text is None or not isinstance(text, str):
                return text

            if entity_type == Entities.EMAIL_ADDRESS and "@" not in text:
                return text
            if entity_type == Entities.BR_PHONE_NUMBER and not any(
                char.isdigit() for char in text
            ):
                return text
            if entity_type == Entities.IP_ADDRESS and not any(
                char.isdigit() for char in text
            ):
                return text
            if entity_type == Entities.CPF and sum(c.isdigit() for c in text) < 11:
                return text

            analyzer = broadcasted_analyzer.value
            anonymizer = broadcasted_anonymizer.value
            results = analyzer.analyze(
                text=text, entities=[entity_type.value], language=language
            )
            anonymized_result = anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators={
                    "DEFAULT": OperatorConfig("replace", {"new_value": replacement})
                },
            )
            return anonymized_result.text

        anonymization_udfs = {
            "BR_PHONE_NUMBER": udf(
                lambda text: anonymize_text(
                    text, Entities.BR_PHONE_NUMBER, "<ANONYMIZED_PHONE>"
                ),
                StringType(),
            ),
            "EMAIL_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.EMAIL_ADDRESS, "<ANONYMIZED_EMAIL>"
                ),
                StringType(),
            ),
            "IP_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.IP_ADDRESS, "<ANONYMIZED_IP_ADDRESS>"
                ),
                StringType(),
            ),
            "CPF": udf(
                lambda text: anonymize_text(text, Entities.CPF, "<ANONYMIZED_CPF>"),
                StringType(),
            ),
            "PERSON_OR_ADDRESS": udf(
                lambda text: anonymize_text(
                    text, Entities.PERSON_OR_ADDRESS, "<ANONYMIZED_PERSON_OR_ADDRESS>"
                ),
                StringType(),
            ),
        }

        for entity in entities:
            df_col = anonymization_udfs[entity.name](df_col)

        return df_col
