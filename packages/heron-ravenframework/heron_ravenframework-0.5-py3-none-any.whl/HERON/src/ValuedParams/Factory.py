
# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED

from ravenframework.utils import InputData, InputTypes
from ravenframework.EntityFactoryBase import EntityFactory

from .SyntheticHistory import SyntheticHistory
from .StaticHistory import StaticHistory
from .ROM import ROM
from .Function import Function
from .Parametric import FixedValue, OptBounds, SweepValues
from .Variable import Variable
from .Activity import Activity
from .RandomVariable import RandomVariable

class ValuedParamFactory(EntityFactory):
  """
    Factory for ValuedParams
  """
  def __init__(self, *args):
    """
      Instantiate
      @ In, args, list, positional arguments
      @ Out, None
    """
    super().__init__(*args)
    # TODO registered_entities = [] # for filling in values

  def make_input_specs(self, name, descr=None, allowed=None, kind='singular'):
    """
      Fill input specs for the provided name and description.
      @ In, name, str, name of new spec
      @ In, descr, str, optional, description of spec
      @ In, allowed, list, optional, string list of allowable types of ValuedParam. Overrides "kind".
      @ In, kind, str, optional, kind of ValuedParam grouping (default)
      @ Out, spec, InputData, specification
    """
    add_descr = ''
    if allowed is None:
      allowed = allowable[kind]
      allowed_str = ', '.join([f'\\xmlNode{{{a}}}' for a in allowed])
      add_descr = rf"""This value can be taken from any \emph{{one}} of the sources as subnodes (described below): {allowed_str}."""

    if descr is None:
      description = add_descr
    else:
      description = descr + r"""\\ \\""" + add_descr

    spec = InputData.parameterInputFactory(name, descr=description)
    for typ, klass in self._registeredTypes.items():
      if typ in allowed:
        spec.addSub(klass.get_input_specs())
    # addons
    spec.addSub(
      InputData.parameterInputFactory(
        'multiplier',
        contentType=InputTypes.FloatType,
        descr=r"""Multiplies any value obtained by this parameter by the given value. \default{1}"""
      )
    )
    addl_spec = InputData.parameterInputFactory(
      'AdditionalInfo',
      descr=r"""Additional arbitrary input information. For custom-defined parameters, such as \xmlNode{Function},
            the additional information will be passed as part of the `texttt{meta[``HERON''][``custom_input'']}
            passed to the user-supplied custom evaluation definition.
            In the case of the \xmlNode{Function}, this is passed to the method in the Python module indicated by
            the user, and will be unique for each use of the \xmlNode{Function} in the HERON input. Note that
            the custom input nodes are not checked in any way by the input parsing."""
    )
    addl_spec.setStrictMode(False)
    spec.addSub(addl_spec)
    return spec

factory = ValuedParamFactory('ValuedParam')

# fixed in inner
factory.registerType('fixed_value', FixedValue)
factory.registerType('sweep_values', SweepValues)
factory.registerType('opt_bounds', OptBounds)
factory.registerType('variable', Variable)
# frequent revaluation
factory.registerType('CSV', StaticHistory)
factory.registerType('ARMA', SyntheticHistory)
factory.registerType('ROM', ROM)
factory.registerType('Function', Function)
factory.registerType('activity', Activity)
factory.registerType('uncertainty', RandomVariable)

# map of "kinds" of ValuedParams to the default acceptable ValuedParam types
allowable = {}
# single evaluations, like cashflow prices and component capacities
allowable['singular'] = [
  'fixed_value',
  'sweep_values',
  'opt_bounds',
  'variable',
  'ARMA',
  'Function',
  'ROM',
  'CSV',
  'uncertainty'
]
# evaluations available only after dispatch (e.g. for economics)
## for example, we can't base a capacity on the dispatch activity ... right?
allowable['post-dispatch'] = allowable['singular'] + ['activity']
allowable['all'] = list(factory.knownTypes())
