import pandas as pd
from mlxtend.frequent_patterns import fpgrowth,apriori, association_rules

def eclat(df, min_support=0.04):
    rows_count = len(df)
    frequent_itemsets = {}

    # Initial pass: get frequent 1-itemsets
    for column in df.columns:
        support = df[column].sum() / rows_count
        if support >= min_support:
            frequent_itemsets[frozenset([column])] = support
    # Iteratively generate k-itemsets
    k = 2
    current_itemsets = list(frequent_itemsets.keys())

    while current_itemsets:
        next_itemsets = []
        for i in range(len(current_itemsets)):
            for j in range(i + 1, len(current_itemsets)):
                combined_itemset = current_itemsets[i] | current_itemsets[j]
                if len(combined_itemset) == k:
                    support = (df[list(combined_itemset)].all(axis=1).sum()) / rows_count
                    if support >= min_support:
                        frequent_itemsets[combined_itemset] = support
                        next_itemsets.append(combined_itemset)
        k += 1
        current_itemsets = next_itemsets

    # Convert to DataFrame
    frequent_itemsets_df = pd.DataFrame(list(frequent_itemsets.items()), columns=['itemsets', 'support'])
    return frequent_itemsets_df

def generate_association_rules(table, min_support=0.02, metric="lift", min_threshold=2, target_rule_count=20):
    current_support = min_support
    rules = pd.DataFrame()  # Initialize an empty DataFrame for rules

    while len(rules) < target_rule_count and current_support > 0:
        # Generate frequent itemsets
        frequent_itemsets = apriori(table, min_support=current_support, use_colnames=True)

        # If no frequent itemsets are found, decrease support further
        if frequent_itemsets.empty:
            print(f"No frequent itemsets found with min_support={current_support}. Reducing min_support...")
            current_support -= 0.001
            continue  # Skip the rest of the loop and try again

        # Generate rules from the frequent itemsets
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)

        # If sufficient rules are found, break the loop
        if len(rules) >= target_rule_count:
            print(f"Found {len(rules)} rules with min_support={current_support}.")
            break

        # If not enough rules, reduce min_support and try again
        current_support -= 0.001
        #print(f"Reducing min_support to {current_support}...")

    if rules.empty:
        print("No rules found even after adjusting min_support.")

    return rules

def generate_fpgrowth_rules(table: pd.DataFrame, min_support: float = 0.02, metric: str = "lift", min_threshold: float = 2):
    frequent_itemsets = fpgrowth(table, min_support=min_support, use_colnames=True)
    fpgrowth_rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    return fpgrowth_rules

def generate_eclat_rules(table: pd.DataFrame, min_support: float = 0.02, metric: str = "lift", min_threshold: float = 2):
    frequent_itemsets = eclat(table, min_support=min_support)
    print(frequent_itemsets)
    eclat_rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    return eclat_rules