from feature_model_parser import validate_xml, parse_feature_model
from solver import compute_mwps
from visualization import create_checkbox_tree

def main():
    xml_file = 'feature-model.xml'
    xsd_file = 'feature_model.xsd'

    # Step 1: Validate and Parse XML
    print("Validating and parsing the feature model...")
    xml_tree = validate_xml(xml_file, xsd_file)
    feature_model = parse_feature_model(xml_tree)
    print("Feature model parsed successfully.\n")

    # Step 2: Compute MWPs
    print("Computing Minimum Working Products (MWPs)...")
    mwps = compute_mwps(feature_model)

    # Step 3: Visualize Feature Model (Optional)
    print("\nVisualizing the feature model...")
    create_checkbox_tree(feature_model)
    
    # Final Output
    print("\n===== Final MWPs =====")
    for idx, mwp in enumerate(mwps, start=1):
        print(f"MWP {idx}: {', '.join(mwp)}")
    
    print("\nProgram Execution Complete!")

if __name__ == "__main__":
    main()
