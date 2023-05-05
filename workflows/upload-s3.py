# import sys

import xarray as xr
from pangeo_forge_cordex import logon, recipe_inputs_from_iids
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe


def upload_s3(iid):
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
        **recipe_kwargs
    )

    #recipe_pruned = recipe.copy_pruned()
    run_function = recipe.to_function()

    run_function()

    ds = xr.open_zarr(recipe.target_mapper, consolidated=True)

    print(ds)


if __name__ == "__main__":
    # ids = sys.argv[1].replace("`", "")
    # iids = parse_instance_ids(ids)
    # total_size = total_size_ids(ids)
    # pprint.pprint(iids)
    # pprint.pprint(total_size)
    iid = "cordex.output.EUR-11.GERICS.ECMWF-ERAINT.evaluation.r1i1p1.REMO2015.v1.mon.tas.v20180813"
    upload_s3(iid)
