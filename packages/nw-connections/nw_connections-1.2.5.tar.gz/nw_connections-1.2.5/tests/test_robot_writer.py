"""The robot writer module.

These tests depend on an external robotwriter to be availble.
"""
import pytest
from nw_connections.robotwriter import RobotWriter, RobotWriterError
from tests.data.config import ROBOT_WRITER_SECRET, ROBOT_WRITER_URL



def setup_writer():
    return RobotWriter(url=ROBOT_WRITER_URL,
                       secret=ROBOT_WRITER_SECRET)

def test_render_string():
    rw = setup_writer()
    template = "p Hello #{t(region, {'conjugation':'short'})}!"
    context = {"region": "Solna kommun"}

    # render without translation
    html = rw.render_string(template, context,translations=[])
    assert (html == "<p>Hello Solna kommun!</p>")

    # render with translation
    html = rw.render_string(template, context,translations=["regions"])
    assert (html == "<p>Hello Solna!</p>")


def test_render_by_name():
    rw = setup_writer()
    context = {"region": "Solna kommun"}
    html = rw.render_by_name("test_basic", context, lang="sv")
    assert (html == "<p>Hello Solna!</p>")

def test_bad_requests():
    rw = setup_writer()

    # call non-existing template
    with pytest.raises(RobotWriterError):
        rw.render_by_name("non_existing_template", {})
