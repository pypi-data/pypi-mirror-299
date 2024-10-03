<h1 align="center">unpy</h1>

<p align="center">
    <i>Unified Python</i>
</p>

<p align="center">Transpiles <code>.pyi</code> stubs from Python 3.13 to 3.10</p>

<p align="center">
    <a href="https://pypi.org/project/unpy/">
        <img
            alt="unpy - PyPI"
            src="https://img.shields.io/pypi/v/unpy?style=flat&color=olive"
        />
    </a>
    <a href="https://github.com/jorenham/unpy">
        <img
            alt="unpy - Python Versions"
            src="https://img.shields.io/pypi/pyversions/unpy?style=flat"
        />
    </a>
    <a href="https://github.com/jorenham/unpy">
        <img
            alt="unpy - license"
            src="https://img.shields.io/github/license/jorenham/unpy?style=flat"
        />
    </a>
</p>
<p align="center">
    <a href="https://github.com/jorenham/unpy/actions?query=workflow%3ACI">
        <img
            alt="unpy - CI"
            src="https://github.com/jorenham/unpy/workflows/CI/badge.svg"
        />
    </a>
    <!-- TODO -->
    <a href="https://github.com/pre-commit/pre-commit">
        <img
            alt="unpy - pre-commit"
            src="https://img.shields.io/badge/pre--commit-enabled-teal?logo=pre-commit"
        />
    </a>
    <a href="https://github.com/KotlinIsland/basedmypy">
        <img
            alt="unpy - basedmypy"
            src="https://img.shields.io/badge/basedmypy-checked-fd9002"
        />
    </a>
    <a href="https://detachhead.github.io/basedpyright">
        <img
            alt="unpy - basedpyright"
            src="https://img.shields.io/badge/basedpyright-checked-42b983"
        />
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img
            alt="unpy - ruff"
            src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"
        />
    </a>
</p>

---

> [!IMPORTANT]
> This project is in the alpha stage:
> You probably shouldn't use it in production.

## Installation

```console
$ pip install unpy
```

## Usage

```console
$ unpy --help
Usage: unpy [OPTIONS] SOURCE [OUTPUT]

Arguments:
  SOURCE    Path to the input .pyi file or '-' to read from stdin.  [required]
  [OUTPUT]  Path to the output .pyi file. Defaults to stdout.

Options:
  --version                       Show the version and exit
  --diff                          Show the changes between the input and
                                  output in unified diff format
  --target [3.10|3.11|3.12|3.13]  The minimum Python version that should be
                                  supported.  [default: 3.10]
  --help                          Show this message and exit.
```

## Examples

Some simple examples of Python 3.13 stubs that are backported to Python 3.10.

### Imports

```console
$ unpy --target 3.10 --diff examples/imports.pyi
```

```diff
+++ -
@@ -1,6 +1,4 @@
- from types import CapsuleType
- from typing import override
- from warnings import deprecated
+ from typing_extensions import CapsuleType, deprecated, override

  @deprecated("RTFM")
  class Spam:
      __pyx_capi__: dict[str, CapsuleType]
      @override
      def __hash__(self, /) -> int: ...
```

Note the alphabetical order of the generated imports.

### Type Aliases

```console
$ unpy --target 3.10 --diff examples/type_aliases.pyi
```

```diff
+++ -
@@ -1,7 +1,15 @@
  from collections.abc import Callable
+ from typing import ParamSpec, TypeAlias, TypeVar
+ from typing_extensions import TypeAliasType, TypeVarTuple, Unpack

- type Binary = bytes | bytearray | memoryview
- type Vector[R: float] = tuple[R, ...]
- type tciD[V, K] = dict[K, V]
- type Things[*Ts] = tuple[*Ts]
- type Callback[**Tss] = Callable[Tss, None]
+ _R = TypeVar("_R", bound=float)
+ _V = TypeVar("_V")
+ _K = TypeVar("_K")
+ _Ts = TypeVarTuple("_Ts")
+ _Tss = ParamSpec("_Tss")
+
+ Binary: TypeAlias = bytes | bytearray | memoryview
+ Vector: TypeAlias = tuple[_R, ...]
+ tciD = TypeAliasType("tciD", dict[_K, _V], type_params=(_V, _K))
+ Things: TypeAlias = tuple[Unpack[_Ts]]
+ Callback: TypeAlias = Callable[_Tss, None]
```

Note that `TypeAlias` cannot be used with `tciD` because the definition order of the
type parameters (at the left-hand side) does not match the order in which they are
accessed (at the right-hand side), and the backported `TypeAliasType` must be used
instead.

### Functions

```console
$ unpy --target 3.10 --diff examples/functions.pyi
```

```diff
+++ -
@@ -1,6 +1,11 @@
+ _T = TypeVar("_T")
+ _S = TypeVar("_S", str, bytes)
+ _X = TypeVar("_X")
+ _Theta = ParamSpec("_Theta")
+ _Y = TypeVar("_Y")
  from collections.abc import Callable as Def
- from typing import Concatenate as Concat
+ from typing import Concatenate as Concat, ParamSpec, TypeVar

- def noop[T](x: T, /) -> T: ...
- def concat[S: (str, bytes)](left: S, right: S) -> S: ...
- def curry[X, **Theta, Y](f: Def[Concat[X, Theta], Y], /) -> Def[[X], Def[Theta, Y]]: ...
+ def noop(x: _T, /) -> _T: ...
+ def concat(left: _S, right: _S) -> _S: ...
+ def curry(f: Def[Concat[_X, _Theta], _Y], /) -> Def[[_X], Def[_Theta, _Y]]: ...
```

### Generic classes and protocols

```console
$ unpy --target 3.10 --diff examples/generics.pyi
```

```diff
+++ -
@@ -1,17 +1,25 @@
- from typing import Protocol, overload
+ from typing import Generic, Protocol, overload
+ from typing_extensions import TypeVar
+
+ _T_contra = TypeVar("_T_contra", contravariant=True)
+ _T_co = TypeVar("_T_co", covariant=True)
+ _T = TypeVar("_T", infer_variance=True)
+ _D = TypeVar("_D")
+ _NameT = TypeVar("_NameT", infer_variance=True, bound=str)
+ _QualNameT = TypeVar("_QualNameT", infer_variance=True, bound=str, default=_NameT)

  class Boring: ...

- class CanGetItem[T_contra, T_co](Protocol):
-     def __getitem__(self, k: T_contra, /) -> T_co: ...
+ class CanGetItem(Protocol[_T_contra, _T_co]):
+     def __getitem__(self, k: _T_contra, /) -> _T_co: ...

- class Stack[T]:
-     def push(self, value: T, /) -> None: ...
+ class Stack(Generic[_T, _D]):
+     def push(self, value: _T, /) -> None: ...
      @overload
-     def pop(self, /) -> T: ...
+     def pop(self, /) -> _T: ...
      @overload
-     def pop[D](self, default: D, /) -> T | D: ...
+     def pop(self, default: _D, /) -> _T | _D: ...

- class Named[NameT: str, QualNameT: str = NameT]:
-     __name__: NameT
-     __qualname__: QualNameT
+ class Named(Generic[_NameT, _QualNameT]):
+     __name__: _NameT
+     __qualname__: _QualNameT
```

Note how `TypeVar` is (only) imported from `typing_extensions` here, which wasn't the
case in the previous example. This is a consequence of the `infer_variance` parameter,
which has been added in Python 3.12.

## Project goals

Here's the alpha version of a prototype of a rough sketch of some initial ideas for the
potential goals of `unpy`:

1. Towards the past
    - [x] Get frustrated while [stubbing scipy](https://github.com/jorenham/scipy-stubs)
    - [x] Transpile Python 3.13 `.pyi` stubs to Python 3.10 stubs
    - [ ] Package-level analysis and conversion
    - [ ] Tooling for stub-only project integration
    - [ ] Use this in [`scipy-stubs`](https://github.com/jorenham/scipy-stubs)
    - [ ] Gradually introduce this into [`numpy`](https://github.com/numpy/numpy)
2. Towards the future
    - [ ] Beyond Python: $\text{Unpy} \supset \text{Python}$
    - [ ] Language support & tooling for *all* `.py` projects
3. Towards each other
    - [ ] Unified typechecking: Fast, reasonable, and language-agnostic

## Features

### Tooling

- Target Python versions
    - [x] `3.13`
    - [x] `3.12`
    - [x] `3.11`
    - [x] `3.10`
    - [ ] `3.9`
- Language support
    - [x] `.pyi`
    - [ ] `.py`
- Conversion
    - [x] stdin => stdout
    - [x] module => module
    - [ ] package => package
    - [ ] project => project (including the `pyproject.toml`)
- Configuration
    - [x] `--diff`: Unified diffs
    - [x] `--target`: Target Python version, defaults to `3.10`
    - [ ] Project-based config in `pyproject.toml` under `[tools.unpy]`
    - [ ] ...
- Integration
    - [ ] File watcher
    - [ ] Pre-commit
    - [ ] LSP
    - [ ] UV
    - [ ] VSCode extension
    - [ ] (based)mypy plugin
    - [ ] Project build tools
    - [ ] Configurable type-checker integration
    - [ ] Configurable formatter integration, e.g. `ruff format`
- Performance
    - [ ] Limit conversion to changed files

### Stub backporting

- Python 3.13 => 3.12
    - [PEP 742][PEP742]
        - `typing.TypeIs` => `typing_extensions.TypeIs`
    - [PEP 705][PEP705]
        - `typing.ReadOnly` => `typing_extensions.ReadOnly`
    - [PEP 702][PEP702]
        - `warnings.deprecated` => `typing_extensions.deprecated`
    - [PEP 696][PEP696]
        - Backport [PEP 695][PEP695] type signatures with a default
        - `typing.NoDefault` => `typing_extensions.NoDefault`
    - Exceptions
        - `asyncio.QueueShutDown` => `builtins.Exception`
        - `pathlib.UnsupportedOperation` => `builtins.NotImplementedError`
        - `queue.ShutDown` => `builtins.Exception`
        - `re.PatternError` => `re.error`
    - Typing
        - `types.CapsuleType` => `typing_extensions.CapsuleType`
        - `typing.{ClassVar,Final}` => `typing_extensions.{ClassVar,Final}` when
        nested
- Python 3.12 => 3.11
    - [PEP 698][PEP698]
        - `typing.override` => `typing_extensions.override`
    - [PEP 695][PEP695]
        - Backport `type _` aliases
        - Backport generic functions
        - Backport generic classes and protocols
        - `typing.TypeAliasType` => `typing_extensions.TypeAliasType`
    - [PEP 688][PEP688]
        - `collections.abc.Buffer` => `typing_extensions.Buffer`
        - `inspect.BufferFlags` => `int`
- Python 3.11 => 3.10
    - [PEP 681][PEP681]
        - `typing.dataclass_transform` => `typing_extensions.dataclass_transform`
    - [PEP 675][PEP675]
        - `typing.LiteralString` => `typing_extensions.LiteralString`
    - [PEP 673][PEP673]
        - `typing.Self` => `typing_extensions.Self`
    - [PEP 655][PEP655]
        - `typing.[Not]Required` => `typing_extensions.[Not]Required`
    - [PEP 654][PEP654]
        - ~`builtins.BaseExceptionGroup`~
        - ~`builtins.ExceptionGroup`~
    - [PEP 646][PEP646]
        - `typing.TypeVarTuple` => `typing_extensions.TypeVarTuple`
        - `typing.Unpack` => `typing_extensions.Unpack`
        - `*Ts` => `typing_extensions.Unpack[Ts]` with `Ts: TypeVarTuple`
    - `asyncio`
        - ~`asyncio.TaskGroup`~
    - `enum`
        - `enum.ReprEnum` => `enum.Enum`
        - `enum.StrEnum` => `str & enum.Enum`
    - `typing`
        - `typing.Any` => `typing_extensions.Any` if subclassed (not recommended)
- Generated `TypeVar`s
    - [x] De-duplicate extracted typevar-likes with same name if equivalent
    - [x] Prefix the names of extracted typevar-likes with `_`
    - [ ] Rename incompatible typevar-likes with the same name (jorenham/unpy#86)

### Simplification and refactoring

- Generic type parameters
    - [x] Convert `default=Any` with `bound=T` to `default=T`
    - [x] Remove `bound=Any` and `bound=object`
    - [ ] Infer variance of PEP 695 type parameters (jorenham/unpy#44)
        - [ ] If never used, it's redundant (and bivariant) (jorenham/unpy#46)
        - [x] If constraints are specified, it's `invariant`
        - [x] If suffixed with `_co`/`_contra`, it's `covariant`/`contravariant`
        - [ ] If used as public instance attribute, it's `invariant`
        - [ ] If only used as return-type (excluding `__init__` and `__new__`), or for
        read-only attributes, it's `covariant`
        - [ ] If only used as parameter-type, it's `contravariant`
        - [ ] Otherwise, assume it's `invariant`
- Methods
    - [ ] Default return types for specific "special method" (jorenham/unpy#55)
    - [ ] Transform `self` method parameters to be positional-only
- Typing operators
    - [ ] `type[S] | type[T]` => `type[S | T]`
    - [ ] Flatten & de-duplicate unions of literals
    - [ ] Remove redundant union values, e.g. `bool | int` => `int`

### Beyond Python

- [ ] `@sealed` types (jorenham/unpy/#42)
- [ ] Unified type-ignore comments (jorenham/unpy/#68)
- [ ] Set-based `Literal` syntax (jorenham/unpy/#76)
- [ ] Reusable method signature definitions
- [ ] Type-mappings, a DRY alternative to `@overload`
- [ ] Intersection types (as implemented in [basedmypy][BMP-ISEC])
- [ ] Higher-kinded types (see python/typing#548)
- [ ] Inline callable types (inspired by [PEP 677][PEP677])

[PEP646]: https://peps.python.org/pep-0646/
[PEP654]: https://peps.python.org/pep-0654/
[PEP655]: https://peps.python.org/pep-0655/
[PEP673]: https://peps.python.org/pep-0673/
[PEP675]: https://peps.python.org/pep-0675/
[PEP677]: https://peps.python.org/pep-0677/
[PEP681]: https://peps.python.org/pep-0681/
[PEP688]: https://peps.python.org/pep-0688/
[PEP695]: https://peps.python.org/pep-0695/
[PEP696]: https://peps.python.org/pep-0696/
[PEP698]: https://peps.python.org/pep-0698/
[PEP702]: https://peps.python.org/pep-0702/
[PEP705]: https://peps.python.org/pep-0705/
[PEP742]: https://peps.python.org/pep-0705/
[BMP-ISEC]: https://github.com/KotlinIsland/basedmypy#intersection-types
