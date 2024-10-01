from fluid_sbom.internal.package_information.dart import (
    get_pub_package,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.utils.file import (
    Digest,
)


def complete_package(package: Package) -> Package:
    pub_package = get_pub_package(package.name)
    if not pub_package:
        return package

    current_package = next(
        (
            version
            for version in pub_package["versions"]
            if version["version"] == package.version
        ),
        None,
    )
    package.health_metadata = HealthMetadata(
        latest_version=pub_package["latest"]["version"],
        latest_version_created_at=pub_package["latest"]["published"],
    )
    if current_package:
        package.health_metadata.artifact = Artifact(
            url=current_package["archive_url"],
            integrity=Digest(
                value=current_package["archive_sha256"],
                algorithm="sha256",
            ),
        )

    package.health_metadata.authors = next(
        (
            version["pubspec"]["author"]
            for version in reversed(pub_package["versions"])
            if "author" in version["pubspec"]
        ),
        None,
    )

    return package
