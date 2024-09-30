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

    def test_should_use_client_abstraction(self):
        client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

        health = client.health_check()
        assert health.status == "Service is up and running"

        data = {"input": {"a": 1, "b": 2}}
        params = {"param1": "value1", "param2": "value2"}

        job = client.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status == JobStatus.PENDING

        result = client.get_result(job.id)
        assert result is not None

        job = client.get_status(job.id)
        assert job.id is not None
        assert job.status == JobStatus.SUCCEEDED

    def test_should_use_generated_client(self):
        if (consumer_key is not None) or (consumer_secret is not None):
            auth = PlanqkServiceAuth(consumer_key, consumer_secret)
            api = PlanqkServiceApi(token=auth.get_token, base_url=service_endpoint)
        else:
            api = PlanqkServiceApi(token="random_token", base_url=service_endpoint)

        health = api.status_api.health_check()
        assert health.status == "Service is up and running"

        data = {"input": {"a": 1, "b": 2}}
        params = {"param1": "value1", "param2": "value2"}

        job = api.service_api.start_execution(data=data, params=params)
        assert job.id is not None
        assert job.status == JobStatus.PENDING

        status = api.service_api.get_status(job.id)
        while status.status != JobStatus.SUCCEEDED and status.status != JobStatus.FAILED:
            status = api.service_api.get_status(job.id)

        assert status.status == JobStatus.SUCCEEDED or status.status == JobStatus.FAILED

        result = api.service_api.get_result(job.id)
        assert result is not None
