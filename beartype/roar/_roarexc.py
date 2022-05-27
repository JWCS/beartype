#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2022 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype exception hierarchy.**

This private submodule publishes a hierarchy of both public and private
:mod:`beartype`-specific exceptions raised at decoration, call, and usage time.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta

# See the "beartype.cave" submodule for further commentary.
__all__ = ['STAR_IMPORTS_CONSIDERED_HARMFUL']

# ....................{ SUPERCLASS                         }....................
class BeartypeException(Exception, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype exceptions.**

    Instances of subclasses of this exception are raised either:

    * At decoration time from the :func:`beartype.beartype` decorator.
    * At call time from the new callable generated by the
      :func:`beartype.beartype` decorator to wrap the original callable.
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(self, message: str) -> None:
        '''
        Initialize this exception.

        This constructor (in order):

        #. Passes all passed arguments as is to the superclass constructor.
        #. Sanitizes the fully-qualified module name of this
           exception from the private ``"beartype.roar._roarexc"`` submodule to
           the public ``"beartype.roar"`` subpackage to both improve the
           readability of exception messages and discourage end users from
           accessing this private submodule. By default, Python emits less
           readable and dangerous exception messages resembling:

               beartype.roar._roarexc.BeartypeCallHintParamViolation:
               @beartyped quote_wiggum_safer() parameter lines=[] violates type
               hint typing.Annotated[list[str], Is[lambda lst: bool(lst)]], as
               value [] violates validator Is[lambda lst: bool(lst)].
        '''

        # Defer to the superclass constructor.
        super().__init__(message)

        # Sanitize the fully-qualified module name of the class of this
        # exception. See the docstring for justification.
        self.__class__.__module__ = 'beartype.roar'
        # print(f'{self.__class__.__name__}: {message}')

# ....................{ CAVE                               }....................
class BeartypeCaveException(BeartypeException):
    '''
    Abstract base class of all **beartype cave exceptions.**

    Instances of subclasses of this exception are raised at usage time from
    various types published by the :func:`beartype.cave` submodule.
    '''

    pass

# ....................{ CAVE ~ NoneTypeOr                  }....................
class BeartypeCaveNoneTypeOrException(BeartypeCaveException):
    '''
    Abstract base class of all **beartype cave** ``None`` **tuple factory
    exceptions.**

    Instances of subclasses of this exception are raised at usage time from
    the :func:`beartype.cave.NoneTypeOr` tuple factory.
    '''

    pass


class BeartypeCaveNoneTypeOrKeyException(BeartypeCaveNoneTypeOrException):
    '''
    **Beartype cave** ``None`` **tuple factory key exception.**

    Instances of this exception are raised when indexing the :func:
    `beartype.cave.NoneTypeOr` dictionary with an invalid key, including:

    * The empty tuple.
    * Arbitrary objects that are neither:

      * **Types** (i.e., :class:`beartype.cave.ClassType` instances).
      * **Tuples of types** (i.e., tuples whose items are all
        :class:`beartype.cave.ClassType` instances).
    '''

    pass


class BeartypeCaveNoneTypeOrMutabilityException(
    BeartypeCaveNoneTypeOrException):
    '''
    **Beartype cave** ``None`` **tuple factory mutability exception.**

    Instances of this exception are raised when attempting to explicitly set a
    key on the :func:`beartype.cave.NoneTypeOr` dictionary.
    '''

    pass

# ....................{ CONF                               }....................
class BeartypeConfException(BeartypeException):
    '''
    **Beartype configuration exception.**

    Instances of this exception are raised on either erroneously instantiating
    the :class:`beartype.BeartypeConf` class *or* passing an object that is not
    an instance of that class as the ``conf`` parameter to the
    :func:`beartype.beartype` decorator.
    '''

    pass

# ....................{ DECORATOR                          }....................
class BeartypeDecorException(BeartypeException):
    '''
    Abstract base class of all **beartype decorator exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator.
    '''

    pass

# ....................{ DECORATOR ~ wrapp[ee|er]           }....................
class BeartypeDecorWrappeeException(BeartypeDecorException):
    '''
    **Beartype decorator wrappee exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator when passed a **wrappee** (i.e., object
    to be decorated by this decorator) of invalid type.
    '''

    pass


class BeartypeDecorWrapperException(BeartypeDecorException):
    '''
    **Beartype decorator parse exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on accidentally generating an **invalid
    wrapper** (i.e., syntactically invalid new callable to wrap the original
    callable).
    '''

    pass

# ....................{ DECORATOR ~ hint                   }....................
class BeartypeDecorHintException(BeartypeDecorException):
    '''
    Abstract base class of all **beartype decorator type hint exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    annotated by one or more **invalid type hints** (i.e., annotations that are
    neither PEP-compliant nor PEP-compliant type hints supported by this
    decorator).
    '''

    pass


class BeartypeDecorHintForwardRefException(BeartypeDecorHintException):
    '''
    **Beartype decorator forward reference type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by an
    **invalid forward reference type hint** (i.e., string whose value is the
    name of a user-defined class that has yet to be declared).
    '''

    pass


class BeartypeDecorHintTypeException(BeartypeDecorHintException):
    '''
    **Beartype decorator class type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by an
    **invalid class type hint** (i.e., class invalid for use as a type hint,
    typically due to failing to support runtime :func:`isinstance` calls).
    '''

    pass

# ....................{ DECORATOR ~ hint : non-pep         }....................
class BeartypeDecorHintNonpepException(BeartypeDecorHintException):
    '''
    **Beartype decorator PEP-noncompliant type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by an
    **invalid PEP-noncompliant type hint** (i.e., type hint failing to comply
    with :mod:`beartype`-specific semantics, including tuple unions and
    fully-qualified forward references).

    Tuple unions, for example, are required to contain *only* PEP-noncompliant
    annotations. This exception is thus raised for callables type-hinted with
    tuples containing one or more PEP-compliant items (e.g., instances or
    classes declared by the stdlib :mod:`typing` module) *or* arbitrary objects
    (e.g., dictionaries, lists, numbers, sets).
    '''

    pass


class BeartypeDecorHintNonpepNumpyException(BeartypeDecorHintNonpepException):
    '''
    **Beartype decorator PEP-noncompliant NumPy type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by an
    **invalid NumPy type hint** (e.g., ``numpy.typed.NDArray[...]`` type hint
    subscripted by an invalid number of arguments).
    '''

    pass

# ....................{ DECORATOR ~ hint : pep             }....................
class BeartypeDecorHintPepException(BeartypeDecorHintException):
    '''
    Abstract base class of all **beartype decorator PEP-compliant type hint
    value exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    annotated with one or more PEP-compliant type hints either violating an
    annotation-centric PEP (e.g., :pep:`484`) *or* this decorator's
    implementation of such a PEP.
    '''

    pass


class BeartypeDecorHintPepSignException(BeartypeDecorHintPepException):
    '''
    **Beartype decorator PEP-compliant type hint sign exception.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    annotated with one or more PEP-compliant type hints *not* uniquely
    identifiable by a **sign** (i.e., object uniquely identifying a category
    of PEP-compliant type hints).
    '''

    pass


class BeartypeDecorHintPepUnsupportedException(BeartypeDecorHintPepException):
    '''
    **Beartype decorator unsupported PEP-compliant type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints (e.g., instances or classes declared
    by the stdlib :mod:`typing` module) currently unsupported by this
    decorator.
    '''

    pass

# ....................{ DECORATOR ~ hint : pep : proposal  }....................
class BeartypeDecorHintPep3119Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`3119`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`3119` *or* this
    decorator's implementation of :pep:`3119`, including:

    * Hints that are **non-isinstanceable classes** (i.e., classes that
      prohibit being passed as the second parameter to the :func:`isinstance`
      builtin by leveraging metaclasses overriding the ``__instancecheck__()``
      dunder method to raise exceptions). Notably, this includes most public
      classes declared by the standard :mod:`typing` module.
    '''

    pass


class BeartypeDecorHintPep484Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`484`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`484` *or* this
    decorator's implementation of :pep:`484`, including:

    * Hints subscripted by the :attr:`typing.NoReturn` type hint (e.g.,
      ``typing.List[typing.NoReturn]``).
    '''

    pass


class BeartypeDecorHintPep484585Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`484`- or :pep:`585`-compliant **dual type hint
    exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints violating :pep:`484`, :pep:`585`, *or*
    this decorator's implementation of :pep:`484` or :pep:`585`.
    '''

    pass


class BeartypeDecorHintPep544Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`544`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`544` *or* this
    decorator's implementation of :pep:`544`.
    '''

    pass


class BeartypeDecorHintPep557Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`557`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`557` *or* this
    decorator's implementation of :pep:`557`.
    '''

    pass


class BeartypeDecorHintPep585Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`585`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`585` *or* this
    decorator's implementation of :pep:`585`.
    '''

    pass


class BeartypeDecorHintPep586Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`586`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`586` *or* this
    decorator's implementation of :pep:`586`.
    '''

    pass


class BeartypeDecorHintPep593Exception(BeartypeDecorHintPepException):
    '''
    **Beartype decorator** :pep:`593`-compliant **type hint exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated with
    one or more PEP-compliant type hints either violating :pep:`593` *or* this
    decorator's implementation of :pep:`593`.
    '''

    pass

# ....................{ DECORATOR ~ param                  }....................
class BeartypeDecorParamException(BeartypeDecorException):
    '''
    Abstract base class of all **beartype decorator parameter exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    declaring invalid parameters.
    '''

    pass


class BeartypeDecorParamNameException(BeartypeDecorParamException):
    '''
    **Beartype decorator parameter name exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable declaring
    parameters with **invalid names** (i.e., prefixed by the
    :mod:`beartype`-reserved substring ``"__bear"``).
    '''

    pass

# ....................{ DECORATOR ~ pep                    }....................
class BeartypeDecorPepException(BeartypeDecorException):
    '''
    Abstract base class of all **beartype decorator Python Enhancement Proposal
    (PEP) exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    violating a specific PEP.
    '''

    pass


class BeartypeDecorHintPep563Exception(BeartypeDecorPepException):
    '''
    **Beartype decorator** `PEP 563`_ **evaluation exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on failing to dynamically evaluate a
    postponed annotation of the decorated callable when `PEP 563`_ is active
    for that callable.

    .. _PEP 563:
       https://www.python.org/dev/peps/pep-0563
    '''

    pass

# ....................{ CALL                               }....................
class BeartypeCallException(BeartypeException):
    '''
    Abstract base class of all **beartyped callable exceptions.**

    Instances of subclasses of this exception are raised from wrapper functions
    generated by the :func:`beartype.beartype` decorator, typically when
    failing a runtime type-check at call time.
    '''

    pass


class BeartypeCallUnavailableTypeException(BeartypeCallException):
    '''
    **Beartyped callable unavailable type exceptions.**

    This exception is raised from the :class:`beartype.cave.UnavailableType`
    class when passed to either the :func:`isinstance` or :func:`issubclass`
    builtin functions, typically due to a type defined by the
    :class:`beartype.cave` submodule being conditionally unavailable under the
    active Python interpreter.
    '''

    pass

# ....................{ CALL ~ hint                        }....................
class BeartypeCallHintException(BeartypeCallException):
    '''
    Abstract base class of all **beartyped callable type-checking exceptions.**

    Instances of subclasses of this exception are raised from wrapper functions
    generated by the :func:`beartype.beartype` decorator when failing a runtime
    type-check at callable call time, typically due to either being passed a
    parameter or returning a value violating a type hint annotating that
    parameter or return value.
    '''

    pass


class BeartypeCallHintForwardRefException(BeartypeCallHintException):
    '''
    **Beartyped callable forward reference type-checking exception.**

    This exception is raised from wrapper functions generated by the
    :func:`beartype.beartype` decorator when a **forward reference type hint**
    (i.e., string whose value is the name of a user-defined class that has yet
    to be defined) erroneously references a module attribute whose value is
    *not* actually a class.
    '''

    pass

# ....................{ CALL ~ hint : violation            }....................
class BeartypeCallHintViolation(BeartypeCallHintException):
    '''
    Abstract base class of all **beartyped callable type-checking violations.**

    Instances of subclasses of this exception are raised from wrapper functions
    generated by the :func:`beartype.beartype` decorator when either passed a
    parameter or returning an object whose value is of **unexpected
    PEP-compliant type** (i.e., violating a PEP-compliant type hint annotated
    for that parameter or return value).
    '''

    pass


class BeartypeCallHintParamViolation(BeartypeCallHintViolation):
    '''
    **Beartyped callable parameter type-checking exception.**

    This exception is raised from a call to a wrapper function generated by the
    :func:`beartype.beartype` decorator type-checking a decorated callable when
    the caller passes that call a parameter violating the type hint annotating
    that parameter of that decorated callable.
    '''

    pass


class BeartypeCallHintReturnViolation(BeartypeCallHintViolation):
    '''
    **Beartyped callable return type-checking exception.**

    This exception is raised from a call to a wrapper function generated by the
    :func:`beartype.beartype` decorator type-checking a decorated callable when
    that call returns an object violating the type hint annotating the return
    of that decorated callable.
    '''

    pass

# ....................{ API ~ abby                         }....................
class BeartypeAbbyHintViolation(BeartypeCallHintViolation):
    '''
    **Beartype functional type-checking exception.**

    This exception is raised at call time by the
    :func:`beartype.abby.die_if_unbearable` function when passed an arbitrary
    object violating the passed type hint.
    '''

    pass

# ....................{ API ~ claw                         }....................
class BeartypeClawException(BeartypeException):
    '''
    Abstract base class of all **beartype import hook exceptions.**

    Instances of subclasses of this exception are raised at call time from the
    callables and classes published by the :func:`beartype.claw` subpackage.
    '''

    pass


class BeartypeClawRegistrationException(BeartypeClawException):
    '''
    **Beartype import hook registration exception.**

    This exception is raised at call time by the
    :func:`beartype.claw.beartype_submodules_on_import` function when passed
    invalid parameters.
    '''

    pass

# ....................{ API ~ vale                         }....................
class BeartypeValeException(BeartypeException):
    '''
    Abstract base class of all **beartype validator exceptions.**

    Instances of subclasses of this exception are raised at usage (e.g.,
    instantiation, callable call) time from the class hierarchy published by
    the :func:`beartype.vale` subpackage.
    '''

    pass


class BeartypeValeSubscriptionException(BeartypeValeException):
    '''
    **Beartype validator subscription exception.**

    This exception is raised at instantiation time when subscripting (indexing)
    classes published by the :func:`beartype.vale` subpackage, including
    attempts to:

    * Instantiate *any* of these classes. Like standard type hints, these
      classes are *only* intended to be subscripted (indexed).
    * Subscript *any* of these classes by anything other than a **data
      validator** (i.e., tester function satisfying the type hint
      ``collections.abc.Callable[[typing.Any,], bool]``).
    * Apply the ``&`` or ``|`` operators to *any* subscriptions of these
      classes and *any* other objects (e.g.,
      ``beartype.vale.Is[lambda obj: True]] & 'If it seems bad, it is.'``).
    '''

    pass

# ....................{ PRIVATE ~ decorator                }....................
class _BeartypeDecorBeartypistryException(BeartypeDecorException):
    '''
    **Beartype decorator beartypistry exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator when erroneously accessing the
    **beartypistry** (i.e.,
    :class:`beartype._decor._cache.cachetype.bear_typistry` singleton).

    This private exception denotes a critical internal issue and should thus
    *never* be raised -- let alone exposed to end users.
    '''

    pass

# ....................{ PRIVATE ~ util                     }....................
class _BeartypeUtilException(BeartypeException):
    '''
    Abstract base class of all **beartype private utility exceptions.**

    Instances of subclasses of this exception are raised by *most* (but *not*
    all) private submodules of the private :mod:`beartype._util` subpackage.
    These exceptions denote critical internal issues and should thus *never* be
    raised, let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilCallableException(_BeartypeUtilException):
    '''
    **Beartype callable utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.utilfunc` subpackage.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilMappingException(_BeartypeUtilException):
    '''
    **Beartype mapping utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.kind.utilkinddict` submodule.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilModuleException(_BeartypeUtilException):
    '''
    **Beartype module utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.mod.utilmodule` subpackage when dynamically importing
    an unimportable external user-defined module, typically due to a
    **PEP-compliant forward reference type hint** (i.e., string whose value is
    the name of a user-defined class that has yet to be defined) erroneously
    referencing a non-existent module or module attribute.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilPathException(_BeartypeUtilException):
    '''
    **Beartype path utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.path` subpackage on various fatal edge cases.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilPythonException(_BeartypeUtilException):
    '''
    **Beartype Python utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.py` subpackage on various fatal edge cases.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilTextException(_BeartypeUtilException):
    '''
    **Beartype text utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.text` subpackage on various fatal edge cases.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilTypeException(_BeartypeUtilException):
    '''
    **Beartype class utility exception.**

    This exception is raised by public functions of the private
    :mod:`beartype._util.cls.utilclstest` subpackage.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : call                }..................
class _BeartypeCallHintRaiseException(_BeartypeUtilException):
    '''
    Abstract base class of all **beartype human-readable exception raiser
    exceptions.**

    Instances of subclasses of this exception are raised by private utility
    **exception raiser functions** (i.e., functions raising human-readable
    exceptions from wrapper functions when either passed a parameter or
    returning a value annotated by a type hint fails the runtime type-check
    required by that hint) when an unexpected failure occurs.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : call : pep          }..................
class _BeartypeCallHintPepRaiseException(_BeartypeCallHintRaiseException):
    '''
    **Beartype PEP-compliant human-readable exception raiser exception.**

    This exception is raised by the
    :func:`beartype._decor._error.errormain.raise_pep_call_exception`
    exception raiser function when an unexpected failure occurs.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeCallHintPepRaiseDesynchronizationException(
    _BeartypeCallHintPepRaiseException):
    '''
    **Beartype human-readable exception raiser desynchronization exception.**

    This exception is raised by the
    :func:`beartype._decor._error.errormain.raise_pep_call_exception` function
    (which raises human-readable exceptions from wrapper functions when either
    passed a parameter or returning a value, referred to as the "pith" for
    brevity, annotated by a PEP-compliant type hint fails the type-check
    required by that hint) when this pith appears to satisfy this type-check, a
    runtime paradox implying either:

    * The parent wrapper function generated by the :mod:`beartype.beartype`
      decorator type-checking this pith triggered a false negative by
      erroneously misdetecting this pith as failing this type check.
    * The
        :func:`beartype._decor._error.errormain.raise_pep_call_exception`
      function re-type-checking this pith triggered a false positive by
      erroneously misdetecting this pith as satisfying this type check when in
      fact this pith fails to do so.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : cache               }..................
class _BeartypeUtilCachedException(_BeartypeUtilException):
    '''
    Abstract base class of all **beartype caching utility exceptions.**

    Instances of subclasses of this exception are raised by private submodules
    of the private :mod:`beartype._util.cache` subpackage. These exceptions
    denote critical internal issues and should thus *never* be raised -- let
    alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilCallableCachedException(_BeartypeUtilCachedException):
    '''
    **Beartype memoization exception.**

    This exception is raised by the
    :func:`beartype._util.cache.utilcache.utilcachecall.callable_cached`
    decorator on various fatal errors (e.g., when the signature of the
    decorated callable is unsupported).

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilCacheLruException(_BeartypeUtilCachedException):
    '''
    **Beartype Least Recently Used (LRU) cache exception.**

    This exception is raised by the
    :func:`beartype._util.cache.utilcache.utilcachelru.CacheLruStrong` class
    on various fatal errors (e.g., when the cache capacity is *not* a positive
    integer).

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : cache : pool        }..................
class _BeartypeUtilCachedKeyPoolException(_BeartypeUtilException):
    '''
    **Beartype key pool exception.**

    This exception is raised by private functions of the private
    :mod:`beartype._util.cache.pool.utilcachepool` subpackage on various fatal
    edge cases.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''
    pass


class _BeartypeUtilCachedFixedListException(_BeartypeUtilCachedException):
    '''
    **Beartype decorator fixed list exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator when an internal callable erroneously
    mutates a **fixed list** (i.e., list constrained to a fixed length defined
    at instantiation time), usually by attempting to modify the length of that
    list.

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilCachedObjectTypedException(_BeartypeUtilCachedException):
    '''
    **Beartype decorator typed object exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator when an internal callable erroneously
    acquires a **pooled typed object** (i.e., object internally cached to a
    pool of all objects of that type).

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : object              }..................
class _BeartypeUtilObjectException(_BeartypeUtilException):
    '''
    Abstract base class of all **beartype object utility exceptions.**

    Instances of subclasses of this exception are raised by private submodules
    of the private :mod:`beartype._util.utilobject` submodule. These exceptions
    denote critical internal issues and should thus *never* be raised -- let
    alone allowed to percolate up the call stack to end users.
    '''

    pass


class _BeartypeUtilObjectNameException(_BeartypeUtilObjectException):
    '''
    **Beartype object name exception.**

    This exception is raised by the
    :func:`beartype._util.utilobject.get_object_basename_scoped` getter when
    the passed object is **unnamed** (i.e., fails to declare either the
    ``__name__`` or ``__qualname__`` dunder attributes).

    This exception denotes a critical internal issue and should thus *never* be
    raised -- let alone allowed to percolate up the call stack to end users.
    '''

    pass
