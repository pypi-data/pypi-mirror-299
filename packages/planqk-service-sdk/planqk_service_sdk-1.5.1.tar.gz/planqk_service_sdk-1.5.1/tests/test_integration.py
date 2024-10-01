import os
import unittest

from planqk.service.auth import PlanqkServiceAuth
from planqk.service.client import PlanqkServiceClient
from planqk.service.sdk import JobStatus
from planqk.service.sdk.client import PlanqkServiceApi

service_endpoint = os.getenv('SERVICE_ENDPOINT', "http://localhost:8081")
consumer_key = os.getenv('CONSUMER_KEY', None)
consumer_secret = os.getenv('CONSUMER_SECRET', None)


class IntegrationTestSuite(unittest.TestCase):

    def test_should_use_client(self):
        client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

        health = client.health_check()
        assert health.status == "Service is up and running"

        data = {
            "values": [
                1,
                5.2,
                20,
                7,
                9.4
            ]
        }
        params = {
            "round_off": True
        }

        job = client.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status == JobStatus.PENDING

        result = client.get_result(job.id)
        assert result is not None

        job = client.get_status(job.id)
        assert job.id is not None
        assert job.status == JobStatus.SUCCEEDED or job.status == JobStatus.FAILED

        print(job, result)

    def test_should_use_raw_client(self):
        if (consumer_key is not None) or (consumer_secret is not None):
            auth = PlanqkServiceAuth(consumer_key, consumer_secret)
            api = PlanqkServiceApi(token=auth.get_token, base_url=service_endpoint)
        else:
            api = PlanqkServiceApi(token="random_token", base_url=service_endpoint)

        health = api.status_api.health_check()
        assert health.status == "Service is up and running"

        data = {
            "values": [
                1,
                5.2,
                20,
                7,
                9.4
            ]
        }
        params = {
            "round_off": True
        }

        job = api.service_api.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status == JobStatus.PENDING

        job = api.service_api.get_status(job.id)
        while job.status != JobStatus.SUCCEEDED and job.status != JobStatus.FAILED:
            job = api.service_api.get_status(job.id)

        assert job.status == JobStatus.SUCCEEDED or job.status == JobStatus.FAILED

        result = api.service_api.get_result(job.id)
        assert result is not None

        print(job, result)
