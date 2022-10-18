# -*- coding: utf-8 -*-
import json

import pytest

from tfs.resources import *


class TestWorkitem(object):
    @pytest.fixture()
    def workitem_with_child_only(self, tfsapi):
        data_str = r"""{
            "id": 100,
            "rev": 1,
            "fields": {
                "System.AreaPath": "Test Agile",
                "System.TeamProject": "Test Agile",
                "System.IterationPath": "Test Agile\\Current\\Iteration 1",
                "System.WorkItemType": "Bug",
                "System.State": "Active",
                "System.Reason": "New",
                "System.CreatedDate": "2015-10-14T07:40:46.96Z",
                "System.CreatedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "System.ChangedDate": "2015-10-14T07:40:46.96Z",
                "System.ChangedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "System.Title": "MyTitle",
                "Microsoft.VSTS.Common.StateChangeDate": "2015-10-14T07:40:46.96Z",
                "Microsoft.VSTS.Common.ActivatedDate": "2015-10-14T07:40:46.96Z",
                "Microsoft.VSTS.Common.ActivatedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "Microsoft.VSTS.Common.Priority": 2,
                "Microsoft.VSTS.Common.Severity": "3 - Medium"
            },
            "relations": [
                {
                  "rel": "System.LinkTypes.Hierarchy-Forward",
                  "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/10",
                  "attributes": {
                    "isLocked": false
                  }
                },
                {
                  "rel": "System.LinkTypes.Hierarchy-Forward",
                  "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/11",
                  "attributes": {
                    "isLocked": false
                  }
                }
              ],
            "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/100"
        }"""
        data_ = json.loads(data_str)
        wi = Workitem(tfsapi, data_)
        yield wi

    @pytest.fixture()
    def workitem(self, tfsapi):
        data_str = r"""{
            "id": 100,
            "rev": 1,
            "fields": {
                "System.AreaPath": "Test Agile",
                "System.TeamProject": "Test Agile",
                "System.IterationPath": "Test Agile\\Current\\Iteration 1",
                "System.WorkItemType": "Bug",
                "System.State": "Active",
                "System.Reason": "New",
                "System.CreatedDate": "2015-10-14T07:40:46.96Z",
                "System.CreatedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "System.ChangedDate": "2015-10-14T07:40:46.96Z",
                "System.ChangedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "System.Title": "MyTitle",
                "System.Russia": "Русский язык",
                "Microsoft.VSTS.Common.StateChangeDate": "2015-10-14T07:40:46.96Z",
                "Microsoft.VSTS.Common.ActivatedDate": "2015-10-14T07:40:46.96Z",
                "Microsoft.VSTS.Common.ActivatedBy": "Alexey Ivanov <DOMAIN\\AIvanov>",
                "Microsoft.VSTS.Common.Priority": 2,
                "Microsoft.VSTS.Common.Severity": "3 - Medium",
                "Custom.Bug.Type": "Manual Test Case"
            },
            "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/100",
            "relations": [
            {
              "rel": "System.LinkTypes.Hierarchy-Reverse",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/110",
              "attributes": {
                "isLocked": false
              }
            },
            {
            "attributes": {
                "authorizedDate": "2018-01-06T05:43:42.75Z",
                "id": 47,
                "name": ".gitignore",
                "resourceCreatedDate": "2018-01-06T05:43:41.63Z",
                "resourceModifiedDate": "2018-01-06T05:43:41.63Z",
                "resourceSize": 1276,
                "revisedDate": "9999-01-01T00:00:00Z"
            },
            "rel": "AttachedFile",
            "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/attachments\/5766cbba-2794-468c-801b-3ede5e3267a0"
            }
            ],
            "_links": {
              "self": {
                "href": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/100"
              },
              "workItemUpdates": {
                "href": "http://tfs.tfs.ru/tfs/DefaultCollection/_apis/wit/workItems/309/updates"
              },
              "workItemRevisions": {
                "href": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workitems\/100\/revisions"
              },
              "workItemHistory": {
                "href": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/100\/history"
              },
              "html": {
                "href": "http:\/\/tfs.tfs.ru\/tfs\/web\/wi.aspx?pcguid=9cd4a217-5ab5-4e09-8116-ec8a6141e5a5&id=100"
              },
              "workItemType": {
                "href": "http://tfs.tfs.ru/tfs/DefaultCollection/6ce954b1-ce1f-45d1-b94d-e6bf2464ba2c/_apis/wit/workItemTypes/Product%20Backlog%20Item"
              },
              "fields": {
                "href": "http://tfs.tfs.ru/tfs/DefaultCollection/_apis/wit/fields"
              }
            }
        }"""
        data_ = json.loads(data_str)
        wi = Workitem(tfsapi, data_)
        yield wi

    def test_workitem_id(self, workitem):
        assert workitem.id == 100

    def test_workitem_fields(self, workitem):
        assert workitem["Reason"] == "New"
        assert workitem["AreaPath"] == "Test Agile"
        assert workitem["Tags"] is None

    def test_workitem_fields_with_prefix(self, workitem):
        assert workitem["System.Reason"] == "New"
        assert workitem["System.AreaPath"] == "Test Agile"
        assert workitem["System.Tags"] is None

    def test_workitem_fields_custom(self, workitem):
        assert workitem["Custom.Bug.Type"] == "Manual Test Case"

    @pytest.mark.httpretty
    def test_workitem_field_update(self, workitem):
        workitem["Reason"] = "Canceled"
        assert workitem["Reason"] == "Canceled"

    def test_workitem_fields_case_ins(self, workitem):
        assert workitem["ReaSon"] == "New"
        assert workitem["AREAPath"] == "Test Agile"

    def test_workitem_parent_id(self, workitem):
        assert workitem.parent_id == 110

    def test_workitem_parent_with_child_only(self, workitem_with_child_only):
        assert workitem_with_child_only.parent_id is None
        assert workitem_with_child_only.child_ids == [10, 11]

    def test_workitem_field_russia(self, workitem):
        assert workitem["russia"] == "Русский язык"

    def test_workitem_field_names(self, workitem):
        assert "Russia" in workitem.field_names
        assert "Title" in workitem.field_names

    def test_find_in_relation(self, workitem):
        assert (
            len(workitem.find_in_relation("Hierarchy-Reverse")) == 1
        ), "Can not find in relation some link"

    def test_attachment(self, workitem):
        assert len(workitem.attachments) == 1
        attach = workitem.attachments[0]
        assert isinstance(attach, Attachment)
        assert attach.name == ".gitignore"

    def test_dir_links(self, workitem):
        properties_must_be = [
            "workItemHistory",
            "workItemRevisions",
            "workItemType",
            "workItemUpdates",
        ]
        properties = dir(workitem)
        for property_name in properties_must_be:
            assert (
                property_name in properties
            ), "Workitem object must has attribute '{}'".format(property_name)

    # Started failing without related changes at
    # https://travis-ci.org/devopshq/tfs/builds/378607508?utm_source=github_status&utm_medium=notification
    # @pytest.mark.httpretty
    # def test_wi_revisions(self, workitem):
    #     revisions = workitem.workItemRevisions
    #     assert isinstance(revisions[0], TFSObject)
    #
    #     revisions = workitem.revisions
    #     assert isinstance(revisions[0], TFSObject)

    def test_wi_raise_attribute_error(self, workitem):
        with pytest.raises(AttributeError):
            _ = workitem.not_exist_attribute


class TestChangeset(object):
    @pytest.fixture()
    def changeset(self, tfsapi):
        data_str = """{
          "changesetId": 16,
          "url": "http://tfs.tfs.ru/DefaultCollection/_apis/tfvc/changesets/16",
          "author": {
            "id": "8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d",
            "displayName": "Chuck Reinhart",
            "uniqueName": "fabrikamfiber3@hotmail.com",
            "url": "http://tfs.tfs.ru/DefaultCollection/_apis/Identities/8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d",
            "imageUrl": "http://tfs.tfs.ru/DefaultCollection/_api/_common/identityImage?id=8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d"
          },
          "checkedInBy": {
            "id": "8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d",
            "displayName": "Chuck Reinhart",
            "uniqueName": "fabrikamfiber3@hotmail.com",
            "url": "http://tfs.tfs.ru/DefaultCollection/_apis/Identities/8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d",
            "imageUrl": "http://tfs.tfs.ru/DefaultCollection/_api/_common/identityImage?id=8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d"
          },
          "createdDate": "2014-03-24T20:21:02.727Z",
          "comment": "My Comment",
          "_links": {
            "self": {
              "href": "http://tfs.tfs.ru/DefaultCollection/_apis/tfvc/changesets/16"
            },
            "changes": {
              "href": "http://tfs.tfs.ru/DefaultCollection/_apis/tfvc/changesets/16/changes"
            },
            "workItems": {
              "href": "http://tfs.tfs.ru/DefaultCollection/_apis/tfvc/changesets/16/workItems"
            },
            "author": {
              "href": "http://tfs.tfs.ru/DefaultCollection/_apis/Identities/8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d"
            },
            "checkedInBy": {
              "href": "http://tfs.tfs.ru/DefaultCollection/_apis/Identities/8c8c7d32-6b1b-47f4-b2e9-30b477b5ab3d"
            }
          }
        }"""
        data_ = json.loads(data_str)
        cs = Changeset(tfsapi, data_)
        yield cs

    def test_changeset_fields(self, changeset):
        assert changeset.id == 16
        assert changeset.comment == "My Comment"
        assert isinstance(changeset.author, Identity)
        assert changeset.author.displayName == "Chuck Reinhart"

    def test_changeset_fields_get(self, changeset):
        assert changeset.get("comment") == "My Comment"

    @pytest.mark.httpretty
    def test_get_changesets_workitem(self, tfsapi):
        changesets = tfsapi.get_changesets(from_=10, to_=14)
        changeset = changesets[0]
        workitems = changeset.workitems

        assert len(workitems) == 2
        assert workitems[0].id == 100
        assert workitems[1].id == 101


class TestTFSQuery:
    @pytest.fixture()
    def tfsquery(self, tfsapi):
        data_str = r"""
        {
          "id": "cbbcdcaa-377f-42f7-a544-4d9507f2aa22",
          "name": "Shared Queries",
          "path": "Shared Queries",
          "createdDate": "2013-12-17T10:38:02.147Z",
          "lastModifiedBy": {
            "id": "190c53ac-8f14-4c4c-b4ba-d91a9b30da02",
            "displayName": "Andrey Ivanov <DOMAIN\\AIvanov>"
          },
          "lastModifiedDate": "2013-12-17T10:38:02.58Z",
          "isFolder": true,
          "hasChildren": true,
          "isPublic": true,
          "_links": {
            "self": {
              "href": "http://tfs.tfs.ru/tfs/DefaultCollection/9d639e22-e9a9-49d7-8b40-ef94d9607bdb/_apis/wit/queries/cbbcdcaa-377f-42f7-a544-4d9507f2aa22"
            },
            "html": {
              "href": "http://tfs.tfs.ru/tfs/web/qr.aspx?pguid=9d639e22-e9a9-49d7-8b40-ef94d9607bdb&qid=cbbcdcaa-377f-42f7-a544-4d9507f2aa22"
            }
          },
          "url": "http://tfs.tfs.ru/tfs/DefaultCollection/9d639e22-e9a9-49d7-8b40-ef94d9607bdb/_apis/wit/queries/cbbcdcaa-377f-42f7-a544-4d9507f2aa22"
        }
        """
        data_ = json.loads(data_str)
        cs = TFSQuery(tfsapi, data_)
        yield cs

    @pytest.mark.httpretty
    def test_tfsquery(self, tfsquery):
        assert tfsquery.id == "cbbcdcaa-377f-42f7-a544-4d9507f2aa22"

    @pytest.mark.httpretty
    def test_tfsquery_columns(self, tfsquery):
        assert "System.Title" in tfsquery.columns

    @pytest.mark.httpretty
    def test_tfsquery_column_names(self, tfsquery):
        assert "Title" in tfsquery.column_names

    @pytest.mark.httpretty
    def test_tfsquery_ids(self, tfsquery):
        assert len(tfsquery.workitems) == 2
        assert tfsquery.workitems[0].id == 100
        assert tfsquery.workitems[1].id == 101


class TestWiql(object):
    @pytest.fixture()
    def wiql(self, tfsapi):
        data_str = r"""{
          "queryResultType": "workItem",
          "columns": [
            {
              "name": "ID",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/System.Id",
              "referenceName": "System.Id"
            },
            {
              "name": "Severity",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/Microsoft.VSTS.Common.Severity",
              "referenceName": "Microsoft.VSTS.Common.Severity"
            },
            {
              "name": "Target Version",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/TargetVersion",
              "referenceName": "TargetVersion"
            }
          ],
          "sortColumns": [
            {
              "field": {
                "name": "Target Version",
                "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/TargetVersion",
                "referenceName": "TargetVersion"
              },
              "descending": false
            },
            {
              "field": {
                "name": "Severity",
                "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/Microsoft.VSTS.Common.Severity",
                "referenceName": "Microsoft.VSTS.Common.Severity"
              },
              "descending": false
            }
          ],
          "workItems": [
            {
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/100",
              "id": 100
            },
            {
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/workItems\/101",
              "id": 101
            }
          ],
          "asOf": "2017-07-24T06:59:38.74Z",
          "queryType": "flat"
        }"""
        data_ = json.loads(data_str)
        wiql = Wiql(tfsapi, data_)
        yield wiql

    @pytest.fixture()
    def wiql_empty(self, tfsapi):
        data_str = r"""
        {
          "queryResultType": "workItem",
          "columns": [
            {
              "name": "ID",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/System.Id",
              "referenceName": "System.Id"
            },
            {
              "name": "Severity",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/Microsoft.VSTS.Common.Severity",
              "referenceName": "Microsoft.VSTS.Common.Severity"
            },
            {
              "name": "Target Version",
              "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/TargetVersion",
              "referenceName": "TargetVersion"
            }
          ],
          "sortColumns": [
            {
              "field": {
                "name": "Target Version",
                "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/TargetVersion",
                "referenceName": "TargetVersion"
              },
              "descending": false
            },
            {
              "field": {
                "name": "Severity",
                "url": "http:\/\/tfs.tfs.ru\/tfs\/DefaultCollection\/_apis\/wit\/fields\/Microsoft.VSTS.Common.Severity",
                "referenceName": "Microsoft.VSTS.Common.Severity"
              },
              "descending": false
            }
          ],
          "workItems": [
          ],
          "asOf": "2017-07-24T06:59:38.74Z",
          "queryType": "flat"
        }"""
        data_ = json.loads(data_str)
        wiql = Wiql(tfsapi, data_)
        yield wiql

    def test_wiql(self, wiql):
        with pytest.raises(AttributeError):
            wiql.id = wiql.id
        assert wiql.queryResultType == "workItem"

    def test_get_wiql_workitem_ids(self, wiql):
        assert wiql.workitem_ids == [100, 101]

    @pytest.mark.httpretty
    def test_get_wiql_workitems(self, wiql):
        workitems = wiql.workitems

        assert len(workitems) == 2
        assert workitems[0].id == 100
        assert workitems[1].id == 101

    def test_wiql_empty(self, wiql_empty):
        assert wiql_empty.workitem_ids == []

    def test_wiql_result(self, wiql):
        assert wiql._data == wiql.result


class TestUtilities(object):
    def test_class_for_resource_is_case_insensitive(self):
        obj = class_for_resource("bUiLd/DeFiNiTiOnS/123")

        assert obj is Definition
