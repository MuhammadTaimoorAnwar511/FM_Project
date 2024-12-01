from lxml import etree


def validate_xml(xml_file, xsd_file):
    try:
        xml_doc = etree.parse(xml_file)
        xsd_doc = etree.parse(xsd_file)
        xmlschema = etree.XMLSchema(xsd_doc)
        xmlschema.assertValid(xml_doc)
        print(f"\nValidation successful: '{xml_file}' is valid against '{xsd_file}'.")
        return xml_doc
    except etree.XMLSchemaError as e:
        print(f"\nValidation error: {e}")
        raise


def parse_feature_model(xml_tree):
    root = xml_tree.getroot()
    feature_model = {}

    def parse_feature(element):
        feature = {
            'name': element.get('name'),
            'mandatory': element.get('mandatory') == 'true',
            'children': [],
            'groups': []
        }

        for child in element:
            if child.tag == 'feature':
                feature['children'].append(parse_feature(child))
            elif child.tag == 'group':
                group = {
                    'type': child.get('type'),
                    'features': [parse_feature(f) for f in child.findall('feature')]
                }
                feature['groups'].append(group)
        return feature

    feature_model['root'] = parse_feature(root.find('feature'))

    constraints_element = root.find('constraints')
    constraints = []
    if constraints_element is not None:
        for constraint in constraints_element.findall('constraint'):
            constraints.append({
                'englishStatement': constraint.findtext('englishStatement'),
                'booleanExpression': constraint.findtext('booleanExpression')
            })
    feature_model['constraints'] = constraints

    # Print the parsed feature model for verification
    print("\nParsed Feature Model:")
    print(feature_model)

    return feature_model
