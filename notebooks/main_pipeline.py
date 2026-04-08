# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Main Data Pipeline
# MAGIC
# MAGIC This notebook demonstrates a simple data pipeline that:
# MAGIC 1. Creates a sample sales dataset
# MAGIC 2. Applies transformations (categorization, calculations)
# MAGIC 3. Saves the result as a temporary view
# MAGIC
# MAGIC In a real project, this would read from a data lake and write to a warehouse.

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# Step 1: Create a sample sales dataset
# In production, this would be: spark.read.table("raw.sales")
df_raw = (
    spark.range(1000)
    .withColumn("sale_amount", (F.col("id") % 500).cast("double") + 10)
    .withColumn("region", F.when(F.col("id") % 3 == 0, "North")
                           .when(F.col("id") % 3 == 1, "South")
                           .otherwise("East"))
)

print(f"Raw records: {df_raw.count()}")
display(df_raw.limit(5))

# COMMAND ----------

# Step 2: Apply business transformations
df_transformed = (
    df_raw
    # Categorize sale amounts
    .withColumn("sale_category",
        F.when(F.col("sale_amount") >= 300, "high")
         .when(F.col("sale_amount") >= 100, "medium")
         .otherwise("low"))
    # Calculate tax (10%)
    .withColumn("tax", F.round(F.col("sale_amount") * 0.10, 2))
    # Calculate total with tax
    .withColumn("total", F.round(F.col("sale_amount") + F.col("tax"), 2))
)

print(f"Transformed records: {df_transformed.count()}")
display(df_transformed.limit(5))

# COMMAND ----------

# Step 3: Save as a temp view (in production, write to a Delta table)
df_transformed.createOrReplaceTempView("pipeline_output")

print("Pipeline completed successfully!")
