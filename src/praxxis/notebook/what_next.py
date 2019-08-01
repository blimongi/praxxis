"""
Rule-engine and model-based predictions based on user history.
"""
import requests
import json
import time
from requests.auth import HTTPBasicAuth

from src.praxxis.sqlite import sqlite_scene
from src.praxxis.rulesengine import rules_checker


def what_next(args, user_info_db, current_scene_db, library_db, rulesengine_db, model_db, start, end):
    """calls prediction endpoints to get next notebooks"""
    from src.praxxis.display import display_rulesengine
    history = sqlite_scene.get_recent_history(current_scene_db, 5)
    if history == []:
        from src.praxxis.util.error import EmptyHistoryError
        raise EmptyHistoryError()

    rules_based = rules_checker.rules_check(rulesengine_db, history[-1][0], history[-1][1], start, end)
    if rules_based != []:
        display_rulesengine.display_predictions(rules_based)
        write_to_list(rules_based, current_scene_db, library_db)
        return rules_based
    else:
        model_based_prediction(history, model_db)

def model_based_prediction(history, model_db):
    import sys
    import warnings

    if sys.version_info.major == 3 and sys.version_info.minor > 6:
        from src.praxxis.display import display_error
        display_error.tensorflow_version_error()
        sys.exit(1)

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FutureWarning)
        from src.praxxis.model import score
        predictions = score.get_predictions(history, model_db)

    predictions = [(prediction, 0) for prediction in predictions]
    from src.praxxis.display import display_model
    from src.praxxis.display import display_rulesengine
    display_model.display_beta_warning()
    display_rulesengine.display_predictions(predictions)
    

def write_to_list(notebook_library_list, current_scene_db, library_db):
    """grabs paths and writes to notebook list so ordinal referencing works"""
    from src.praxxis.sqlite import sqlite_notebook

    notebooklist = []
    for notebook in notebook_library_list:
        path = sqlite_notebook.get_notebook_path(library_db, notebook[0], notebook[1])
        notebook = (notebook[0], path, notebook[1], None)
        notebooklist.append(notebook)

    sqlite_notebook.write_list(current_scene_db, notebooklist)
    