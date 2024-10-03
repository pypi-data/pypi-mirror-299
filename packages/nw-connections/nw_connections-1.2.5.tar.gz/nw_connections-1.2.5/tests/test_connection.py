# encoding: utf-8
import pytest
import json
from copy import deepcopy
import requests_cache
from six import string_types
from nw_connections.connection import (LocalConnection, DatabaseSchemaConnection,
    DatabaseConnection, DatabaseRecipeConnection,
    DatabasePipelineConnection, AWSConnection, ConnectionError,
    PostgrestTabDataConnection)

from tests.data.config import (POSTGREST_URL, POSTGREST_JWT_TOKEN, POSTGREST_ROLE,
    AWS_ACCESS_ID, AWS_ACCESS_KEY, TAB_DATA_DB_ROLE,TAB_DATA_JWT_TOKEN,
    TAB_DATA_URL)



def test_get_with_local_connection():
    """ Should open all files in data/connection and verify count
    """
    connection = LocalConnection("tests/data/connection")
    files = [x for x in connection.get()]
    expected_number_of_files_in_folder = 2
    assert len(files) == expected_number_of_files_in_folder

def test_get_by_id_with_local_connection():
    """ Open file1.json and verify that content is correct
    """
    connection = LocalConnection("tests/data/connection")
    file_content = connection.get_by_id("file1")
    assert file_content == { "id": "file1" }


def test_missing_file_should_not_exist():
    connection = LocalConnection("tests/data/connection")
    assert connection.exists(id="missing_file") == False

def test_get_files_with_invalid_query():
    connection = LocalConnection("tests/data/connection")

    with pytest.raises(ValueError):
        connection.get(missing_key="foo")


def test_list_schemas_from_api():
    """ Make sure that listing schemas from database works
    """
    connection = DatabaseSchemaConnection(POSTGREST_URL)
    schemas = connection.get()
    assert len(schemas) > 0
    assert isinstance(schemas[0], string_types)

def test_list_recipes_from_api():
    """ Try to get every recipe one by one
        This mote of a test for the api
    """
    connection = DatabaseRecipeConnection(POSTGREST_URL)
    recipes = connection.get()
    assert len(recipes) > 0
    assert isinstance(recipes[0], string_types)

def test_get_recipe_from_api():
    """
    """
    connection = DatabaseRecipeConnection(POSTGREST_URL)
    # This test depends on the name of the production recipe
    # not changing, not optimal.
    recipe = connection.get(id="ams-unemployment-monthly.json")

    # Should work without .json also
    recipe = connection.get(id="ams-unemployment-monthly")

def test_get_schema_from_api():
    """ Make sure that listing schemas from database works
    """
    connection = DatabaseSchemaConnection(POSTGREST_URL)
    resp = connection.get_by_id("marple-dataset.json")
    assert resp['$schema'] == 'http://json-schema.org/draft-04/schema#'
    assert isinstance(resp,dict)

def _test_get_recipes_from_api():
    """ Make sure that listing schemas from database works
    """
    connection = DatabaseRecipeConnection(POSTGREST_URL)
    recipes = connection.get()
    for recipe_id in recipes:
        recipe = connection.get_by_id(recipe_id)
        # TODO: Assert that the recipe actully matches json schema
        assert len(recipe.keys()) > 0

def test_get_recipe_with_unicode_id_and_no_json():
    connection = DatabaseRecipeConnection(POSTGREST_URL)
    recipe = connection.get_by_id(u"brå-reported_crime_by_crime_type-monthly")
    assert len(recipe.keys()) > 0


def _test_get_pipeline_by_id_from_api():
    connection = DatabasePipelineConnection(POSTGREST_URL)
    pipelines = connection.get()
    for pipeline_id in pipelines:
        pipeline = connection.get_by_id(pipeline_id)
        assert pipeline["id"] == pipeline_id.replace(".json","")

def test_get_recipe_with_cache():
    """ Get a recipe twice and make sure it comes from cache second time
    """
    connection = DatabaseRecipeConnection(POSTGREST_URL)
    recipe = connection.get()[0]

    connection.get_by_id(recipe, cache=True)
    assert connection.response.from_cache == False

    connection.get_by_id(recipe, cache=True)
    assert connection.response.from_cache == True



# ==========================
#    ALARM TESTS
# ==========================
@pytest.fixture(scope="session")
def database_alarm_connection():
    return DatabaseConnection(POSTGREST_URL, "alarm_test",
        jwt_token=POSTGREST_JWT_TOKEN, db_role=POSTGREST_ROLE)

@pytest.fixture(scope="session")
def get_example_alarm(database_alarm_connection):
    """Get a local example alarm
    """
    with open("tests/data/connection/alarm/example_alarm.json") as f:
        alarm = json.load(f)
    return alarm


def test_add_alarm_on_database_connection(database_alarm_connection,
                                          get_example_alarm):
    """Trying adding an alarm to database
    """
    connection, alarm = database_alarm_connection, get_example_alarm
    r = connection.store(alarm["id"], alarm)
    assert r.status_code in [201, 204]


def test_alarm_connection_on_database_without_auth():
    """ Make a basic request without auth
    """
    connection = DatabaseConnection(POSTGREST_URL, "alarm_test",
                                    jwt_token=POSTGREST_JWT_TOKEN,
                                    db_role=POSTGREST_ROLE)
    # Sample query
    assert connection.exists(id="foo") == False

def test_query_alarms_with_list_on_database_connection():
    """ Make a query with a list of regions
        This test depends on the old db entries not changing
    """
    connection = DatabaseConnection(POSTGREST_URL, "alarm",
                                    jwt_token=POSTGREST_JWT_TOKEN,
                                    db_role=POSTGREST_ROLE)
    alarms = connection.get(source="AMS", trigger_date="2016-10-01",
        region=[u"Älmhults kommun", u"Åmåls kommun"])
    assert len(alarms) == 7

def test_delete_alarm(database_alarm_connection, get_example_alarm):
    connection, alarm = database_alarm_connection, get_example_alarm
    r = connection.store(alarm["id"], alarm)
    if r.status_code in [201, 204]:
        r = connection.delete(alarm["id"])
        assert r.status_code == 204
    else:
        assert False, "Error setting up test"

def test_get_alarm_object_with_cache(database_alarm_connection, get_example_alarm):
    """ Get an alarm with caching enabled
    """
    connection, alarm = database_alarm_connection, get_example_alarm

    # Set up test by adding example alarm
    r = connection.store(alarm["id"], alarm)
    assert r.status_code in [201, 204], "Error setting up test"

    alarms = connection.get(id=alarm["id"], cache=True)
    r1 = connection.response
    assert r1.from_cache == False

    alarms = connection.get(id=alarm["id"], cache=True)
    r2 = connection.response
    assert r2.from_cache == True


# ==========================
#    NEWSLEAD TESTS
# ==========================
@pytest.fixture(scope="session")
def database_newslead_connection():
    conn =  DatabaseConnection(POSTGREST_URL, "newslead_test",
        jwt_token=POSTGREST_JWT_TOKEN, db_role=POSTGREST_ROLE)
    return conn

def test_add_newslead_on_database_connection(database_newslead_connection):
    """ Trying adding an alarm to database
    """
    connection = database_newslead_connection
    with open("tests/data/connection/newslead/example_newslead.json") as f:
        newslead = json.load(f)
    r = connection.store(newslead["id"], newslead)
    assert r.status_code in [201, 204]


# ==========================
#    REPORT TESTS
# ==========================
@pytest.fixture(scope="session")
def database_report_connection():
    conn =  DatabaseConnection(POSTGREST_URL, "report_test",
        jwt_token=POSTGREST_JWT_TOKEN, db_role=POSTGREST_ROLE)
    return conn


def test_add_report_on_database_connection(database_report_connection):
    """ Trying adding a report object to database
    """
    connection = database_report_connection
    with open("tests/data/connection/report/example_report.json") as f:
        report = json.load(f)
    assert isinstance(report, dict)
    r = connection.store(report["id"], report)
    assert r.status_code in [201, 204]
    stored_report = connection.get(report["id"])[0]
    assert isinstance(stored_report, dict)

# ==========================
#    TAB DATA CONNECTION TESTS
# ==========================

@pytest.fixture(scope="session")
def postgrest_tab_data_connection():
    conn = PostgrestTabDataConnection(TAB_DATA_URL, "test_table",
                                      jwt_token=TAB_DATA_JWT_TOKEN,
                                      db_role=TAB_DATA_DB_ROLE)

    # empty test table
    conn.delete()
    return conn

def test_tab_data_connection_postgrest(postgrest_tab_data_connection):
    conn = postgrest_tab_data_connection

    n_rows = len(conn.get())
    assert(n_rows == 0)

    r = conn.insert({
        "col_a": "john",
        "col_b": 123,
    })
    n_rows = len(conn.get())
    assert(n_rows == 1)

    # add some new data
    conn.upsert(
        [
        {
            "col_a": "john",
            "col_b": 234,
        },
        {
            "col_a": "mike",
            "col_b": 345,

        }
        ])
    n_rows = len(conn.get())
    assert(n_rows == 2)

    john_row = conn.get({"col_a": "john"})[0]
    assert(john_row["col_b"] == 234)

    # and delete john
    r = conn.delete({"col_a": "john"})
    n_rows = len(conn.get())
    assert(n_rows == 1)


# ============================
#   S3 TESTS
# ============================
@pytest.fixture(scope="session")
def get_s3_connection():
    """ Connects to the test bucket
    """
    return AWSConnection("newsworthy",
                         folder="nw_connection_tests",
                         aws_access_key_id=AWS_ACCESS_ID,
                         aws_secret_access_key=AWS_ACCESS_KEY)


def test_store_text_file_to_s3(get_s3_connection):
    """ Store a simple text file
    """
    connection = get_s3_connection
    resp = connection.store(u"test_text_file_åäö.txt", u"Hej världen")
    assert resp["ResponseMetadata"]["HTTPStatusCode"] == 200

def test_store_image_file_to_s3(get_s3_connection):
    """ Store a simple text file
    """
    connection = get_s3_connection
    with open("tests/data/connection/sample_chart.png") as f:
        connection.store(u"sample_chart.png", f)

def test_get_json_file_from_s3(get_s3_connection):
    connection = get_s3_connection

    with open("tests/data/connection/file1.json") as f:
        json_data = json.load(f)
        connection.store(u"file1", json_data)

    json_data = connection.get_by_id("file1")
    assert json_data["id"] == "file1"
