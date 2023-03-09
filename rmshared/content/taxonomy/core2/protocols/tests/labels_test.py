from mock.mock import Mock
from mock.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core2 import labels
from rmshared.content.taxonomy.core2 import protocols
from rmshared.content.taxonomy.protocols import IFields
from rmshared.content.taxonomy.protocols import IValues


class TestLabels:
    @fixture
    def fields_(self) -> IFields | Mock:
        return Mock(spec=IFields)

    @fixture
    def values_(self) -> IValues | Mock:
        return Mock(spec=IValues)

    def test_value(self, fields_: IFields, values_: IValues):
        fields_.make_field = Mock(side_effect=['field_1'])
        values_.make_value = Mock(side_effect=['value_1'])
        fields_.jsonify_field = Mock(side_effect=[{'field_1': {}}])
        values_.jsonify_value = Mock(side_effect=[{'value_1': {}}])

        protocol = protocols.labels.Value(fields_, values_)

        assert protocol.get_name() == 'value'
        assert protocol.make_label({'field': {'field_1': {}}, 'value': {'value_1': {}}}) == labels.Value(field='field_1', value='value_1')
        assert protocol.jsonify_label_info(labels.Value(field='field_1', value='value_1')) == {'field': {'field_1': {}}, 'value': {'value_1': {}}}
        assert values_.make_value.call_args_list == [call({'value_1': {}})]
        assert fields_.make_field.call_args_list == [call({'field_1': {}})]
        assert values_.jsonify_value.call_args_list == [call('value_1')]
        assert fields_.jsonify_field.call_args_list == [call('field_1')]

    def test_badge(self, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_2'])
        fields_.jsonify_field = Mock(side_effect=[{'field_2': {}}])

        protocol = protocols.labels.Badge(fields_)

        assert protocol.get_name() == 'badge'
        assert protocol.make_label({'field': {'field_2': {}}}) == labels.Badge(field='field_2')
        assert protocol.jsonify_label_info(labels.Badge(field='field_2')) == {'field': {'field_2': {}}}
        assert fields_.make_field.call_args_list == [call({'field_2': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_2')]

    def test_empty(self, fields_: IFields):
        fields_.make_field = Mock(side_effect=['field_3'])
        fields_.jsonify_field = Mock(side_effect=[{'field_3': {}}])

        protocol = protocols.labels.Empty(fields_)

        assert protocol.get_name() == 'empty'
        assert protocol.make_label({'field': {'field_3': {}}}) == labels.Empty(field='field_3')
        assert protocol.jsonify_label_info(labels.Empty(field='field_3')) == {'field': {'field_3': {}}}
        assert fields_.make_field.call_args_list == [call({'field_3': {}})]
        assert fields_.jsonify_field.call_args_list == [call('field_3')]
