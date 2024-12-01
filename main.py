from feature_model_parser import validate_xml, parse_feature_model
from translator import translate_to_propositional_logic
from solver import compute_mwps
from visualization import create_checkbox_tree

def main():
    xml_file = 'feature-model.xml'
    xsd_file = 'feature_model.xsd'

    # Step 1: Validate and Parse XML
    xml_tree = validate_xml(xml_file, xsd_file)
    feature_model = parse_feature_model(xml_tree)

    # Step 2: Translate to Propositional Logic
    logic_expressions = translate_to_propositional_logic(feature_model)

    # Step 3: Compute MWPs
    #mwps = compute_mwps(logic_expressions)

    # Step 4: Visualize Feature Model
    #create_checkbox_tree(feature_model)

    # Final Output
    print("\nProgram Execution Complete!")
    #print(f"Final MWPs: {mwps}")

if __name__ == "__main__":
    main()
