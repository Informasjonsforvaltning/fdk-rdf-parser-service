from typing import Dict, List, Optional, Set

from fdk_rdf_parser_service.parser.classes import (
    Dataset,
    Distribution,
    MediaTypeOrExtent,
    ReferenceDataCode,
)

from .reference_data import DatasetReferenceData
from .utils import (
    extend_reference_data_code,
    extend_reference_data_code_list,
    extend_reference_types,
    remove_scheme_and_trailing_slash,
)


def extend_dataset_with_reference_data(
    dataset: Dataset, ref_data: DatasetReferenceData
) -> Dataset:
    dataset.accessRights = (
        extend_reference_data_code(dataset.accessRights, ref_data.rightsstatement)
        if dataset.accessRights
        else None
    )
    dataset.provenance = (
        extend_reference_data_code(dataset.provenance, ref_data.provenancestatement)
        if dataset.provenance
        else None
    )
    dataset.accrualPeriodicity = (
        extend_reference_data_code(dataset.accrualPeriodicity, ref_data.frequency)
        if dataset.accrualPeriodicity
        else None
    )
    dataset.language = extend_reference_data_code_list(
        dataset.language, ref_data.linguisticsystem
    )
    dataset.spatial = extend_reference_data_code_list(
        dataset.spatial, ref_data.location
    )
    dataset.distribution = extend_distributions(
        dataset.distribution, ref_data.openlicenses, ref_data.media_types
    )
    dataset.references = extend_reference_types(
        dataset.references, ref_data.referencetypes
    )

    return dataset


def extend_distributions(
    distributions: Optional[List[Distribution]],
    open_licenses: Optional[Dict[str, ReferenceDataCode]],
    ref_media_types: Optional[Dict[str, MediaTypeOrExtent]],
) -> Optional[List[Distribution]]:
    if distributions is None:
        return distributions
    else:
        extended_distributions = []
        for dist in distributions:
            if open_licenses is not None:
                if dist.license is not None:
                    extended_licenses = []
                    for lic in dist.license:
                        ref_code = (
                            open_licenses.get(remove_scheme_and_trailing_slash(lic.uri))
                            if lic.uri is not None
                            else None
                        )
                        if ref_code is not None:
                            dist.openLicense = True
                            if lic.prefLabel is None:
                                lic.prefLabel = ref_code.prefLabel
                        extended_licenses.append(lic)
                    dist.license = extended_licenses

            if ref_media_types:
                fdk_formats: Set[MediaTypeOrExtent] = set()

                if dist.fdkFormat:
                    ref_code_formats = []
                    for fmt in dist.fdkFormat:
                        ref_media_type = (
                            ref_media_types.get(
                                remove_scheme_and_trailing_slash(fmt.uri)
                            )
                            if fmt.uri
                            else None
                        )
                        if ref_media_type:
                            ref_code_formats.append(
                                ReferenceDataCode(
                                    uri=ref_media_type.uri,
                                    code=ref_media_type.code,
                                    prefLabel={"nb": ref_media_type.code}
                                    if ref_media_type.code
                                    else None,
                                )
                            )
                            fdk_formats.add(ref_media_type)
                        elif fmt.code:
                            fdk_formats.add(fmt)
                    dist.fdkFormat = list(fdk_formats) if len(fdk_formats) > 0 else None
                    dist.mediaType = (
                        ref_code_formats if len(ref_code_formats) > 0 else None
                    )

                if (
                    dist.compressFormat
                    and dist.compressFormat.uri
                    and ref_media_types.get(
                        remove_scheme_and_trailing_slash(dist.compressFormat.uri)
                    )
                ):
                    dist.compressFormat = ref_media_types[
                        remove_scheme_and_trailing_slash(dist.compressFormat.uri)
                    ]

                if (
                    dist.packageFormat
                    and dist.packageFormat.uri
                    and ref_media_types.get(
                        remove_scheme_and_trailing_slash(dist.packageFormat.uri)
                    )
                ):
                    dist.packageFormat = ref_media_types[
                        remove_scheme_and_trailing_slash(dist.packageFormat.uri)
                    ]

            extended_distributions.append(dist)
        return extended_distributions