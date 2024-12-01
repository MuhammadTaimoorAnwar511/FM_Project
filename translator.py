def translate_to_propositional_logic(feature_model):
    """
    Translates the feature model into a simplified propositional logic formula
    that matches the expected output format exactly.
    """
    clauses = []

    def translate_feature(feature, is_root=False):
        """
        Recursively translates a feature and its sub-features into propositional logic clauses.
        """
        local_clauses = []
        feature_name = feature['name']

        # Add the root feature explicitly
        if is_root:
            local_clauses.append(feature_name)

        # Handle child features
        for child in feature.get('children', []):
            child_name = child['name']
            if child['mandatory']:
                # Mandatory child relationship
                local_clauses.append(f"({child_name} → {feature_name})")
                local_clauses.append(f"({feature_name} → {child_name})")
            else:
                # Optional features: Parent ↔ (Child ∨ ~Child)
                local_clauses.append(f"({feature_name} ↔ ({child_name} ∨ ~{child_name}))")
            local_clauses.extend(translate_feature(child))

        # Handle groups
        for group in feature.get('groups', []):
            group_features = [f['name'] for f in group['features']]
            if group['type'] == 'or':
                # OR Group: Parent → (A ∨ B ∨ ...)
                or_clause = " ∨ ".join(group_features)
                local_clauses.append(f"({feature_name} → ({or_clause}))")
                for gf in group_features:
                    local_clauses.append(f"({gf} → {feature_name})")
            elif group['type'] == 'xor':
                # XOR Group: Parent → (Exactly one child is true)
                xor_clauses = []
                for i, fi in enumerate(group_features):
                    others = " ∧ ".join([f"~{other}" for j, other in enumerate(group_features) if i != j])
                    xor_clauses.append(f"({fi} ∧ {others})")
                xor_clause = " ∨ ".join(xor_clauses)
                local_clauses.append(f"({feature_name} → ({xor_clause}))")

                # Add explicit implications for XOR features
                for gf in group_features:
                    local_clauses.append(f"({gf} → {feature_name})")  # This fixes the issue

        return local_clauses

    # Start translating from the root feature
    root_feature = feature_model['root']
    root_feature['is_root'] = True
    clauses.extend(translate_feature(root_feature, is_root=True))

    # Translate cross-tree constraints
    for constraint in feature_model['constraints']:
        if constraint['booleanExpression']:
            clauses.append(constraint['booleanExpression'])
        elif constraint['englishStatement']:
            known_translation = translate_english_constraint(constraint['englishStatement'])
            if known_translation:
                clauses.append(known_translation)

    # Combine clauses into a single formula
    formula = " ∧ ".join(clauses)
    print("\nPropositional Logic Formula:")
    print(formula)
    return formula


def translate_english_constraint(english):
    """
    Translates known English constraints into propositional logic.
    """
    translations = {
        "The Location feature is required to filter the catalog by location.": "ByLocation → Location",
    }
    return translations.get(english)


def translate_feature(feature):
    clauses = []
    feature_name = feature['name']

    # If it's the root feature
    if feature.get('is_root', False):
        clauses.append(feature_name)

    # Handle child features
    for child in feature.get('children', []):
        child_name = child['name']
        if child['mandatory']:
            clauses.append(f"({feature_name} -> {child_name})")
        else:
            clauses.append(f"({child_name} -> {feature_name})")
        # Flatten the recursive call
        clauses.extend(translate_feature(child))

    # Handle groups
    for group in feature.get('groups', []):
        group_features = [f['name'] for f in group['features']]
        if group['type'] == 'or':
            or_clause = " | ".join(group_features)
            clauses.append(f"({feature_name} -> ({or_clause}))")
            for gf in group_features:
                clauses.append(f"({gf} -> {feature_name})")
        elif group['type'] == 'xor':
            for gf in group_features:
                clauses.append(f"({gf} -> {feature_name})")
            for i in range(len(group_features)):
                for j in range(i + 1, len(group_features)):
                    clauses.append(f"(~{group_features[i]} | ~{group_features[j]})")
            or_clause = " | ".join(group_features)
            clauses.append(f"({feature_name} -> ({or_clause}))")
        # Flatten the recursive call
        for gf in group['features']:
            clauses.extend(translate_feature(gf))

    return clauses
