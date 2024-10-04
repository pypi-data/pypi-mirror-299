import pandas as pd
import numpy as np
import re
import warnings
import sys
from .data_preprocessing import DataPreprocessor
from .feature_engineering import FeatureEngineering
from .cluster_scoring import ClusterScoring
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
import plotly.graph_objs as go
from plotly.offline import iplot
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import silhouette_score, silhouette_samples
import time
import warnings
from itertools import cycle, islice
from sklearn import cluster, mixture
import matplotlib.cm as cm
import seaborn as sns


warnings.filterwarnings("ignore", category=FutureWarning)


def display_unique_values(df):
    for column in df.columns:
        unique_values = df[column].unique()
        print(f"Unique values in column '{column}':")
        print(unique_values)
        print(f"Total unique values: {len(unique_values)}")
        print('-' * 50)

def find_columns_with_data(df, patterns):
    """
    Find columns in the dataframe that match the given regex patterns along with their corresponding data.

    Parameters:
    - df: DataFrame
    - patterns: List of regex patterns to search for

    Returns:
    - DataFrame with matched columns and corresponding data
    """
    selected_data = {}
    for col in df.columns:
        for pattern in patterns:
            if re.search(pattern, col, re.IGNORECASE):
                selected_data[col] = df[col].astype('int64', errors='ignore')
                break
    selected_df = pd.DataFrame(selected_data)
    return selected_df
def preprocess_datas(df):
    # Drop non-numeric columns (like 'InvoiceNo') or encode them if necessary
    numerical_df = df.select_dtypes(include=['float', 'int'])

    return numerical_df

def remove_outliers_iqr(df, features):
    for feature in features:
        if pd.api.types.is_numeric_dtype(df[feature]):  # Check if column is numeric
            Q1 = df[feature].quantile(0.25)
            Q3 = df[feature].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[feature] >= lower_bound) & (df[feature] <= upper_bound)]
        else:
            print(f"Skipping non-numeric feature: {feature}")
    return df

def customer_segmentation(df, sample_size=None):
    preprocessed_data = None
    # Define regex patterns for each required column
    column_patterns = {
        'InvoiceNo': [r'invoice\s*no', r'invoice\s*number', r'invoice'],
        'StockCode': [r'stock\s*code', r'stock\s*id', r'product\s*code'],
        'Description': [r'description', r'desc'],
        'Quantity': [r'quantity', r'qty'],
        'InvoiceDate': [r'invoice\s*date', r'date'],
        'UnitPrice': [r'unit\s*price', r'price\s*per\s*unit', r'price'],
        'CustomerID': [r'customer\s*id', r'customer'],
        'Country': [r'country', r'nation']
    }

    # Create a DataFrame with the selected columns and data
    selected_df = find_columns_with_data(df, column_patterns)
    selected_df.isnull().sum()
    selected_df[selected_df['Description'].isnull()]
    selected_df.dropna(subset=['CustomerID'], inplace=True)
    selected_df[selected_df['Description'].isnull()]
    selected_df.isnull().sum()
    selected_df.describe()
    selected_df = selected_df[(selected_df['Quantity'] > 0) & (selected_df['UnitPrice'] > 0)]
    selected_df.describe()
    print("We have", selected_df.duplicated().sum(), "duplicates")

    if not selected_df.empty:  # Check if the selected DataFrame is not empty
        print(selected_df.head())


        # Data Preprocessing
        preprocessor = DataPreprocessor(selected_df)
        print(selected_df.isnull().sum())
        preprocessor.remove_nulls(strategy='mode')  # Check for null values and remove them
        # Add 'Amount' column before feature engineering
        selected_df['Amount'] = selected_df['Quantity'] * selected_df['UnitPrice']

        # Continue with the rest of the data preprocessing
        print(selected_df.isnull().sum())
        preprocessed_data = preprocessor.df

        # Print the preprocessed dataframe
        print("\nPreprocessed Data:")
        print(preprocessed_data.head())
    else:
        print("No matching columns found in the DataFrame.")

    #return preprocessed_data if not selected_df.empty else None
    if 'InvoiceDate' in preprocessed_data.columns:
            preprocessed_data['InvoiceDate'] = pd.to_datetime(preprocessed_data['InvoiceDate'])
    fe = FeatureEngineering(preprocessed_data)

    # Calculate RFM values
    rfm_data = fe.calculate_rfm(customer_id='CustomerID', date_col='InvoiceDate', monetary_col='Amount')

    # Calculate growth values
    growth_data = fe.calculate_growth(customer_id='CustomerID', date_col='InvoiceDate', monetary_col='Amount')

    # Calculate velocity values
    velocity_data = fe.calculate_velocity(customer_id='CustomerID', date_col='InvoiceDate')

    # Display the calculated RFM, growth, and velocity values
    print("RFM Data:")
    print(rfm_data)
    print("\nGrowth Data:")
    print(growth_data)
    print("\nVelocity Data:")
    print(velocity_data)

    numerical_df = preprocessed_data[['InvoiceNo'] + preprocessed_data.select_dtypes(include=['float', 'int']).columns.tolist()]

   # Ensure 'CustomerID' and 'InvoiceNo' are numeric
    numerical_df['CustomerID'] = pd.to_numeric(numerical_df['CustomerID'].astype(str).str.strip(), errors='coerce').astype('float32')

    #numerical_df['InvoiceNo'] = pd.to_numeric(numerical_df['InvoiceNo'].astype(str).str.strip(), errors='coerce').astype('float32')
    # Drop rows with NaN values
    numerical_df = numerical_df.dropna()
    print('numerical df:')
    print(numerical_df.head())
    # Check for duplicate columns
    if numerical_df.columns.duplicated().any():
    # Drop duplicate columns
      numerical_df = numerical_df.loc[:, ~numerical_df.columns.duplicated()]
      print("Duplicate columns were found and removed.")
    else:
      print("No duplicate columns found.")

    # Remove outliers using IQR method
    numerical_df = remove_outliers_iqr(numerical_df, numerical_df.columns)

    # Sample the dataset if sample_size is specified and smaller than the dataset size
    if sample_size and len(numerical_df) > sample_size:
        numerical_df = numerical_df.sample(n=sample_size, random_state=42)

    numer = numerical_df.drop(columns=['CustomerID'])
    cater = preprocessed_data[['Description', 'Country']]

    # Create a dictionary with customer information
    customer_info_dict = preprocessed_data.set_index('CustomerID')[['Description', 'Country']].T.to_dict()

    # Memory usage of categorical variables
    cater_memory = cater.memory_usage(deep=True).sum()
    print(f"Memory usage of categorical variables: {cater_memory / (1024**3):.2f} GB")

    # Encode categorical data with LabelEncoder and store the encoders
    label_encoders = {}
    for col in cater.columns:
        le = LabelEncoder()
        cater[col] = le.fit_transform(cater[col].astype(str))
        label_encoders[col] = le

    # Handle NaN values
    numer.replace([np.inf, -np.inf], np.nan, inplace=True)
    cater.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_numerical_imputed = pd.DataFrame(imputer.fit_transform(numer), columns=numer.columns)
    X_categorical_imputed = pd.DataFrame(imputer.fit_transform(cater), columns=cater.columns)

    # Combine imputed numerical and categorical data
    X_combined = pd.concat([X_numerical_imputed, X_categorical_imputed], axis=1)


    # Drop NaN values from the combined data
    X_combined = X_combined.dropna()
    print('X_combined:')
    print(X_combined.head())

# Check for NaN values after dropping
    if X_combined.isnull().sum().sum() > 0:
        print("NaN values still present after dropping.")
    else:
        print("No NaN values present after dropping.")
        # Scale the combined data
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_combined), columns=X_combined.columns)
    # Perform PCA analysis on the scaled data
    pca_2d = PCA(n_components=2)
    PCs_2d = pd.DataFrame(pca_2d.fit_transform(X_scaled))
    PCs_2d.columns = ["PC1_2d", "PC2_2d"]

    plotX = pd.concat([X_scaled, PCs_2d], axis=1, join='inner')

    # Perform KMeans clustering on the PCA components with 5 clusters
    kmeans_pca = KMeans(n_clusters=5)
    kmeans_pca.fit(PCs_2d)
    plotX['Cluster_PCA'] = kmeans_pca.labels_

    # Visualize clusters in 2D using PCA components with 5 clusters
    trace1_pca = go.Scatter(
        x=plotX[plotX['Cluster_PCA'] == 0]["PC1_2d"],
        y=plotX[plotX['Cluster_PCA'] == 0]["PC2_2d"],
        mode="markers",
        name="Cluster 0",
        marker=dict(color='rgba(255, 128, 255, 0.8)'),
        text=None
    )

    trace2_pca = go.Scatter(
        x=plotX[plotX['Cluster_PCA'] == 1]["PC1_2d"],
        y=plotX[plotX['Cluster_PCA'] == 1]["PC2_2d"],
        mode="markers",
        name="Cluster 1",
        marker=dict(color='rgba(255, 128, 2, 0.8)'),
        text=None
    )

    trace3_pca = go.Scatter(
        x=plotX[plotX['Cluster_PCA'] == 2]["PC1_2d"],
        y=plotX[plotX['Cluster_PCA'] == 2]["PC2_2d"],
        mode="markers",
        name="Cluster 2",
        marker=dict(color='rgba(0, 255, 200, 0.8)'),
        text=None
    )

    trace4_pca = go.Scatter(
        x=plotX[plotX['Cluster_PCA'] == 3]["PC1_2d"],
        y=plotX[plotX['Cluster_PCA'] == 3]["PC2_2d"],
        mode="markers",
        name="Cluster 3",
        marker=dict(color='rgba(100, 100, 200, 0.8)'),
        text=None
    )

    trace5_pca = go.Scatter(
        x=plotX[plotX['Cluster_PCA'] == 4]["PC1_2d"],
        y=plotX[plotX['Cluster_PCA'] == 4]["PC2_2d"],
        mode="markers",
        name="Cluster 4",
        marker=dict(color='rgba(50, 255, 50, 0.8)'),
        text=None
    )

    data_pca = [trace1_pca, trace2_pca, trace3_pca, trace4_pca, trace5_pca]

    title_pca = "Visualizing Clusters in Two Dimensions Using PCA with 5 Clusters"

    layout_pca = dict(title=title_pca,
                    xaxis=dict(title='PC1', ticklen=5, zeroline=False),
                    yaxis=dict(title='PC2', ticklen=5, zeroline=False)
                    )

    fig_pca = dict(data=data_pca, layout=layout_pca)

    iplot(fig_pca)

    clustering_results = ClusterScoring(PCs_2d, kmeans_pca.labels_)
    cluster_details = clustering_results.score_clusters()

    # Access the cluster details for analysis
    print("Cluster Summary:")
    print(cluster_details['Summary'])
    print('--------------------------------------------------')
    print()

    print("Points Within Sigma:")
    print(cluster_details['Points Within Sigma'])
    print('--------------------------------------------------')
    print()

    print("Average Intra-Cluster Distance:")
    print(cluster_details['Average Intra-Cluster Distance'])
    print('--------------------------------------------------')
    print()

    print("Points From Other Clusters:")
    print(cluster_details['Points From Other Clusters'])
    print('--------------------------------------------------')
    print()

    clustering_algorithms = (
    ("MiniBatch\nKMeans", cluster.MiniBatchKMeans(n_clusters=5, random_state=42)),
    ("MeanShift\nKMeans (5 clusters)", cluster.MeanShift(bandwidth=2, bin_seeding=True)), 
    ("DBSCAN\nKMeans (5 clusters)", cluster.DBSCAN(eps=0.3, min_samples=10)),  
    ("Gaussian\nMixture", mixture.GaussianMixture(n_components=5, covariance_type="full", random_state=42)))

    best_silhouette_score = -1
    best_method = ""
    best_clusterer = None
    best_y_pred = None

    # Evaluate all algorithms
    for name, algorithm in clustering_algorithms:
        t0 = time.time()

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            algorithm.fit(X_scaled)

        t1 = time.time()

        # Get cluster labels
        if hasattr(algorithm, "labels_"):
            y_pred = algorithm.labels_.astype(int)
        else:
            y_pred = algorithm.predict(X_scaled)
        # Apply KMeans post-processing for MeanShift and DBSCAN to enforce 5 clusters
        if name.startswith("MeanShift") or name.startswith("DBSCAN"):
            kmeans = cluster.KMeans(n_clusters=5, random_state=42)
            y_pred = kmeans.fit_predict(X_scaled)

        # Calculate Silhouette score
        silhouette_avg = silhouette_score(X_scaled, y_pred)
        print(f"Silhouette Score for {name}: {silhouette_avg:.3f}")

        # Track the best algorithm
        if silhouette_avg > best_silhouette_score:
            best_silhouette_score = silhouette_avg
            best_method = name
            best_clusterer = algorithm
            best_y_pred = y_pred

    # Plot the best clustering result
    # ---- Cluster Visualization Plot ---- #
    plt.figure(figsize=(18, 6))

    # Subplot 1: Cluster Scatter Plot
    plt.subplot(1, 3, 1)
    plt.title(f"{best_method} (Best Method)", size=18)
    sns.set(style="whitegrid")

    palette = sns.color_palette("tab10", n_colors=int(max(best_y_pred) + 1))

    scatter = plt.scatter(
        X_scaled.iloc[:, 0], X_scaled.iloc[:, 1],
        s=100,  # Increase point size for better visibility
        c=[palette[i] for i in best_y_pred],  # Use the color palette for the clusters
        alpha=0.7,  # Add transparency
        edgecolor='k'  # Black border
    )

    for i in np.unique(best_y_pred):
        cluster_points = X_scaled[best_y_pred == i]
        center = cluster_points.mean(axis=0)
        plt.text(center[0], center[1], f"Cluster {i}",
                color="black", fontsize=12, fontweight="bold",
                bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=2))

    plt.xticks([])  
    plt.yticks([])  # Remove ticks

    plt.text(0.99, 0.01, f"Silhouette Score: {best_silhouette_score:.3f}",
            transform=plt.gca().transAxes, size=15, horizontalalignment="right",
            color="black", bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"))

    # ---- Silhouette Plot ---- #
    # Subplot 2: Silhouette Plot
    plt.subplot(1, 3, 2)
    plt.title("Silhouette Plot", size=18)
    sample_silhouette_values = silhouette_samples(X_scaled, best_y_pred)
    y_lower = 10
    for i in np.unique(best_y_pred):
        ith_cluster_silhouette_values = sample_silhouette_values[best_y_pred == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        plt.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=palette[i], edgecolor=palette[i], alpha=0.7)
        plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        y_lower = y_upper + 10  # 10 for space between plots

    plt.axvline(x=best_silhouette_score, color="red", linestyle="--")  # Average silhouette score
    plt.xlabel("Silhouette Coefficient")
    plt.ylabel("Cluster")
    plt.yticks([])  # Clear y-axis labels

    # ---- Distribution Plot ---- #
    # Subplot 3: Cluster Size Distribution
    plt.subplot(1, 3, 3)
    plt.title("Cluster Distribution", size=18)
    unique, counts = np.unique(best_y_pred, return_counts=True)
    sns.barplot(x=unique, y=counts, palette=palette)
    plt.xlabel("Cluster")
    plt.ylabel("Number of points")

    plt.tight_layout()
    plt.show()

    # Output best method and silhouette score
    print(f"\nBest Clustering Method: {best_method} with a Silhouette Score of {best_silhouette_score:.3f}")

    # Use best clustering algorithm to predict labels
    labels = best_clusterer.fit_predict(X_scaled)
# Perform LDA for the best method
    if best_method == "MiniBatch\nKMeans":
        labels = cluster.MiniBatchKMeans(n_clusters=5, random_state=42).fit_predict(X_scaled)
    elif best_method == "MeanShift":
        labels = cluster.MeanShift(bandwidth=2, bin_seeding=True).fit_predict(X_scaled)
    elif best_method == "DBSCAN":
        labels = cluster.DBSCAN(eps=0.3, min_samples=10).fit_predict(X_scaled)
    elif best_method == "Gaussian\nMixture":
        labels = mixture.GaussianMixture(n_components=5, covariance_type="full", random_state=42).fit_predict(X_scaled)

    # Determine the number of classes from clustering results
    n_classes = len(np.unique(labels))

    # Adjust n_components for LDA if necessary
    n_components_lda = min(X_scaled.shape[1], n_classes - 1)

    # Perform LDA with the adjusted n_components
    lda = LDA(n_components=n_components_lda)
    X_lda = lda.fit_transform(X_scaled, labels)

    # Visualize the clusters using LDA-transformed data
    plt.figure(figsize=(10, 8))
    for label in np.unique(labels):
        plt.scatter(X_lda[labels == label, 0], np.zeros_like(X_lda[labels == label, 0]), label=f'Cluster {label}', alpha=0.6)

    plt.title(f'LDA Visualization ({best_method})')
    plt.xlabel('LD1')
    plt.ylabel('LD2')
    plt.legend()
    plt.show()

    # Cluster Scoring
    clustering_results = ClusterScoring(X_scaled, labels)
    cluster_details = clustering_results.score_clusters()

    print("Cluster Summary:")
    print(cluster_details['Summary'])
    print('--------------------------------------------------')
    print()

    print("Points Within Sigma:")
    print(cluster_details['Points Within Sigma'])
    print('--------------------------------------------------')
    print()

    print("Average Intra-Cluster Distance:")
    print(cluster_details['Average Intra-Cluster Distance'])
    print('--------------------------------------------------')
    print()

    print("Points From Other Clusters:")
    print(cluster_details['Points From Other Clusters'])
    print('--------------------------------------------------')
    print()

     # Additional details for best clustering method
    print(f"Number of data points in each cluster for {best_method}:")
    unique, counts = np.unique(labels, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"Cluster {label}: {count} data points")

    # Preparing market basket analysis DataFrame
    market_basket_df = X_combined[['Description','Quantity','UnitPrice','Amount','Country','InvoiceNo']].copy()

    market_basket_df['Cluster'] = labels

    if 'CustomerID' in preprocessed_data.columns:
      market_basket_df['CustomerID'] = preprocessed_data['CustomerID']

      for col in ['Description', 'Country']:
          if col in market_basket_df.columns and col in label_encoders:
              market_basket_df[col] = label_encoders[col].inverse_transform(market_basket_df[col].astype(int))


      # Final failsafe check
      def check_numerical_in_description(df, column_name):
          numeric_descriptions = df[df[column_name].apply(lambda x: bool(re.search(r'\d', str(x))))]
          return numeric_descriptions

      numeric_descriptions = check_numerical_in_description(market_basket_df, 'Description')

      if not numeric_descriptions.empty:
          print("Numeric values found in 'Description' column after reversion:")
          print(numeric_descriptions)
    # Create a dictionary using both CustomerID and InvoiceNo as keys
    invoice_date_map = preprocessed_data.set_index(['CustomerID', 'InvoiceNo'])['InvoiceDate'].to_dict()

    # Create a tuple of (CustomerID, InvoiceNo) in market_basket_df for each row
    market_basket_df['Customer_Invoice_Key'] = list(zip(market_basket_df['CustomerID'], market_basket_df['InvoiceNo']))

    # Map the InvoiceDate based on (CustomerID, InvoiceNo)
    market_basket_df['InvoiceDate'] = market_basket_df['Customer_Invoice_Key'].map(invoice_date_map)

    # Drop the helper column 'Customer_Invoice_Key' after mapping is done
    market_basket_df.drop(columns=['Customer_Invoice_Key'], inplace=True)



    print("Market Basket DataFrame ready for Apriori, FP-Growth, and Eclat analysis.")
    print(market_basket_df.head())
   

    return market_basket_df


# If running as a script, call run_example
if __name__ == "__main__":
    example_df = pd.read_csv("data.csv",encoding='ISO-8859-1')  # Load an example DataFrame from a CSV file
    customer_segmentation(example_df,sample_size=10000)