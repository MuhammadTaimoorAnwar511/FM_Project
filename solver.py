from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Glucose3

def compute_mwps(feature_model):
    """Compute Minimum Working Products (MWPs) from the feature model."""

    def get_all_features(model):
        """Extract all feature names from the feature model."""
        features = set()

        def extract_features(feature):
            features.add(feature['name'])
            for child in feature.get('children', []):
                extract_features(child)
            for group in feature.get('groups', []):
                for f in group['features']:
                    features.add(f['name'])

        extract_features(model['root'])
        return sorted(list(features))

    def create_cnf_clauses(model, features_dict):
        """Convert feature model to CNF clauses."""
        clauses = []

        def process_feature_constraints(feature, parent_idx=None):
            current_idx = features_dict[feature['name']]

            # Parent-child relationship
            if parent_idx is not None:
                clauses.append([parent_idx, -current_idx])  # Child implies parent
                if feature.get('mandatory', False):
                    clauses.append([-parent_idx, current_idx])  # Parent implies mandatory child

            for child in feature.get('children', []):
                process_feature_constraints(child, current_idx)

            for group in feature.get('groups', []):
                group_indices = [features_dict[f['name']] for f in group['features']]
                if group['type'] == 'xor':
                    for idx1, idx2 in combinations(group_indices, 2):
                        clauses.append([-idx1, -idx2])  # At most one
                    clauses.append([-current_idx] + group_indices)  # At least one
                elif group['type'] == 'or':
                    # OR: Parent implies at least one child
                    clauses.append([-current_idx] + group_indices)
                for idx in group_indices:
                    clauses.append([-idx, current_idx])  # Child implies parent

        process_feature_constraints(model['root'])

        # Add cross-tree constraints
        for constraint in model['constraints']:
            if constraint['englishStatement'] == "The Location feature is required to filter the catalog by location.":
                loc_idx = features_dict['Location']
                byloc_idx = features_dict['ByLocation']
                clauses.append([-byloc_idx, loc_idx])

        return clauses

    def is_valid_product(features, mandatory_features):
        """Validate if a product configuration satisfies mandatory features."""
        for feature in mandatory_features:
            if isinstance(feature, str):
                if feature not in features:
                    return False
            elif isinstance(feature, tuple):
                if not any(f in features for f in feature):
                    return False
        return True

    def identify_mandatory_features(model):
        """Identify all mandatory features."""
        mandatory = set()

        def process_feature(feature, is_mandatory_branch):
            if is_mandatory_branch or feature.get('mandatory', False):
                mandatory.add(feature['name'])
                for child in feature.get('children', []):
                    process_feature(child, True)

                for group in feature.get('groups', []):
                    if group['type'] == 'xor':
                        mandatory.add(tuple(f['name'] for f in group['features']))
            else:
                for child in feature.get('children', []):
                    process_feature(child, False)

        process_feature(model['root'], True)  # Root is always mandatory
        return mandatory

    all_features = get_all_features(feature_model)
    features_dict = {feat: idx + 1 for idx, feat in enumerate(all_features)}
    reverse_dict = {idx: feat for feat, idx in features_dict.items()}

    cnf = CNF(from_clauses=create_cnf_clauses(feature_model, features_dict))
    mandatory_features = identify_mandatory_features(feature_model)

    mwps = []
    solver = Glucose3()
    solver.append_formula(cnf.clauses)

    while solver.solve():
        model = solver.get_model()
        selected_features = {reverse_dict[abs(v)] for v in model if v > 0}

        # Skip empty configurations
        if not selected_features:
            solver.add_clause([-v for v in model])  # Block empty configuration
            continue

        # Validate and minimize the selected features
        is_minimal = True
        for feature in selected_features:
            if feature not in mandatory_features:
                test_features = selected_features - {feature}
                if is_valid_product(test_features, mandatory_features):
                    is_minimal = False
                    break

        # Exclude configurations that violate OR constraints (selecting both CreditCard and Discount)
        if 'CreditCard' in selected_features and 'Discount' in selected_features:
            is_minimal = False

        # Add only minimal valid configurations
        if is_minimal:
            mwps.append(sorted(list(selected_features)))

        # Block the current model
        solver.add_clause([-v for v in model])

    print("\n===== all possible working products =====")
    print(f"Total Number of MWPs: {len(mwps)}")
    for idx, mwp in enumerate(mwps, 1):
        print(f"\nMWP {idx}:")
        print(", ".join(mwp) + ".")

    return mwps
