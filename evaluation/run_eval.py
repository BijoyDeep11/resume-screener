from scipy.stats import spearmanr

human_scores = [70, 40, 90, 60, 30]
model_scores = [65, 45, 85, 55, 35]

corr, _ = spearmanr(human_scores, model_scores)

print("Spearman correlation:", round(corr, 2))
