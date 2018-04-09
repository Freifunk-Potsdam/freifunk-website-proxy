
def test_save_and_load(db):
    """Save something and load it."""
    db.save(123)
    assert db.load() == 123


def test_can_not_load_anything(db):
    assert db.load() is None


def test_loading_creates_copies(db):
    l = []
    db.save(l)
    assert db.load() is not l


def test_saving_again_uses_new_object(db):
    db.save(1)
    db.save(2)
    assert db.load() == 2


def test_creating_a_database_with_same_file_loads_same_contents(db):
    from freifunk_website_proxy.database import Database
    db2 = Database(db.file)
    db.save(1234)
    assert db2.load() == 1234
    

def test_can_save_functions(db):
    db.save(test_can_save_functions)
    assert db.load() == test_can_save_functions


def test_can_not_load_from_different_version(db):
    db.save(123)
    db.version += 1
    assert db.load() is None

