
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe

from pangeo_forge_cordex import recipe_inputs_from_iids, logon



def test_recipe_inputs():
    
    iid = 'cordex.output.EUR-11.GERICS.ECMWF-ERAINT.evaluation.r1i1p1.REMO2015.v1.day.tas.v20180813'
    sslcontext = logon()
    
    recipe_inputs = recipe.recipe_inputs_from_iids(iid, sslcontext)
    
    urls = recipe_inputs[iid]["urls"]
    recipe_kwargs = recipe_inputs[iid]["recipe_kwargs"]
    pattern_kwargs = recipe_inputs[iid]["pattern_kwargs"]
    
    pattern = pattern_from_file_sequence(urls, "time", **pattern_kwargs)
    recipe = XarrayZarrRecipe(
        pattern, xarray_concat_kwargs={"join": "exact"}, **recipe_kwargs
    )

