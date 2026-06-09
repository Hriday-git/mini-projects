# Wildlife IoT Data Analysis using Hadoop & PySpark
Analyzes wildlife tracking data from IoT sensors to identify animal behavior patterns, monitor health conditions, detect high-risk situations, and generate conservation insights.

## Tech Stack
- Python, PySpark, Apache Spark
- Apache Hadoop (HDFS)
- WSL (Ubuntu), VS Code

## Features
- Behavior & region-wise activity analysis
- Heart rate and behavior duration monitoring
- Risk detection system (High / Medium / Normal)
- Species distribution and most active region identification
- ML-based risk prediction (Logistic Regression, Decision Tree, Random Forest)
- Auto-selects best performing model by accuracy

## Risk Detection Logic
| Risk Level | Condition                                                                      |
| High       | Heart Rate > 110 or motion is Running / Swimming / Flying / Jumping / Climbing |
| Medium     | Heart Rate ≥ 90                                                                |
| Normal     | All other conditions                                                           |

## How to Run
```bash
git clone <repository-url>
cd wildlife_project
python3 -m venv pyspark-env
source pyspark-env/bin/activate
pip install -r requirements.txt
python3 analysis.py
```

## Demo
<img width="1918" height="917" alt="Screenshot 2026-05-03 194619" src="https://github.com/user-attachments/assets/9b78a5f2-42cb-46cc-b4e1-9c9fd235ccbf" />
<img width="1909" height="902" alt="Screenshot 2026-05-03 194643" src="https://github.com/user-attachments/assets/e717b788-8a17-452a-9798-92c83feadbb6" />
<img width="1480" height="794" alt="Screenshot 2026-05-03 194722" src="https://github.com/user-attachments/assets/bdfc04a3-2f6f-465d-a4a5-13abd7aef9b5" />
<img width="1452" height="844" alt="Screenshot 2026-05-03 194831" src="https://github.com/user-attachments/assets/5ed923ed-6e3c-4c69-910c-6cc7b364bca1" />




## Author
Hriday Pipalia 
