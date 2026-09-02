"""
EcoCart Customer Segmentation
K-Means clustering with urban/rural bias detection and mitigation.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

SEGMENT_NAMES = {0: 'High-Value Urban', 1: 'Mid-Value Suburban', 2: 'Low-Frequency Rural'}


def generate_customer_data(n=200, biased=True):
    """
    Generate synthetic customer data.
    biased=True  → Urban customers over-represented (80/10/10 split)
    biased=False → Balanced split (34/33/33)
    """
    rng = np.random.default_rng(seed=7)
    if biased:
        urban_n, suburban_n, rural_n = int(n * 0.8), int(n * 0.1), n - int(n * 0.8) - int(n * 0.1)
    else:
        urban_n = suburban_n = rural_n = n // 3
        rural_n += n - (urban_n + suburban_n + rural_n)

    # Urban: high purchase freq, high spend, low distance
    urban = rng.multivariate_normal([8, 250, 5], [[2, 0, 0], [0, 1500, 0], [0, 0, 4]], urban_n)
    # Suburban
    suburban = rng.multivariate_normal([5, 130, 20], [[2, 0, 0], [0, 800, 0], [0, 0, 25]], suburban_n)
    # Rural: in biased mode, add extra noise so rural gets misclassified more
    rural_cov_scale = 8 if biased else 1
    rural = rng.multivariate_normal(
        [2, 60, 80],
        [[rural_cov_scale, 0, 0], [0, 400 * rural_cov_scale, 0], [0, 0, 100]],
        rural_n,
    )

    X = np.vstack([urban, suburban, rural])
    X = np.clip(X, [0, 0, 0], [20, 1000, 200])
    labels_true = (
        ['Urban'] * urban_n + ['Suburban'] * suburban_n + ['Rural'] * rural_n
    )
    return X, labels_true


def run_segmentation(biased=True):
    X, true_labels = generate_customer_data(n=210, biased=biased)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = km.fit_predict(X_scaled)

    # Rename clusters by mean purchase frequency (ascending)
    cluster_means = [X[clusters == c, 0].mean() for c in range(3)]
    order = np.argsort(cluster_means)  # low freq → high freq
    cluster_label_map = {order[0]: 'Low-Frequency Rural',
                         order[1]: 'Mid-Value Suburban',
                         order[2]: 'High-Value Urban'}

    customers = []
    for i, (row, c, tl) in enumerate(zip(X, clusters, true_labels)):
        customers.append({
            'id': i + 1,
            'purchase_freq': round(float(row[0]), 1),
            'avg_spend': round(float(row[1]), 2),
            'distance_km': round(float(row[2]), 1),
            'cluster': int(c),
            'segment': cluster_label_map[c],
            'true_group': tl,
        })

    # Distribution stats
    total = len(customers)
    dist = {}
    for seg in cluster_label_map.values():
        count = sum(1 for c in customers if c['segment'] == seg)
        dist[seg] = {'count': count, 'pct': round(count / total * 100, 1)}

    # Bias metrics: rural representation rate
    rural_customers = [c for c in customers if c['true_group'] == 'Rural']
    rural_correctly_segmented = sum(1 for c in rural_customers if 'Rural' in c['segment'])
    rural_rate = round(rural_correctly_segmented / len(rural_customers) * 100, 1) if rural_customers else 0

    urban_customers = [c for c in customers if c['true_group'] == 'Urban']
    urban_correctly_segmented = sum(1 for c in urban_customers if 'Urban' in c['segment'])
    urban_rate = round(urban_correctly_segmented / len(urban_customers) * 100, 1) if urban_customers else 0

    return {
        'customers': customers[:50],   # return sample for display
        'distribution': dist,
        'bias_metrics': {
            'urban_accuracy': urban_rate,
            'rural_accuracy': rural_rate,
            'biased_dataset': biased,
            'total_customers': total,
        },
        'mitigation': {
            'applied': not biased,
            'strategy': 'Re-sampling: equalise Urban/Suburban/Rural representation in training data',
        }
    }
