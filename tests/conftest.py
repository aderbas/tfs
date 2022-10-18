# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

import httpretty
import pytest

from tfs import TFSAPI


def request_callback_get(request, uri, headers):
    # Map path from url to a file
    path = urlparse(uri).path.split("DefaultCollection/")[1]
    response_file = os.path.normpath("tests/resources/{}".format(path))
    response_file = os.path.join(response_file, "response.json")

    if os.path.exists(response_file):
        code = 200
        response = open(response_file, mode="r", encoding="utf-8-sig").read()
    else:
        code = 404
        response = "Cannot find file {}".format(response_file)

    return code, headers, response


@pytest.fixture(autouse=True)
def tfs_server_mock():
    for method in (httpretty.GET, httpretty.POST, httpretty.PUT, httpretty.PATCH):
        httpretty.register_uri(
            method,
            re.compile(r"http://.*/DefaultCollection/.*"),
            body=request_callback_get,
            content_type="application/json",
        )


@pytest.fixture()
def tfsapi():
    client = TFSAPI(
        "http://tfs.tfs.ru/tfs", "DefaultCollection/MyProject", "username", "password"
    )
    yield client
