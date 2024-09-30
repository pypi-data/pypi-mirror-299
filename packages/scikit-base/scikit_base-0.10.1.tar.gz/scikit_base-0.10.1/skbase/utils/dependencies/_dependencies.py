# -*- coding: utf-8 -*-
"""Utility to check soft dependency imports, and raise warnings or errors."""
import sys
import warnings
from functools import lru_cache
from inspect import isclass

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, Specifier, SpecifierSet
from packaging.version import InvalidVersion, Version


def _check_soft_dependencies(
    *packages,
    package_import_alias="deprecated",
    severity="error",
    obj=None,
    msg=None,
):
    """Check if required soft dependencies are installed and raise error or warning.

    Parameters
    ----------
    packages : str or list/tuple of str, or length-1-tuple containing list/tuple of str
        str should be package names and/or package version specifications to check.
        Each str must be a PEP 440 compatible specifier string, for a single package.
        For instance, the PEP 440 compatible package name such as ``"pandas"``;
        or a package requirement specifier string such as ``"pandas>1.2.3"``.
        arg can be str, kwargs tuple, or tuple/list of str, following calls are valid:
        ``_check_soft_dependencies("package1")``
        ``_check_soft_dependencies("package1", "package2")``
        ``_check_soft_dependencies(("package1", "package2"))``
        ``_check_soft_dependencies(["package1", "package2"])``

    package_import_alias : ignored, present only for backwards compatibility

    severity : str, "error" (default), "warning", "none"
        whether the check should raise an error, a warning, or nothing

        * "error" - raises a ``ModuleNotFoundError`` if one of packages is not installed
        * "warning" - raises a warning if one of packages is not installed
          function returns False if one of packages is not installed, otherwise True
        * "none" - does not raise exception or warning
          function returns False if one of packages is not installed, otherwise True

    obj : python class, object, str, or None, default=None
        if self is passed here when _check_soft_dependencies is called within __init__,
        or a class is passed when it is called at the start of a single-class module,
        the error message is more informative and will refer to the class/object;
        if str is passed, will be used as name of the class/object or module

    msg : str, or None, default=None
        if str, will override the error message or warning shown with msg

    Raises
    ------
    InvalidRequirement
        if package requirement strings are not PEP 440 compatible
    ModuleNotFoundError
        error with informative message, asking to install required soft dependencies
    TypeError, ValueError
        on invalid arguments

    Returns
    -------
    boolean - whether all packages are installed, only if no exception is raised
    """
    if len(packages) == 1 and isinstance(packages[0], (tuple, list)):
        packages = packages[0]
    if not all(isinstance(x, str) for x in packages):
        raise TypeError(
            "packages argument of _check_soft_dependencies must be str or tuple of "
            f"str, but found packages argument of type {type(packages)}"
        )

    if obj is None:
        class_name = "This functionality"
    elif not isclass(obj):
        class_name = type(obj).__name__
    elif isclass(obj):
        class_name = obj.__name__
    elif isinstance(obj, str):
        class_name = obj
    else:
        raise TypeError(
            "obj argument of _check_soft_dependencies must be a class, an object,"
            " a str, or None, but found obj of type"
            f" {type(obj)}"
        )

    if msg is not None and not isinstance(msg, str):
        raise TypeError(
            "msg argument of _check_soft_dependencies must be a str, "
            f"or None, but found msg of type {type(msg)}"
        )

    for package in packages:
        try:
            req = Requirement(package)
            req = _normalize_requirement(req)
        except InvalidRequirement:
            msg_version = (
                f"wrong format for package requirement string, "
                f"passed via packages argument of _check_soft_dependencies, "
                f'must be PEP 440 compatible requirement string, e.g., "pandas"'
                f' or "pandas>1.1", but found {package!r}'
            )
            raise InvalidRequirement(msg_version) from None

        package_name = req.name
        package_version_req = req.specifier

        pkg_env_version = _get_pkg_version(package_name)

        # if package not present, make the user aware of installation reqs
        if pkg_env_version is None:
            if obj is None and msg is None:
                msg = (
                    f"{class_name} requires package {package!r} to be present "
                    f"in the python environment, but {package!r} was not found. "
                )
            elif msg is None:  # obj is not None, msg is None
                msg = (
                    f"{class_name} requires package {package!r} to be present "
                    f"in the python environment, but {package!r} was not found. "
                    f"{package!r} is a dependency of {class_name} and required "
                    f"to construct it. "
                )
            msg = msg + (
                f"Please run: `pip install {package}` to "
                f"install the {package} package. "
            )
            # if msg is not None, none of the above is executed,
            # so if msg is passed it overrides the default messages

            _raise_at_severity(msg, severity, caller="_check_soft_dependencies")
            return False

        # now we check compatibility with the version specifier if non-empty
        if package_version_req != SpecifierSet(""):
            msg = (
                f"{class_name} requires package {package!r} to be present "
                f"in the python environment, with version {package_version_req}, "
                f"but incompatible version {pkg_env_version} was found. "
            )
            if obj is not None:
                msg = msg + (
                    f"{package!r}, with version {package_version_req},"
                    f"is a dependency of {class_name} and required to construct it. "
                )

            # raise error/warning or return False if version is incompatible
            if pkg_env_version not in package_version_req:
                _raise_at_severity(msg, severity, caller="_check_soft_dependencies")
                return False

    # if package can be imported and no version issue was caught for any string,
    # then obj is compatible with the requirements and we should return True
    return True


@lru_cache
def _get_installed_packages_private():
    """Get a dictionary of installed packages and their versions.

    Same as _get_installed_packages, but internal to avoid mutating the lru_cache
    by accident.
    """
    from importlib.metadata import distributions, version

    dists = distributions()
    package_names = {dist.metadata["Name"] for dist in dists}
    package_versions = {pkg_name: version(pkg_name) for pkg_name in package_names}
    # developer note:
    # we cannot just use distributions naively,
    # because the same top level package name may appear *twice*,
    # e.g., in a situation where a virtual env overrides a base env,
    # such as in deployment environments like databricks.
    # the "version" contract ensures we always get the version that corresponds
    # to the importable distribution, i.e., the top one in the sys.path.
    return package_versions


def _get_installed_packages():
    """Get a dictionary of installed packages and their versions.

    Returns
    -------
    dict : dictionary of installed packages and their versions
        keys are PEP 440 compatible package names, values are package versions
        MAJOR.MINOR.PATCH version format is used for versions, e.g., "1.2.3"
    """
    return _get_installed_packages_private().copy()


def _get_pkg_version(package_name):
    """Check whether package is available in environment, and return its version if yes.

    Returns ``Version`` object from ``lru_cache``, this should not be mutated.

    Parameters
    ----------
    package_name : str, optional, default=None
        name of package to check,
        PEP 440 compatibe specifier string, e.g., "pandas" or "sklearn".
        This is the pypi package name, not the import name, e.g.,
        ``scikit-learn``, not ``sklearn``.

    Returns
    -------
    None, if package is not found in python environment.
    ``importlib`` ``Version`` of package, if present in environment.
    """
    pkgs = _get_installed_packages()
    pkg_vers_str = pkgs.get(package_name, None)
    if pkg_vers_str is None:
        return None
    try:
        pkg_env_version = Version(pkg_vers_str)
    except InvalidVersion:
        pkg_env_version = None
    return pkg_env_version


def _check_python_version(obj, package=None, msg=None, severity="error"):
    """Check if system python version is compatible with requirements of obj.

    Parameters
    ----------
    obj : BaseObject descendant
        used to check python version

    package : str, default = None
        if given, will be used in error message as package name

    msg : str, optional, default = default message (msg below)
        error message to be returned in the ``ModuleNotFoundError``, overrides default

    severity : str, "error" (default), "warning", "none"
        whether the check should raise an error, a warning, or nothing

        * "error" - raises a ``ModuleNotFoundError`` if one of packages is not installed
        * "warning" - raises a warning if one of packages is not installed
          function returns False if one of packages is not installed, otherwise True
        * "none" - does not raise exception or warning
          function returns False if one of packages is not installed, otherwise True

    Returns
    -------
    compatible : bool, whether obj is compatible with system python version
        check is using the python_version tag of obj

    Raises
    ------
    ModuleNotFoundError
        User friendly error if obj has python_version tag that is
        incompatible with the system python version. If package is given,
        error message gives package as the reason for incompatibility.
    """
    est_specifier_tag = obj.get_class_tag("python_version", tag_value_default="None")
    if est_specifier_tag in ["None", None]:
        return True

    try:
        est_specifier = SpecifierSet(est_specifier_tag)
    except InvalidSpecifier:
        msg_version = (
            f"wrong format for python_version tag, "
            f'must be PEP 440 compatible specifier string, e.g., "<3.9, >= 3.6.3",'
            f" but found {est_specifier_tag!r}"
        )
        raise InvalidSpecifier(msg_version) from None

    # python sys version, e.g., "3.8.12"
    sys_version = sys.version.split(" ")[0]

    if sys_version in est_specifier:
        return True
    # now we know that est_version is not compatible with sys_version

    if isclass(obj):
        class_name = obj.__name__
    else:
        class_name = type(obj).__name__

    if not isinstance(msg, str):
        msg = (
            f"{class_name} requires python version to be {est_specifier},"
            f" but system python version is {sys.version}."
        )

        if package is not None:
            msg += (
                f" This is due to python version requirements of the {package} package."
            )

    _raise_at_severity(msg, severity, caller="_check_python_version")
    return False


def _check_env_marker(obj, package=None, msg=None, severity="error"):
    """Check if packaging marker tag is with requirements of obj.

    Parameters
    ----------
    obj : BaseObject descendant
        used to check python version
    package : str, default = None
        if given, will be used in error message as package name
    msg : str, optional, default = default message (msg below)
        error message to be returned in the `ModuleNotFoundError`, overrides default

    severity : str, "error" (default), "warning", "none"
        whether the check should raise an error, a warning, or nothing

        * "error" - raises a ``ModuleNotFoundError`` if one of packages is not installed
        * "warning" - raises a warning if one of packages is not installed
          function returns False if one of packages is not installed, otherwise True
        * "none" - does not raise exception or warning
          function returns False if one of packages is not installed, otherwise True

    Returns
    -------
    compatible : bool, whether obj is compatible with system python version
        check is using the python_version tag of obj

    Raises
    ------
    InvalidMarker
        User friendly error if obj has env_marker tag that is not a
        packaging compatible marker string
    ModuleNotFoundError
        User friendly error if obj has an env_marker tag that is
        incompatible with the python environment. If package is given,
        error message gives package as the reason for incompatibility.
    """
    est_marker_tag = obj.get_class_tag("env_marker", tag_value_default="None")
    if est_marker_tag in ["None", None]:
        return True

    try:
        est_marker = Marker(est_marker_tag)
    except InvalidMarker:
        msg_version = (
            f"wrong format for env_marker tag, "
            f"must be PEP 508 compatible specifier string, e.g., "
            f'platform_system!="windows", but found {est_marker_tag!r}'
        )
        raise InvalidMarker(msg_version) from None

    if est_marker.evaluate():
        return True
    # now we know that est_marker is not compatible with the environment

    if isclass(obj):
        class_name = obj.__name__
    else:
        class_name = type(obj).__name__

    if not isinstance(msg, str):
        msg = (
            f"{class_name} requires an environment to satisfy "
            f"packaging marker spec {est_marker}, but environment does not satisfy it."
        )

        if package is not None:
            msg += f" This is due to requirements of the {package} package."

    _raise_at_severity(msg, severity, caller="_check_env_marker")
    return False


def _check_estimator_deps(obj, msg=None, severity="error"):
    """Check if object/estimator's package & python requirements are met by python env.

    Convenience wrapper around `_check_python_version` and `_check_soft_dependencies`,
    checking against estimator tags `"python_version"`, `"python_dependencies"`.

    Checks whether dependency requirements of `BaseObject`-s in `obj`
    are satisfied by the current python environment.

    Parameters
    ----------
    obj : BaseObject descendant, instance or class, or list/tuple thereof
        object(s) that this function checks compatibility of, with the python env

    msg : str, optional, default = default message (msg below)
        error message to be returned in the ``ModuleNotFoundError``, overrides default

    severity : str, "error" (default), "warning", "none"
        whether the check should raise an error, a warning, or nothing

        * "error" - raises a ``ModuleNotFoundError`` if one of packages is not installed
        * "warning" - raises a warning if one of packages is not installed
          function returns False if one of packages is not installed, otherwise True
        * "none" - does not raise exception or warning
          function returns False if one of packages is not installed, otherwise True

    Returns
    -------
    compatible : bool, whether `obj` is compatible with python environment
        False is returned only if no exception is raised by the function
        checks for python version using the python_version tag of obj
        checks for soft dependencies present using the python_dependencies tag of obj
        if `obj` contains multiple `BaseObject`-s, checks whether all are compatible

    Raises
    ------
    ModuleNotFoundError
        User friendly error if obj has python_version tag that is
        incompatible with the system python version.
        Compatible python versions are determined by the "python_version" tag of obj.
        User friendly error if obj has package dependencies that are not satisfied.
        Packages are determined based on the "python_dependencies" tag of obj.
    """
    compatible = True

    # if list or tuple, recurse & iterate over element, and return conjunction
    if isinstance(obj, (list, tuple)):
        for x in obj:
            x_chk = _check_estimator_deps(x, msg=msg, severity=severity)
            compatible = compatible and x_chk
        return compatible

    compatible = compatible and _check_python_version(obj, severity=severity)
    compatible = compatible and _check_env_marker(obj, severity=severity)

    pkg_deps = obj.get_class_tag("python_dependencies", None)
    pck_alias = obj.get_class_tag("python_dependencies_alias", None)
    if pkg_deps is not None and not isinstance(pkg_deps, list):
        pkg_deps = [pkg_deps]
    if pkg_deps is not None:
        pkg_deps_ok = _check_soft_dependencies(
            *pkg_deps, severity=severity, obj=obj, package_import_alias=pck_alias
        )
        compatible = compatible and pkg_deps_ok

    return compatible


def _normalize_requirement(req):
    """Normalize packaging Requirement by removing build metadata from versions.

    Parameters
    ----------
    req : packaging.requirements.Requirement
        requirement string to normalize, e.g., Requirement("pandas>1.2.3+foobar")

    Returns
    -------
    normalized_req : packaging.requirements.Requirement
        normalized requirement object with build metadata removed from versions,
        e.g., Requirement("pandas>1.2.3")
    """
    # Process each specifier in the requirement
    normalized_specs = []
    for spec in req.specifier:
        # Parse the version and remove the build metadata
        spec_v = Version(spec.version)
        version_wo_build_metadata = f"{spec_v.major}.{spec_v.minor}.{spec_v.micro}"

        # Create a new specifier without the build metadata
        normalized_spec = Specifier(f"{spec.operator}{version_wo_build_metadata}")
        normalized_specs.append(normalized_spec)

    # Reconstruct the specifier set
    normalized_specifier_set = SpecifierSet(",".join(str(s) for s in normalized_specs))

    # Create a new Requirement object with the normalized specifiers
    normalized_req = Requirement(f"{req.name}{normalized_specifier_set}")

    return normalized_req


def _raise_at_severity(
    msg,
    severity,
    exception_type=None,
    warning_type=None,
    stacklevel=2,
    caller="_raise_at_severity",
):
    """Raise exception or warning or take no action, based on severity.

    Parameters
    ----------
    msg : str
        message to raise or warn

    severity : str, "error" (default), "warning", "none"
        whether the check should raise an error, a warning, or nothing

        * "error" - raises a ``ModuleNotFoundError`` if one of packages is not installed
        * "warning" - raises a warning if one of packages is not installed
          function returns False if one of packages is not installed, otherwise True
        * "none" - does not raise exception or warning
          function returns False if one of packages is not installed, otherwise True

    exception_type : Exception, default=ModuleNotFoundError
        exception type to raise if severity="severity"
    warning_type : warning, default=Warning
        warning type to raise if severity="warning"
    stacklevel : int, default=2
        stacklevel for warnings, if severity="warning"
    caller : str, default="_raise_at_severity"
        caller name, used in exception if severity not in ["error", "warning", "none"]

    Returns
    -------
    None

    Raises
    ------
    exception : exception_type, if severity="error"
    warning : warning+type, if severity="warning"
    ValueError : if severity not in ["error", "warning", "none"]
    """
    if exception_type is None:
        exception_type = ModuleNotFoundError

    if severity == "error":
        raise exception_type(msg)
    elif severity == "warning":
        warnings.warn(msg, category=warning_type, stacklevel=stacklevel)
    elif severity == "none":
        return None
    else:
        raise ValueError(
            f"Error in calling {caller}, severity "
            f'argument must be "error", "warning", or "none", found {severity!r}.'
        )
    return None
