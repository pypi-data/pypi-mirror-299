import logging
from math import e
from typing import List

from atscale.errors import atscale_errors
from atscale.base import enums, private_enums
from atscale.data_model.data_model import DataModel
from atscale.utils import feature_utils, project_utils, query_utils
from atscale.utils import model_utils, validation_utils, db_utils
from atscale.parsers import project_parser

logger = logging.getLogger(__name__)


def _write_regression_model_checks(
    model_type: private_enums.ScikitLearnModelType,
    data_model: DataModel,
    regression_model,
    new_feature_name: str,
    granularity_levels: List[str],
    feature_inputs: List[str],
):
    """A helper function for writing regression models to AtScale.

    Args:
        model_type (enums.private_enums.ScikitLearnModelType): the type of scikit-learn model being written to AtScale.
        data_model (DataModel): The AtScale DataModel to add the regression into.
        regression_model (LinearRegression): The scikit-learn LinearRegression model to build into a feature.
        new_feature_name (str): The name of the created feature.
        granularity_levels (List[str], optional): List of the query names for the categorical levels with the greatest
        levels of granularity that predictions with this model can be run on.
    """

    if not granularity_levels:
        raise ValueError(
            "The granularity_levels parameter was passed as either None or empty. "
            "Predictions must be joined to at least one level of a hierarchy."
        )

    model_failure = False
    # TODO at some point we may want to generalize this and remove the enum so we can take any model object and just check it is a type we support.
    # if not isinstance(regression_model, sklearn.linear_model.LinearRegression) and not isinstance(regression_model, sklearn.linear_model.LogisticRegression):
    # raise atscale_errors.WorkFlowError(
    #        f"The model object of type: {type(regression_model)} is not compatible with this method "
    #        f"which takes an object of type sklearn.linear_model.LinearRegression or sklearn.linear_model.LogisticRegression"
    #    )
    #

    if model_type == private_enums.ScikitLearnModelType.LINEARREGRESSION:
        if type(regression_model).__name__ not in ["LinearRegression"]:
            model_failure = True
    elif model_type == private_enums.ScikitLearnModelType.LOGISTICREGRESSION:
        if type(regression_model).__name__ not in ["LogisticRegression"]:
            model_failure = True

    if model_failure:
        raise atscale_errors.WorkFlowError(
            f"The model object of type: {type(regression_model)} is not compatible with this method "
            f"which takes an object of type sklearn.linear_model.{model_type.value}"
        )

    try:
        import sklearn
    except ImportError:
        raise ImportError(
            "scikit-learn needs to be installed to use this functionality, the function takes an "
            f"sklearn.linear_model.{model_type.value} object. Try running pip install scikit-learn"
        )

    model_failure = False

    if model_type == private_enums.ScikitLearnModelType.LINEARREGRESSION:
        if not isinstance(regression_model, sklearn.linear_model.LinearRegression):
            model_failure = True
    elif model_type == private_enums.ScikitLearnModelType.LOGISTICREGRESSION:
        if not isinstance(regression_model, sklearn.linear_model.LogisticRegression):
            model_failure = True

    if model_failure:
        raise atscale_errors.WorkFlowError(
            f"The model object of type: {type(regression_model)} is not compatible with this method "
            f"which takes an object of type sklearn.linear_model.{model_type.value}"
        )

    feature_list = granularity_levels + feature_inputs
    if feature_list:
        model_utils._check_features(
            features_check_tuples=[(feature_list, private_enums.CheckFeaturesErrMsg.ALL)],
            feature_dict=data_model.get_features(use_published=True),
            is_feat_published=True,
        )

    model_utils._check_conflicts(to_add=new_feature_name, data_model=data_model)


def _write_regression_model(
    model_type: private_enums.ScikitLearnModelType,
    data_model: DataModel,
    regression_model,
    new_feature_name: str,
    feature_inputs: List[str],
    granularity_levels: List[str],
):
    """A helper function for writing regression models to AtScale.

    Args:
        model_type (enums.private_enums.ScikitLearnModelType): the type of scikit-learn model being written to AtScale.
        data_model (DataModel): The AtScale DataModel to add the regression into.
        regression_model (sklearn.linear_model): The scikit-learn linear model to build into a feature.
        new_feature_name (str): The name of the created feature.
        feature_inputs (List[str]): List of names of inputs features in the input order.
        granularity_levels (List[str]): List of lowest categorical levels that predictions with this
            model can be run on.
    """
    _write_regression_model_checks(
        model_type=model_type,
        data_model=data_model,
        regression_model=regression_model,
        new_feature_name=new_feature_name,
        granularity_levels=granularity_levels,
        feature_inputs=feature_inputs,
    )

    atscale_query: str = query_utils._generate_atscale_query(
        data_model=data_model, feature_list=feature_inputs + granularity_levels
    )
    feature_query: str = query_utils._generate_db_query(
        data_model=data_model, atscale_query=atscale_query, use_aggs=False
    )

    project_dict = data_model.project._get_dict()
    warehouse_id = validation_utils._validate_warehouse_id_parameter(
        atconn=data_model.project._atconn, project_dict=project_dict
    )

    db_platform = data_model.project._atconn._get_warehouse_platform(warehouse_id=warehouse_id)
    db_conn = db_platform.dbconn
    quote = db_conn._column_quote()

    feature_query = f"({feature_query}) AS {quote}base_query{quote}"

    numeric = " + ".join(
        [
            f"{theta1}*{quote}base_query{quote}.{quote}{x}{quote}"
            for theta1, x in zip(regression_model.coef_[0], feature_inputs)
        ]
    )
    numeric += f" + {regression_model.intercept_[0]}"
    if model_type == private_enums.ScikitLearnModelType.LINEARREGRESSION:
        numeric = f"({numeric}) as {quote}{new_feature_name}{quote}"
    elif model_type == private_enums.ScikitLearnModelType.LOGISTICREGRESSION:
        numeric: str = (
            f"ROUND(1 - 1 / (1 + POWER({e}, {numeric})), 0) as {quote}{new_feature_name}{quote}"
        )

    feature_dict = data_model.get_features(
        feature_type=enums.FeatureType.CATEGORICAL, use_published=False
    )
    join_features = [feature_dict[x].get("base_name", x) for x in granularity_levels]
    roleplay_features = [
        feature_dict[x].get("roleplay_expression", "{0}") for x in granularity_levels
    ]

    key_dict = project_parser._get_feature_keys(
        data_model.project._get_dict(), data_model.cube_id, join_features
    )
    join_columns = []
    join_sql = ""
    join_index = 1
    categorical_string = ""
    # loop through the pairs of granularity levels in the new table and join features in the model to see if we need to pull in key columns
    for level, base_name in zip(granularity_levels, join_features):
        # if there is only one key and it matches the value then the column is coming from the base query and can be added to the join_columns as is
        if (
            len(key_dict[base_name]["key_cols"]) == 1
            and key_dict[base_name]["key_cols"][0] == key_dict[base_name]["value_col"]
        ):
            categorical_string = (
                categorical_string + f", {quote}base_query{quote}.{quote}{level}{quote}"
            )
            join_columns.append([level])
        else:
            # if there is a mismatch we get the sql for a join query and join on the value column
            key_sql, needed_cols = db_utils._get_key_col_sql(key_dict[base_name], db_conn)
            join_sql = (
                join_sql
                + f" LEFT JOIN ({key_sql}) AS {quote}join_{join_index}{quote} ON {quote}base_query{quote}.{quote}{level}{quote} = {quote}join_{join_index}{quote}.{quote}{key_dict[base_name]['value_col']}{quote}"
            )
            # add all the key columns to the outer select and the join_columns
            for col in key_dict[base_name]["key_cols"]:
                categorical_string = (
                    categorical_string + f", {quote}join_{join_index}{quote}.{quote}{col}{quote}"
                )
            join_columns.append(key_dict[base_name]["key_cols"])
            join_index = join_index + 1

    qds_query = f"SELECT {numeric}{categorical_string} FROM ({feature_query}{join_sql})"
    dataset_name = f"{new_feature_name}_QDS"

    columns = data_model.project._atconn._get_query_columns(
        warehouse_id=warehouse_id, query=qds_query
    )
    project_dataset, dataset_id = project_utils._create_query_dataset(
        project_dict=project_dict,
        name=dataset_name,
        query=qds_query,
        columns=columns,
        warehouse_id=warehouse_id,
        allow_aggregates=True,
    )
    model_utils._create_dataset_relationship_from_dataset(
        project_dict=project_dict,
        cube_id=data_model.cube_id,
        dataset_name=dataset_name,
        join_features=join_features,
        join_columns=join_columns,
        roleplay_features=roleplay_features,
    )

    feature_utils._create_aggregate_feature(
        project_dict=project_dict,
        cube_id=data_model.cube_id,
        dataset_id=dataset_id,
        column_name=new_feature_name,
        new_feature_name=new_feature_name,
        aggregation_type=enums.Aggs.SUM,
    )
    data_model.project._update_project(project_dict=project_dict, publish=True)


def _snowpark_udf_call(
    udf_name: str,
    feature_inputs: List[str],
):
    inputs = ", ".join(f'"{f}"' for f in feature_inputs)
    return f"{udf_name}(array_construct({inputs}))"
