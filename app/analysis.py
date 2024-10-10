# analysis.py
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_network(csv_file, output_folder):
    # Read CSV file
    df = pd.read_csv(csv_file)

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Visualization 1: Distribution of attack labels
    label_counts = df['Label'].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=label_counts.index, y=label_counts.values, palette="viridis")
    plt.title("Distribution of Attack Labels")
    plt.xlabel("Attack Label")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    attack_dist_path = os.path.join(output_folder, 'attack_distribution.png')
    plt.savefig(attack_dist_path, transparent=True)  # Save with a transparent background
    plt.close()

    # Visualization 2: Top Source IPs in the dataset
    top_ips = df['SrcIP'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_ips.index, y=top_ips.values, palette="magma")
    plt.title("Top 10 Source IPs by Frequency")
    plt.xlabel("Source IP")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    top_ips_path = os.path.join(output_folder, 'top_ips.png')
    plt.savefig(top_ips_path, transparent=True)
    plt.close()

    # Visualization 3: Flow Duration Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['FlowDuration'], bins=50, kde=True, color='blue')
    plt.title("Flow Duration Distribution")
    plt.xlabel("Flow Duration")
    plt.ylabel("Frequency")
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    flow_duration_path = os.path.join(output_folder, 'flow_duration.png')
    plt.savefig(flow_duration_path, transparent=True)
    plt.close()

    return {
        'attack_distribution': attack_dist_path,
        'top_ips': top_ips_path,
        'flow_duration': flow_duration_path
    }
