from utils import create_shortname

def test_create_shortname():
    assert create_shortname("arts") == "arts"
    assert create_shortname("uw   arts") == "arts"
    assert create_shortname("uw arts club") == "arts-club"
    assert create_shortname("uw arts crafts club") == "arts-crafts-club"
    assert create_shortname("Waterloo Class of '25") == "class-of-25"
    assert create_shortname("UW Human Vs. Zombies") == "human-vs-zombies"
    assert create_shortname("Physclub") == "physclub"
    assert create_shortname("OSU!Uwaterloo") == "osu"
    assert create_shortname("UW/WLU DD '25") == "dd-25"
    assert create_shortname("uwclubs") == "uwclubs"
    assert create_shortname("uw clubs") == "clubs"