import pytest


def test_navigate_to_receiving_form(client_two):
    # arrange

    # act
    result = client_two.get('/receiving', follow_redirects=True)

    # assert
    assert b'Receiving' in result.data
