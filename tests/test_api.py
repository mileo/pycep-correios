#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pycep_correios
----------------------------------

Tests for `pycep_correios` module.
"""

import requests
from unittest import mock, TestCase
from jinja2 import Environment, PackageLoader

from pycep_correios import get_address, format_cep
from pycep_correios.exceptions import InvalidCEP
from pycep_correios.exceptions import TimeOut
from pycep_correios.exceptions import TooManyRedirects
from pycep_correios.exceptions import ConnectionError


class TestCorreios(TestCase):

    def setUp(self):

        address = {
            'bairro': 'Asa Norte',
            'cep': '70002900',
            'cidade': 'Brasília',
            'end': 'SBN Quadra 1 Bloco A',
            'id': '0',
            'uf': 'DF',
        }

        self.expected_address = {
            'bairro': address['bairro'],
            'cidade': address['cidade'],
            'complemento': '',
            'outro': '',
            'logradouro': address['end'],
            'uf': address['uf'],
        }

        self.env = Environment(loader=PackageLoader('tests', 'templates'))

        template = self.env.get_template('response.xml')
        xml = template.render(**address)
        self.response_xml = (xml.replace('\n', '')).replace('\t', '')

        template = self.env.get_template('response_error.xml')
        xml = template.render()
        self.response_xml_error = (xml.replace('\n', '')).replace('\t', '')

    @mock.patch('requests.post')
    def test_get_address(self, mock_api_call):

        # Aqui realizamos consulta com o CEP correto
        param = {
            'text': self.response_xml,
            'ok': True,
            'status_code': 200,
        }

        mock_api_call.return_value = mock.MagicMock(**param)

        self.assertDictEqual(get_address('70002900'), self.expected_address)

        # Aqui realizamos consultas que de alguma forma retornam mensagens de
        # erro
        param = {
            'text': self.response_xml_error,
            'ok': False,
        }

        mock_api_call.return_value = mock.MagicMock(**param)

        self.assertRaises(InvalidCEP, get_address, '1232710')

        mock_api_call.side_effect = requests.exceptions.Timeout()
        self.assertRaises(TimeOut, get_address, '12345-500')

        mock_api_call.side_effect = requests.exceptions.Timeout()
        self.assertRaises(TimeOut, get_address, '12345-500')

        mock_api_call.side_effect = requests.exceptions.TooManyRedirects()
        self.assertRaises(TooManyRedirects, get_address, '12345-500')

        mock_api_call.side_effect = requests.exceptions.ConnectionError()
        self.assertRaises(ConnectionError, get_address, '12345-500')

    def test_format_cep(self):
        self.assertRaises(InvalidCEP, format_cep, 37503003)

    # def test__mount_request(self):
    #     cep = '37503005'
    #     template = self.env.get_template('consultacep.xml')
    #     xml = template.render(cep=cep)
    #     xml = (xml.replace('\n', '')).replace('\t', '')
    #
    #     self.assertEqual(xml, _mount_request(cep=cep))

    # def test__parse_response(self):
    #     response = pycep_correios._parse_response(self.response_xml)
    #     self.assertDictEqual(response, self.expected_address)
    #
    # def test__parse_error(self):
    #     fault = pycep_correios._parse_error(self.response_xml_error)
    #     self.assertEqual(fault.strip(), 'BUSCA DEFINIDA COMO EXATA, '
    #                                     '0 CEP DEVE TER 8 DIGITOS')
