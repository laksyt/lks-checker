from datetime import datetime

from aiohttp import web

from laksyt.entities.report import HealthReport, compose_failure_report, compose_success_report, compose_timeout_report
from laksyt.entities.target import Target


class TestReport:

    def test_compose_success_report(self):
        # Given
        response = web.Response(text='Hello, world', status=200)
        response.time = 0.1

        # When
        report = compose_success_report(Target('url', None), response, None)

        # Then
        assert report is not None
        assert report.target.url == 'url'
        assert report.target.needle is None
        assert report.is_available is True
        assert report.status == 'SUCCESS'
        assert report.status_code == 200
        assert report.response_time == 0.1
        assert report.needle_found is None
        assert isinstance(report.checked_at, datetime)

    def test_compose_failure_report(self):
        # Given
        error = web.HTTPError()
        error.time = 0.2

        # When
        report = compose_failure_report(Target('url', 'needle'), error)

        # Then
        assert report is not None
        assert report.target.url == 'url'
        assert report.target.needle == 'needle'
        assert report.is_available is False
        assert report.status == 'UNAVAILABLE'
        assert report.status_code is None
        assert report.response_time == 0.2
        assert report.needle_found is None
        assert isinstance(report.checked_at, datetime)

    def test_compose_timeout_report(self):
        # When
        report = compose_timeout_report(Target('url', 'needle'), 3)

        # Then
        assert report is not None
        assert report.target.url == 'url'
        assert report.target.needle == 'needle'
        assert report.is_available is False
        assert report.status == 'TIMEOUT'
        assert report.status_code is None
        assert report.response_time == 3
        assert report.needle_found is None
        assert isinstance(report.checked_at, datetime)

    def test_report_serialization_deserialization(self):
        # Given
        response = web.Response(text='Hello, world', status=204)
        response.time = 0.1
        original = compose_success_report(Target('url', 'x'), response, True)

        # When
        bytestr = original.serialize()
        reconstructed = HealthReport.deserialize(bytestr)

        # Then
        assert reconstructed is not None
        assert reconstructed.target.url == 'url'
        assert reconstructed.target.needle == 'x'
        assert reconstructed.is_available is True
        assert reconstructed.status == 'SUCCESS'
        assert reconstructed.status_code == 204
        assert reconstructed.response_time == 0.1
        assert reconstructed.needle_found is True
        assert reconstructed.checked_at == original.checked_at
