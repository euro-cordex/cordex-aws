import sys
from os import path as op
from warnings import warn

import fsspec
import pandas as pd
import xarray as xr
from pangeo_forge_cordex import logon, recipe_inputs_from_iids
from pangeo_forge_cordex.catalog import catalog_entry, path
from pangeo_forge_cordex.parsing import project_from_iid
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe

bucket = "euro-cordex"
df_url_template = f"https://cmip6-pds.s3.amazonaws.com/{bucket}/catalog"


def get_url(bucket, prefix="", fs="s3"):
    return f"{fs}://{op.join(bucket, prefix)}"


def get_zarr_url(iid, bucket, prefix="", fs="s3"):
    return f"{op.join(get_url(bucket, prefix, fs), path(iid))}"


def get_catalog_url(bucket, project, prefix="catalog"):
    if project == "CORDEX-Reklies":
        project = "CORDEX"
    catalog = project
    return f"{op.join(get_url(bucket, prefix), catalog)}.csv"


def run_recipe(iid):
    sslcontext = logon()

    recipe_inputs = recipe_inputs_from_iids(iid, sslcontext)

    urls = recipe_inputs[iid]["urls"]
    recipe_kwargs = recipe_inputs[iid]["recipe_kwargs"]
    pattern_kwargs = recipe_inputs[iid]["pattern_kwargs"]

    pattern = pattern_from_file_sequence(urls, "time", **pattern_kwargs)
    recipe = XarrayZarrRecipe(
        pattern,
        xarray_concat_kwargs={"join": "exact"},
        subset_inputs={"time": 5},
        **recipe_kwargs,
    )

    # recipe_pruned = recipe.copy_pruned()
    run_function = recipe.to_function()

    run_function()

    ds = xr.open_zarr(recipe.target_mapper, consolidated=True)

    print(ds)
    print("-----------------------------------")
    print(f"Actual size: {ds.nbytes / 1.e6} MB")

    return ds


def upload_s3(iid):
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
    print(catalog)
    # update catalog
    if catalog is not None:
        cat = pd.concat([catalog, entry], ignore_index=True)
        if cat.duplicated().any():
            duplicates = cat.where(cat.duplicated()).dropna()
            raise Exception(f"Found duplicates in catalog: {duplicates}")
        catalog = cat
    else:
        # start new catalog
        catalog = entry

    print("running recipe...")
    ds = run_recipe(iid)

    print("uploading to {url}")
    target = fsspec.get_mapper(url)
    ds.to_zarr(target, compute=True)

    # write catalog
    print(f"updating catalog at {cat_url}")
    catalog.to_csv(cat_url, index=False)


if __name__ == "__main__":
    iid = sys.argv[1].replace("`", "")
    # iids = parse_instance_ids(ids)
    # total_size = total_size_ids(ids)
    # pprint.pprint(iids)
    # pprint.pprint(total_size)
    #iid = "cordex.output.EUR-11.GERICS.ECMWF-ERAINT.evaluation.r1i1p1.REMO2015.v1.mon.tas.v20180813"
    upload_s3(iid)
