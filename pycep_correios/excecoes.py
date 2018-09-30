# -*- coding: utf-8 -*-


class ExcecaoPyCEPCorreios(Exception):
    """ Excecao base da lib"""

    def __init__(self, message=''):
        super(ExcecaoPyCEPCorreios, self).__init__(message)
        self.message = message

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.message)


class CEPInvalido(ExcecaoPyCEPCorreios):
    """ Excecao disparada quando o CEP possui tamanho incorreto
    (diferente de 8) e/ou não existe"""


class FalhaNaConexao(ExcecaoPyCEPCorreios):
    """ Erro de conexao durante a requisicao """


class MultiploRedirecionamento(ExcecaoPyCEPCorreios):
    """ Excecao de multiplo redirecionamento """


class Timeout(ExcecaoPyCEPCorreios):
    """ Erro de TimeOut  """
