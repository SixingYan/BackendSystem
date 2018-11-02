#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import yaml
import jinja2
from enum import Enum


class SwaggerTypes(object):
    String = 'string'
    Integer = 'integer'
    Boolean = 'boolean'
    Date = 'date'
    Datetime = 'date-time'
    Array = 'array'
    Object = 'object'
    Number = 'number'
    Ref = '$ref'


class Field(object):
    def __init__(self, name, type_, format_, required, description=None, example=None,
                 default=None, min_length=None, max_length=None, marshmallow_statement=None):
        self.name = name
        self.type = type_
        self.format = format_
        self.required = required
        self.description = description
        self.example = example
        self.default = default
        self.min = max_length
        self.max = max_length
        self.marshmallow_statement = marshmallow_statement

    @property
    def comment(self):
        description = self.description
        example = self.example
        cmt = ''
        if description or example:
            cmt = '  # '
            if description:
                cmt += description
            if example:
                if cmt != '  # ':
                    cmt += ' '
                cmt += 'example: ' + str(example)
        return cmt


class MySchema(object):

    class Type(Enum):
        Top = 'Top'
        Internal = 'Internal'
        Parameter = 'Parameter'

    def __init__(self, type_, name, **kwargs):
        self.type = type_
        self.path = kwargs.get('path')
        self.method = kwargs.get('method')
        self.name = name
        if not name:
            self.name = MySchema._create_name(type_, self.path, self.method)
        self.schema_class_name = MySchema._format_class_name(type_, self.name, self.path, self.method)
        self.object_class_name = MySchema._format_object_name(type_, self.name, self.path, self.method)
        self.fields = []
        self.ref_to = {}

    def __lt__(self, other):
        if self.name.endswith('_') and not other.name.endswith('_'):
            return True
        return self.name < other.name

    @staticmethod
    def _create_name(type_, path, method):
        if type_ == MySchema.Type.Parameter:
            p = path[1:].replace('/', '_').replace('{', '').replace('}', '')
            return 'Param{}'.format(
                ''.join(t[0].upper() + t[1:] for t in p.split('_')),
                method.upper()
            )
        return 'Unnamed'

    @staticmethod
    def _format_class_name(type_, name, path, method):
        if type_ in [MySchema.Type.Top, MySchema.Type.Internal]:
            return '{}Schema'.format(name)
        elif type_ == MySchema.Type.Parameter:
            return '{}Schema'.format(name)

    @staticmethod
    def _format_object_name(type_, name, path, method):
        return name


def fields_as_param_statement(fields):
    required_fileds = [f for f in fields if f.required]
    unrequired_fileds = [f for f in fields if not f.required]
    fields_as_param = [f.name for f in required_fileds]
    [fields_as_param.append('{}=None'.format(f.name)) for f in unrequired_fileds]
    return ', '.join(fields_as_param)


def create_name_for_internal_shcema(parent_schema_name, property_name):
    return '{}_{}'.format(
        parent_schema_name,
        ''.join(t[0].upper() + t[1:] for t in property_name.split('_'))
    )


TYPE_TO_FIELD = {
    SwaggerTypes.String: 'String',
    SwaggerTypes.Integer: 'Integer',
    SwaggerTypes.Boolean: 'Boolean',
    SwaggerTypes.Date: 'Date',
    SwaggerTypes.Datetime: 'Datetime',
    SwaggerTypes.Array: 'List',
    SwaggerTypes.Ref: 'Nested',
    SwaggerTypes.Number: 'Decimal',
}

FORMAT_TO_FIELD = {
    'email': 'Email',
    'url': 'URL',
    'decimal': 'Decimal',
}

VALIDATOR_PACKAGE = 'base'
VALIDATOR_FILE = 'validator'

FORMAT_TO_VALIDATOR = {
    'mobile': '{}.v_mobile'.format(VALIDATOR_FILE),
    'id_card': '{}.v_id_number'.format(VALIDATOR_FILE),
    'bank_card': '{}.v_bank_card_number'.format(VALIDATOR_FILE),
    'enc_user_id': '{}.v_enc_user_id'.format(VALIDATOR_FILE),
    'enc_message_id': '{}.v_enc_message_id'.format(VALIDATOR_FILE),
    'uuid': '{}.v_enc_id'.format(VALIDATOR_FILE),
}

g_internal_unnamed_schemas_definitions = {}
g_ref_from = {}


def property_element_to_field(definition, required):
    field = TYPE_TO_FIELD[definition['type']]
    format_ = definition.get('format')
    if format_ and format_.startswith('decimal'):
        format_ = 'decimal'
    if format_ in FORMAT_TO_FIELD:
        field = FORMAT_TO_FIELD[format_]

    validator = FORMAT_TO_VALIDATOR.get(format_)

    min_ = 'minLength' in definition
    max_ = 'maxLength' in definition
    if min_ or max_:
        if min_ and max_:
            validator = "marshmallow.validate.Length(min={}, max={})".format(definition['minLength'], definition['maxLength'])
        elif min_:
            validator = "marshmallow.validate.Length(min={})".format(definition['minLength'])
        else:
            validator = "marshmallow.validate.Length(max={})".format(definition['maxLength'])

    default = definition.get('default')

    conditions = []
    if required:
        conditions.append('required=True')
    if validator:
        conditions.append('validate={}'.format(validator))
    if default:
        if definition['type'] == SwaggerTypes.String:
            c = 'missing=\'{}\''.format(default)
        else:
            c = 'missing={}'.format(default)
        conditions.append(c)
    if format_ == 'url':
        conditions.append('relative=True')
    conditions_s = ', '.join(conditions)

    tempalte = jinja2.Template('marshmallow.fields.{{field}}({{conditions}})')
    return tempalte.render(field=field, conditions=conditions_s)


def property_ref_to_field(ref_schema_name, required):
    template = jinja2.Template('marshmallow.fields.Nested({{ref_schema}}Schema(){{", required=True" if required else ""}})')
    return template.render(ref_schema=ref_schema_name, required=required)


def property_array_to_field(schema, property_name, item_difinition, required):
    template = jinja2.Template('marshmallow.fields.List({{item}}{{", required=True" if required else ""}})')
    item = property_to_field(schema, property_name, item_difinition, required=False)
    return template.render(item=item, required=required)


def property_to_field(schema, property_name, property_definition, required):
    if '$ref' in property_definition:
        ref_schema_name = property_definition['$ref'].split('/')[-1]
        def_code = property_ref_to_field(ref_schema_name, required)
        schema.ref_to[ref_schema_name] = True
        g_ref_from.setdefault(ref_schema_name, {})[schema.name] = schema
    else:
        if 'type' not in property_definition:
            raise KeyError('{} definition missing "type"'.format(schema.name))

        if property_definition['type'] == SwaggerTypes.Object:
            # Nested unnamed schema: create a definition and make a $ref
            internal_schema_name = create_name_for_internal_shcema(schema.name, property_name)
            def_code = property_ref_to_field(internal_schema_name, required)
            schema.ref_to[internal_schema_name] = True
            g_ref_from.setdefault(internal_schema_name, {})[schema.name] = schema
            # del property_definition['type']
            g_internal_unnamed_schemas_definitions[internal_schema_name] = property_definition
        elif property_definition['type'] == SwaggerTypes.Array:
            def_code = property_array_to_field(schema, property_name, property_definition['items'], required)
        else:
            def_code = property_element_to_field(property_definition, required)

    return def_code


def build_schema(schema_name, schema_definition, internal=False):
    if internal:
        schema = MySchema(MySchema.Type.Internal, schema_name)
    else:
        schema = MySchema(MySchema.Type.Top, schema_name)

    try:
        property_definitions = schema_definition['properties']
    except KeyError as err:
        print('no properties in schema: {}'.format(schema_name))
        raise

    fields = []
    for prop_name, prop_def in property_definitions.items():
        required = True if prop_name in schema_definition.get('required', []) else False

        field_define = property_to_field(schema, prop_name, prop_def, required)

        description = prop_def.get('description')
        example = prop_def.get('example')
        if description or example:
            comment = '  # '
            if description:
                comment += description
            if example:
                if comment != '  # ':
                    comment += ' '
                comment += 'example: ' + str(example)
            field_define += comment

        field = Field(
            name=prop_name,
            type_=prop_def.get('type'),
            format_=prop_def.get('format'),
            required=required,
            description=description,
            example=example,
            default=prop_def.get('default'),
            min_length=prop_def.get('minLength'),
            max_length=prop_def.get('maxLength'),
            marshmallow_statement=field_define
        )
        fields.append(field)

    schema.fields = fields
    schema.fields_as_param_statement = fields_as_param_statement(schema.fields)

    return schema


def resolve_ref(schemas):
    refless_schemas = []
    for _, schema in schemas.items():
        if not schema.ref_to:
            refless_schemas.append(schema)
    for refless_schema in refless_schemas:
        del schemas[refless_schema.name]
        ref_src_schemas = g_ref_from.get(refless_schema.name, {})
        for _, src_schema in ref_src_schemas.items():
            del src_schema.ref_to[refless_schema.name]
    return refless_schemas


def build_field(schema, properties):
    field_define = property_to_field(schema, properties['name'], properties, properties.get('required', False))
    description = properties.get('description')
    example = properties.get('example')
    if description or example:
        comment = '  # '
        if description:
            comment += description
        if example:
            comment += 'example: ' + str(example)
        field_define += comment
    field = Field(
        name=properties['name'],
        type_=properties['type'],
        format_=properties.get('format'),
        required=properties.get('required', False),
        description=description,
        example=example,
        default=properties.get('default'),
        min_length=properties.get('minLength'),
        max_length=properties.get('maxLength'),
        marshmallow_statement=field_define
    )
    return field


def build_parameter_schema(path, method, parameters, global_parameters):
    schema = MySchema(MySchema.Type.Parameter, '', path=path, method=method)
    fields = []
    for param in parameters:
        if '$ref' in param:
            param['name'] = param['$ref'].split('/')[-1]
            field = build_field(schema, global_parameters[param['name']])
        else:
            if param.get('in') != 'query':
                continue
            if 'name' not in param:
                raise Exception('Parameter without name: {}'.format(path))
            field = build_field(schema, param)
        fields.append(field)
    if not fields:
        return None
    schema.fields = fields
    schema.fields_as_param_statement = fields_as_param_statement(schema.fields)
    return schema


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input_file')
    parser.add_argument('-v', '--version', help='swagger OpenAPI version: 2 or 3', type=int, default=2)
    parser.add_argument('-o', '--out', help='output marshmallow schema definition file', type=str, default='api/schema.py')
    args = parser.parse_args()

    openapi_version = args.version
    output_file = args.out
    swagger_yaml_file = args.input_file

    openapi_version = 2
    if openapi_version == 3:
        schema_path = 'components/schemas'.split('/')
    elif openapi_version == 2:
        schema_path = ['definitions']
    else:
        parser.print_help()
        sys.exit(1)

    swagger_yaml = yaml.load(open(swagger_yaml_file, encoding='utf-8'))
    swagger_model_definitions = swagger_yaml
    try:
        for p in schema_path:
            swagger_model_definitions = swagger_model_definitions[p]
    except KeyError:
        raise KeyError('no schema definitions found at {}:{}'.format(swagger_yaml_file, '/'.join(schema_path)))

    # Build schema from query parameters.
    global_parameters = swagger_yaml.get('parameters', {})
    paramter_schemas = []
    swagger_paths = swagger_yaml.get('paths')
    if swagger_paths:
        for path, path_def in swagger_paths.items():
            method = 'get'
            get = path_def.get(method)
            if not get:
                continue
            get_parameters = get.get('parameters')
            if not get_parameters:
                continue
            schema = build_parameter_schema(path, method, get_parameters, global_parameters)
            if not schema:
                print('ignore path without query parameters: {} {}'.format(method, path))
                continue
            paramter_schemas.append(schema)

    # Build schema from swagger model definition.
    all_schemas = {
        name: build_schema(name, definition)
        for name, definition in swagger_model_definitions.items()
    }
    internal_unnamed_schemas = {
        name: build_schema(name, definition, True)
        for name, definition in g_internal_unnamed_schemas_definitions.items()
    }

    all_schemas.update(internal_unnamed_schemas)

    result_shcemas = []
    while all_schemas:
        refless_schemas = resolve_ref(all_schemas)
        refless_schemas.sort()
        result_shcemas += refless_schemas
        if all_schemas and not refless_schemas:
            for name, schema in all_schemas.items():
                print('ref deadline: {}'.format(name))
            break

    TEMPLATE_S = '''# -*- coding: utf-8 -*-

\'\'\' Generated codes

Marshmallow schema classes accord with model definitions in Swagger.
BE VERY CAREFUL to change this file manually.

\'\'\'

import marshmallow
from {{validator_package}} import {{validator_file}}


{% if parameter_schemas %}
\'\'\' SCHEMAS FROM QUERY PARAMETERS.
\'\'\'


{%for schema in parameter_schemas %}
class {{schema.object_class_name}}(object):
    __slots__ = [{% for field in schema.fields %}{%if loop.last%}'{{field.name}}'{%else%}'{{field.name}}', {%endif%}{% endfor %}, '_original_data']

    def __init__(self, {{schema.fields_as_param_statement}}, original_data=None):
{% for field in schema.fields %}
        self.{{field.name}} = {{field.name}}
{% endfor %}
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class {{schema.schema_class_name}}(marshmallow.Schema):
{% for field in schema.fields %}
    {{field.name}} = {{field.marshmallow_statement}}
{% endfor %}

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = {{schema.object_class_name}}(**data)
        return obj


{% endfor %}
{% endif %}
\'\'\' SCHEMAS FROM MODEL DEFINITIONS.
\'\'\'


{%for schema in model_schemas %}
class {{schema.object_class_name}}(object):
    __slots__ = [{% for field in schema.fields %}{%if loop.last%}'{{field.name}}'{%else%}'{{field.name}}', {%endif%}{% endfor %}, '_original_data']

    def __init__(self, {{schema.fields_as_param_statement}}, original_data=None):
{% for field in schema.fields %}
        self.{{field.name}} = {{field.name}}
{% endfor %}
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class {{schema.schema_class_name}}(marshmallow.Schema):
{% for field in schema.fields %}
    {{field.name}} = {{field.marshmallow_statement}}
{% endfor %}

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = {{schema.object_class_name}}(**data)
        return obj


{% endfor -%}'''

    template = jinja2.Template(TEMPLATE_S, trim_blocks=True)
    schema_code = template.render(
        validator_package=VALIDATOR_PACKAGE,
        validator_file=VALIDATOR_FILE,
        parameter_schemas=paramter_schemas,
        model_schemas=result_shcemas
    )

    i = -1
    while i > -len(schema_code) - 1:
        if schema_code[i] == '\n':
            i -= 1
        else:
            break
    if i == -1:
        schema_code = schema_code + '\n'
    schema_code = schema_code[0:i + 2]

    if output_file:
        with open(output_file, "w", encoding="utf-8") as schema_py_file:
            schema_py_file.write(schema_code)
    else:
        print(schema_code, end='')


if __name__ == '__main__':
    main()
