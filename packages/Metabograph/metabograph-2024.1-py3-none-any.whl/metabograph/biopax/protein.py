#!/usr/bin/env
"""
Protein-specific methods for .
"""

import logging

import pandas as pd


LOGGER = logging.getLogger(__name__)


def get_uniprot_id(row, bqm):
    """
    Get the UniProt ID for a row if it exists.

    Args:
        row:
            The row from the dataframe of entities.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        The UniProt ID, or None.
    """
    xrefs = row["xrefs"]
    if not xrefs or pd.isna(xrefs):
        return None
    for xref in xrefs.split(bqm.ITEM_DELIMITER):
        name, value = xref.split(bqm.FIELD_DELIMITER)
        if "UniProt" in name:
            return value
    return None


def _map_members_to_uniprot_ids(row, bqm, uniprot_dict):
    """
    Application function for map_members_to_uniprot_ids.
    """
    members = row["members"]
    if not members or pd.isna(members):
        return None
    uniprot_ids = set()
    for member in members.split(bqm.ITEM_DELIMITER):
        uniprot_id = uniprot_dict.get(member)
        if uniprot_id and not pd.isna(uniprot_id):
            uniprot_ids.add(uniprot_id)
    if uniprot_ids:
        return bqm.ITEM_DELIMITER.join(sorted(uniprot_ids))
    return None


def map_members_to_uniprot_ids(data, bqm):
    """
    Get a series with UniProt IDs of the members in the members column.

    Args:
        data:
            The entity dataframe.

        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        A Pandas series with the UniProt IDs.
    """
    uniprot_dict = data.set_index("entity").to_dict()["uniprot"]
    return data.apply(_map_members_to_uniprot_ids, axis=1, args=(bqm, uniprot_dict))


def get_protein_entities(bqm):
    """
    Get the dataframe of protein entities.

    Args:
        bqm:
            An instance of :py:class:`~.query_manager.BiopaxQueryManager`.

    Returns:
        A Pandas DataFrame.
    """
    phys_ents = bqm.query_physical_entities().merge(
        bqm.query_locations(), how="left", on="entity"
    )
    prots = phys_ents[phys_ents["entity"].str.contains("Protein")].copy()
    if prots.shape[0] != prots["entity"].nunique():
        LOGGER.warning("Duplicate protein entities found in dataframe")

    no_display_name = prots["display_names"].isna()
    if no_display_name.any():
        n_missing = no_display_name.sum()
        LOGGER.warning(
            "%d entit%s missing a display name",
            n_missing,
            "y is" if n_missing == 1 else "ies are",
        )
        no_other_name = prots[no_display_name]["names"].isna()
        if no_other_name.any():
            n_missing = no_other_name.sum()
            LOGGER.warning(
                "%d entit%s have no name at all",
                n_missing,
                "y" if n_missing == 1 else "ies",
            )

    multiple_display_name = prots["display_names"].str.contains(bqm.ITEM_DELIMITER)
    if multiple_display_name.any():
        n_multi = multiple_display_name.sum()
        LOGGER.warning(
            "%d entit%s have multiple display names",
            n_multi,
            "y" if n_multi == 1 else "ies",
        )

    prots["uniprot"] = prots.apply(get_uniprot_id, axis=1, args=(bqm,))
    prots["member_uniprot"] = map_members_to_uniprot_ids(prots, bqm)

    return prots
