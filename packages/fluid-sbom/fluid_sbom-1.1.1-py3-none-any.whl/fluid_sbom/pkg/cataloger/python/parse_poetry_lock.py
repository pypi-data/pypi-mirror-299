from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection import (
    toml,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.python import (
    PythonRequirementsEntry,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.exceptions import (
    UnexpectedNode,
)
import logging
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def parse_poetry_lock(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []
    _content = reader.read_closer.read()
    try:
        toml_content: IndexedDict = toml.parse_toml_with_tree_sitter(_content)
    except UnexpectedNode:
        return [], []
    for package in toml_content.get("package", []):
        p_url = PackageURL(
            type="pypi",
            namespace="",
            name=package["name"],
            version=package["version"],
            qualifiers="",
            subpath="",
        ).to_string()
        try:
            packages.append(
                Package(
                    name=package["name"],
                    version=package["version"],
                    found_by=None,
                    locations=[
                        (
                            _get_location(
                                reader.location, package.position.start.line
                            )
                            if isinstance(package, IndexedDict)
                            else reader.location
                        )
                    ],
                    language=Language.PYTHON,
                    p_url=p_url,
                    metadata=PythonRequirementsEntry(
                        name=package["name"],
                        extras=[],
                        markers=p_url,
                    ),
                    licenses=[],
                    type=PackageType.PythonPkg,
                )
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types "
                "are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(include_url=False),
                        "location": reader.location.path(),
                    }
                },
            )
            continue
    for package in toml_content.get("package", []):
        _pkg = next(
            (pkg for pkg in packages if pkg.name == package["name"]), None
        )
        dependencies: list[str] = list(package.get("dependencies", {}).keys())
        if _pkg and dependencies:
            pkg_dependencies = [
                pkg
                for dep in dependencies
                for pkg in packages
                if pkg.name == dep
            ]
            for dep in pkg_dependencies:
                relationships.append(
                    Relationship(
                        from_=dep,
                        to_=_pkg,
                        type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                        data=None,
                    )
                )

    return packages, relationships
