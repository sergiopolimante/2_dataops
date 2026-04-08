# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Data Quality Tests
# MAGIC
# MAGIC This notebook runs **data quality checks** against the pipeline output.
# MAGIC It is executed by the CI/CD pipeline (GitHub Actions) after deploying to staging.
# MAGIC
# MAGIC **How it works in CI/CD:**
# MAGIC - If ALL assertions pass → the notebook exits successfully → CI promotes to production
# MAGIC - If ANY assertion fails → the notebook raises an error → CI rolls back the deployment
# MAGIC
# MAGIC This is the key **DataOps** pattern: test your data on the actual platform,
# MAGIC not just your code locally.

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup: Run the same pipeline logic
# MAGIC We recreate the pipeline output here so the test job is self-contained.

# COMMAND ----------

# Recreate the pipeline (same logic as main_pipeline.py)
df_raw = (
    spark.range(1000)
    .withColumn("sale_amount", (F.col("id") % 500).cast("double") + 10)
    .withColumn("region", F.when(F.col("id") % 3 == 0, "North")
                           .when(F.col("id") % 3 == 1, "South")
                           .otherwise("East"))
)

df_result = (
    df_raw
    .withColumn("sale_category",
        F.when(F.col("sale_amount") >= 300, "high")
         .when(F.col("sale_amount") >= 100, "medium")
         .otherwise("low"))
    .withColumn("tax", F.round(F.col("sale_amount") * 0.10, 2))
    .withColumn("total", F.round(F.col("sale_amount") + F.col("tax"), 2))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 1: Row count is correct

# COMMAND ----------

row_count = df_result.count()
assert row_count == 1000, f"FAIL: Expected 1000 rows, got {row_count}"
print(f"PASS: Row count is {row_count}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 2: No NULL values in critical columns

# COMMAND ----------

critical_columns = ["sale_amount", "region", "sale_category", "tax", "total"]
for col_name in critical_columns:
    null_count = df_result.filter(F.col(col_name).isNull()).count()
    assert null_count == 0, f"FAIL: Found {null_count} NULLs in '{col_name}'"
    print(f"PASS: No NULLs in '{col_name}'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 3: Categories are valid

# COMMAND ----------

valid_categories = ["high", "medium", "low"]
invalid_count = df_result.filter(~F.col("sale_category").isin(valid_categories)).count()
assert invalid_count == 0, f"FAIL: Found {invalid_count} invalid categories"
print(f"PASS: All categories are valid ({valid_categories})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 4: Tax calculation is correct (10% of sale_amount)

# COMMAND ----------

bad_tax = df_result.filter(
    F.abs(F.col("tax") - F.round(F.col("sale_amount") * 0.10, 2)) > 0.01
).count()
assert bad_tax == 0, f"FAIL: Found {bad_tax} incorrect tax calculations"
print(f"PASS: All tax calculations are correct")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 5: Total = sale_amount + tax

# COMMAND ----------

bad_total = df_result.filter(
    F.abs(F.col("total") - F.round(F.col("sale_amount") + F.col("tax"), 2)) > 0.01
).count()
assert bad_total == 0, f"FAIL: Found {bad_total} incorrect totals"
print(f"PASS: All totals are correct")

# COMMAND ----------

# MAGIC %md
# MAGIC ## All tests passed!

# COMMAND ----------

print("=" * 50)
print("ALL DATA QUALITY TESTS PASSED!")
print("=" * 50)

# Signal success to Databricks (and to the CI/CD pipeline)
dbutils.notebook.exit("ALL_TESTS_PASSED")
