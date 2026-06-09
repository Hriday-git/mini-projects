from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col, when, hour, to_timestamp

# ==============================
# 1. CREATE SPARK SESSION
# ==============================
spark = SparkSession.builder.appName("Wildlife IoT Analytics System").getOrCreate()

# ==============================
# 2. LOAD DATASET
# ==============================
df = spark.read.csv("hdfs://localhost:9000/wildlife/wildlife_tracking_2024_expanded.csv", header=True, inferSchema=True)

# Rename column
df = df.withColumnRenamed("forest_region", "forest")

print("\n===== DATA SAMPLE =====")
df.select("animal_id", "species", "forest", "heart_rate", "motion_type").show(5)

# ==============================
# 3. CORE ANALYTICS
# ==============================

print("\n===== BEHAVIOR DISTRIBUTION =====")
df.groupBy("motion_type").count().show()

print("\n===== REGION-WISE ACTIVITY =====")
df.groupBy("forest").count().show()

print("\n===== AVG HEART RATE PER REGION =====")
df.groupBy("forest").agg(avg("heart_rate").alias("avg_heart_rate")).show()

print("\n===== AVG BEHAVIOR DURATION =====")
df.groupBy("motion_type").agg(avg("behavior_duration_hours").alias("avg_duration")).show()

print("\n===== MOST ACTIVE REGIONS =====")
df.groupBy("forest") \
  .agg(count("*").alias("activity_count")) \
  .orderBy(col("activity_count").desc()).show()

print("\n===== SPECIES COUNT PER REGION =====")
df.groupBy("forest", "species").count().show()

# ==============================
# 4. RISK LOGIC
# ==============================

active_motions = ["Running", "Swimming", "Flying", "Jumping", "Climbing"]

df = df.withColumn(
    "risk_flag",
    when((col("heart_rate") > 110) & (col("motion_type").isin(active_motions)), "High Risk")
    .when(col("heart_rate") >= 90, "Medium Risk")
    .otherwise("Normal")
)

print("\n===== RISK DISTRIBUTION =====")
df.groupBy("risk_flag").count().show()

print("\n===== SAMPLE HIGH RISK CASES =====")
df.filter(col("risk_flag") == "High Risk") \
  .select("animal_id", "species", "forest", "heart_rate", "motion_type") \
  .limit(5).show()

# ==============================
# 5. TIME ANALYSIS (FIXED VERSION)
# ==============================

df = df.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"), "dd-MM-yyyy HH:mm")
)

df = df.withColumn("hour", hour("timestamp"))

#  FIX: use Spark range instead of Python list
hours_df = spark.range(0, 24).withColumnRenamed("id", "hour")

hour_counts = df.groupBy("hour").count()

final_hours = hours_df.join(hour_counts, on="hour", how="left").fillna(0)

print("\n===== ACTIVITY BY HOUR (0–23) =====")
final_hours.orderBy("hour").show()

# ==============================
# 6. MACHINE LEARNING
# ==============================

from pyspark.ml.feature import StringIndexer, VectorAssembler

indexer = StringIndexer(inputCol="motion_type", outputCol="motion_index")
df = indexer.fit(df).transform(df)

df = df.withColumn(
    "risk_level",
    when(
        (col("heart_rate") > 110) & (col("motion_type").isin(active_motions)), 2
    ).when(
        (col("heart_rate") >= 90) & (col("temperature") > 36), 1
    ).otherwise(0)
)

assembler = VectorAssembler(
    inputCols=["heart_rate", "temperature", "motion_index"],
    outputCol="features"
)

df = assembler.transform(df)

# ==============================
# 7. TRAIN TEST SPLIT
# ==============================

train, test = df.randomSplit([0.8, 0.2], seed=42)

print("\nTraining Data Count:", train.count())
print("Testing Data Count:", test.count())

# ==============================
# 8. MODEL (logistic regression)
# ==============================

from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(featuresCol="features", labelCol="risk_level", maxIter=10)

model = lr.fit(train)

# ==============================
# 9. PREDICTIONS
# ==============================

predictions = model.transform(test)

print("\n===== logistic Regression Predictions =====")
predictions.select(
    "heart_rate",
    "motion_type",
    col("risk_level").alias("actual_risk"),
    col("prediction").alias("predicted_risk")
).show(15)

# ==============================
# 10. ACCURACY
# ==============================

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(
    labelCol="risk_level",
    predictionCol="prediction",
    metricName="accuracy"
)

accuracy = evaluator.evaluate(predictions)

print("\n===== MODEL ACCURACY =====")
print("Accuracy:", round(accuracy, 3))

# ==============================
# DECISION TREE MODEL
# ==============================

from pyspark.ml.classification import DecisionTreeClassifier

dt = DecisionTreeClassifier(featuresCol="features", labelCol="risk_level", impurity="gini", maxDepth=5)

dt_model = dt.fit(train)

dt_predictions = dt_model.transform(test)

print("\n===== DECISION TREE PREDICTIONS =====")
dt_predictions.select(
    "heart_rate",
    "motion_type",
    col("risk_level").alias("actual"),
    col("prediction").alias("dt_prediction")
).show(15)

dt_accuracy = evaluator.evaluate(dt_predictions)

print("\n===== DECISION TREE ACCURACY =====")
print("DT Accuracy:", round(dt_accuracy, 3))


# ==============================
# RANDOM FOREST MODEL
# ==============================

from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(featuresCol="features", labelCol="risk_level", numTrees=30, maxDepth=5)

rf_model = rf.fit(train)

rf_predictions = rf_model.transform(test)

print("\n===== RANDOM FOREST PREDICTIONS =====")
rf_predictions.select(
    "heart_rate",
    "motion_type",
    col("risk_level").alias("actual"),
    col("prediction").alias("rf_prediction")
).show(15)

rf_accuracy = evaluator.evaluate(rf_predictions)

print("\n===== RANDOM FOREST ACCURACY =====")
print("RF Accuracy:", round(rf_accuracy, 3))

# ==============================
# FINAL MODEL COMPARISON
# ==============================

print("\n===== MODEL COMPARISON =====")

print("Logistic Regression Accuracy:", round(accuracy, 3))
print("Decision Tree Accuracy:", round(dt_accuracy, 3))
print("Random Forest Accuracy:", round(rf_accuracy, 3))

if rf_accuracy >= dt_accuracy and rf_accuracy >= accuracy:
    best_model = "Random Forest"
elif dt_accuracy >= accuracy:
    best_model = "Decision Tree"
else:
    best_model = "Logistic Regression"

print("\n===== BEST MODEL SELECTED =====")
print("Best Model:", best_model)

spark.stop()