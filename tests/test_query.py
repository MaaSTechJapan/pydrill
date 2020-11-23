#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pydrill.exceptions import QueryError, ImproperlyConfigured


def test_select_employee(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
    expected_result = {'columns': ["employee_id", "full_name", "first_name", "last_name", "position_id", "position_title", "store_id", "department_id", "birth_date", "hire_date", "salary", "supervisor_id", "education_level", "marital_status", "gender", "management_role"],
                       'rows': [{
                           "store_id": "0",
                           "gender": "F",
                           "department_id": "1",
                           "birth_date": "1961-08-26",
                           "supervisor_id": "0",
                           "last_name": "Nowmer",
                           "position_title": "President",
                           "hire_date": "1994-12-01 00:00:00.0",
                           "management_role": "Senior Management",
                           "salary": "80000.0",
                           "marital_status": "S",
                           "full_name": "Sheri Nowmer",
                           "employee_id": "1",
                           "education_level": "Graduate Degree",
                           "first_name": "Sheri",
                           "position_id": "1"
                           }],
                       'metadata': ["BIGINT", "VARCHAR", "VARCHAR", "VARCHAR", "BIGINT", "VARCHAR", "BIGINT", "BIGINT", "VARCHAR", "VARCHAR", "FLOAT8", "BIGINT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"]
                       }

    result = pydrill_instance.query(sql=sql)

    assert result.response.status_code == 200
    assert result.data['columns'] == expected_result['columns']
    assert result.data['rows'] == expected_result['rows']
    assert result.data['metadata'] == expected_result['metadata']


def test_select_iterator(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"

    for row in pydrill_instance.query(sql=sql):
        assert type(row) is dict


def test_select_parquet(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM `dfs.root`.`/CommonStore/nodes/stations.parquet` LIMIT 1"
    result = pydrill_instance.query(sql=sql)
    df = result.to_dataframe()
    assert type(df['geometry'][0]) is dict

def test_select_pandas(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"

    with pytest.raises(ImproperlyConfigured):
        df = pydrill_instance.query(sql=sql).to_dataframe()


def test_select_without_sql(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = ""
    try:
        result = pydrill_instance.query(sql=sql)
    except QueryError as e:
        assert e


def test_plan_for_select_employee(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
    result = pydrill_instance.plan(sql=sql)
    assert result.response.status_code == 200


# TODO: create more tests with other queries.
