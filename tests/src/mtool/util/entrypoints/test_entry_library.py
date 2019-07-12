from src.mtool.util.entrypoints import entry_library

def test_init_library(setup, library_root, library_db):
    import shutil 
    import os 
    
    assert os.path.exists(library_root)
    assert os.path.exists(library_db)
    shutil.rmtree(library_root)
    assert not os.path.exists(library_root)
    
    entry_library.init_library(library_root, library_db)
    
    assert os.path.exists(library_root)
    assert os.path.exists(library_db)


def test_sync_library(setup, library_root, library_db):
    libraries = entry_library.sync_library("", library_root, library_db)
    assert libraries == 0


def test_list_library(setup, add_test_library, library_db):
    libraries = entry_library.list_library("", library_db)
    assert len(libraries) == 1


def test_add_library(setup, library_db): 
    from src.mtool.util import error
    from tests.src.mtool.util import dummy_object
    from src.mtool.library import remove_library
    from src.mtool.library import list_library

    dummy_library = dummy_object.make_dummy_library_path()
    entry_library.add_library(dummy_library, library_db)

    remove_library.remove_library(dummy_library, library_db)
