NLG's requirement for the input recipe:
1) recipe must at least specify the intent

NLG .json template rules
1) Templates are catogorized based on intent.
2) Each template can have at most one sub-template.
3) Sub-templates cannot contain sub-templates.
4) Sub-templates cannot contain descriptors.
4) Attributes are boolean values

A template can match to a recipe if and only if (this is about the realized algorithm):
1) the template has the same # of content tokens as the receipe does
2) the template has the same # of attributes and attribute values as the recipe does
3) descriptor tokens specified in a template must exist in the receipe, aka recipe's descriptor types >= template's descriptor types
