import ast
import sys
from os import path as op
from warnings import warn

import pandas as pd
from pangeo_forge_cordex.catalog import catalog_entry, path
from pangeo_forge_cordex.parsing import project_from_iid

bucket = "euro-cordex"
df_url_template = f"https://cmip6-pds.s3.amazonaws.com/{bucket}/catalog"


def get_url(bucket, prefix="", fs="s3"):
    return f"{fs}://{op.join(bucket, prefix)}"


def get_zarr_url(iid, bucket, prefix="", fs="s3"):
    return f"{op.join(get_url(bucket, prefix, fs), path(iid))}"


def get_catalog_url(bucket, project, prefix="catalog"):
    if project in ["CORDEX", "CORDEX-Reklies", "CORDEX-FPSCONV"]:
        # these go all in the same catalog (they have the same facets)
        catalog = "CORDEX"
    else:
        catalog = project
    return f"{op.join(get_url(bucket, prefix), catalog)}.csv"


def add_entry(iid):
    project_id = project_from_iid(iid)

    url = get_zarr_url(iid, bucket, "CMIP5", "s3")
    entry = catalog_entry(iid, url)
    cat_url = get_catalog_url(bucket, project_id)
    print(f"project_id: {project_id}")
    print(f"URL: {url}")
    print(f"Catalog url: {cat_url}")
    print(f"Catalog entry\n:{entry}")

    # get existing catalog
    try:
        catalog = pd.read_csv(cat_url)
        print(f"Found catalog: {cat_url}")
    except Exception:
        warn(f"Catalog does not exist yet: {cat_url}")
        catalog = None

    # update catalog
    if catalog is not None:
        cat = pd.concat([catalog, entry], ignore_index=True)
        if cat.duplicated().any():
            duplicates = cat.where(cat.duplicated()).dropna()
            warn(f"Found duplicates in catalog: {duplicates}")
        else:
            catalog = cat
    else:
        # start new catalog
        catalog = entry

    # write catalog
    print(f"updating catalog at {cat_url}")
    catalog.to_csv(cat_url, index=False)


def update_catalog(iids):
    if not isinstance(iids, list):
        iids = [iids]
    for iid in iids:
        add_entry(iid)


if __name__ == "__main__":
    iids = ast.literal_eval(sys.argv[1])
    update_catalog(iids)
