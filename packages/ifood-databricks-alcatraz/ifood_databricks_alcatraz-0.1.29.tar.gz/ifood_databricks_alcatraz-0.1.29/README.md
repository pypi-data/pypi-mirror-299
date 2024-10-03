# iFood Databricks Alcatraz

The iFood Databricks Alcatraz library anonymizes PII data in a Spark DataFrame.
It is designed to be used in Databricks notebooks and jobs.


## Example Usage

To get more examples, check the [`examples`](examples) folder.

```python
from pyspark.sql import SparkSession

from ifood_databricks_alcatraz import IFoodAnonymizer, Entities

# We allocate 4GB of memory to the Spark driver to avoid memory issues with the UDF
# This is a common issue when working with UDFs in Spark locally
spark = SparkSession.builder \
    .appName("AppName") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()


# Data to be included in the DataFrame
data = [
    (
        "John Doe",
        40,
        "São Carlos",
        "My phone is 19 967288744",
        "My cpf is 831.756.690-00",
        "My ip is 200.122.22.1",
        "My email address is john@ee.com",
    ),
    (
        "André Osti",
        30,
        "Campinas",
        "My phone is 21 88367-8333",
        "My cpf is 831.756.690-01",
        "My address 10.22.22.1",
        "My address is andre.doe@gmail.com",
    ),
]

columns = ["Name", "Age", "City", "Phone", "CPF", "IP_ADDRESS", "Email"]

df = spark.createDataFrame(data, columns)

df.show(truncate=False)

anonymizer = IFoodAnonymizer()

entities = [Entities.PHONE_NUMBER]

# Apply the anonymization UDF to the 'Name' column
anonymized_df = anonymizer.anonymize_column(df, "Phone", entities=entities)
anonymized_df = anonymizer.anonymize_column(anonymized_df, "IP_ADDRESS", entities=[Entities.IP_ADDRESS])
anonymized_df = anonymizer.anonymize_column(anonymized_df, "CPF", entities=[Entities.CPF])
anonymized_df = anonymizer.anonymize_column(anonymized_df, "Email", entities=[Entities.EMAIL_ADDRESS])

# Show the results
anonymized_df.show(truncate=False)


```
