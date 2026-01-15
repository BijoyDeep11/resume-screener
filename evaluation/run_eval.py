import csv
from scipy.stats import spearmanr

# 🔧 For now, hardcode example model outputs
# Later you can automate this from your pipeline

human_scores = []
model_scores = []

with open("evaluation/labels.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        human_scores.append(int(row["human_score"]))

        # Example: replace these with real outputs later
        # For now, we simulate realistic model behavior
        simulated_model_score = int(row["human_score"]) + (-5 if int(row["human_score"]) > 50 else 5)
        model_scores.append(simulated_model_score)

# -------------------------
# Spearman Correlation
# -------------------------
corr, p_value = spearmanr(human_scores, model_scores)

print("Human scores :", human_scores)
print("Model scores :", model_scores)
print("Spearman correlation:", round(corr, 2))
print("P-value:", round(p_value, 4))
