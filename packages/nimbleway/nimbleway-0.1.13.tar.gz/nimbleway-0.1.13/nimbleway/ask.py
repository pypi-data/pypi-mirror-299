import csv
import io
from enum import Enum
from httpx import Client, Timeout
from time import sleep


class AskNimble:
    def __init__(self, client):
        self.headers = client.headers
        self.answerit_url = "https://answerit.webit.live"
        self.client = Client(base_url=self.answerit_url, headers=self.headers,
                                  follow_redirects=True)

    def ask_domain_retreival(self, urls: list[str], questions: list[str]) -> dict:
        request_body = {
            "sources": [{"url": url, "render": True}
                        for url in urls],
            "questions": questions,
            "depth": 1
        }
        response = self.client.post(url="/pipelines/", json=request_body)
        response.raise_for_status()
        json = response.json()
        return {**self.wait_for_pipeline_execution_to_finish(pipeline_id=json['pipeline_id'],
                                                             pipeline_execution_id=json['pipeline_execution_id']),
                "pipeline_id": json['pipeline_id'],
                "pipeline_execution_id": json['pipeline_execution_id']}

    def ask_pipeline(self, pipeline_id, questions: list[str], urls: list[str] = None,) -> dict:
        urls = [] if urls is None else urls
        request_body = {
            "sources": [{"url": url, "render": True}
                        for url in urls],
            "questions": questions,
            "depth": 1
        }
        response = self.client.patch(url=f"/pipelines/{pipeline_id}", json=request_body)
        response.raise_for_status()
        json = response.json()
        return self.wait_for_pipeline_execution_to_finish(pipeline_id=pipeline_id,
                                                          pipeline_execution_id=json['pipeline_execution_id'])

    def ask_online_pipeline(self, pipeline_id, questions: list[str]) -> dict:
        # urls = [] if urls is None else urls
        request_body = {
            "table_name": "zillow",
            "sequential": "true",
            "queries": questions,
        }
        response = self.client.post(url=f"/pipelines/{pipeline_id}/ask", json=request_body,
                                    timeout=Timeout(10.0, read=None))
        response.raise_for_status()
        json = response.json()
        return json

    def ask_webapi(self, webapi_data: list[dict], questions: list[str],  pipeline_id: str = '') -> dict:
        pipeline_id = 'amazon248'  # if pipeline_id == '' else pipeline_id
        # Prepare the endpoint
        url = f"/pipelines/{pipeline_id}/ask_data"

        csv_file = io.StringIO()
        if webapi_data:
            fieldnames = webapi_data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            keys_to_remove=[]
            for data in webapi_data:
                for key in data.keys():
                    if key not in fieldnames:
                        keys_to_remove.append(key)
            for key in keys_to_remove:
                webapi_data.pop(key)
            writer.writeheader()
            writer.writerows(webapi_data)
        csv_file.seek(0)

        # Read CSV content and encode it to bytes
        csv_content = csv_file.read().encode('utf-8')

        files = {
            'datafile': csv_content
        }
        params = {
            "table_name": "amazon_reviews",  # "zillow"
            "id_col_name": "id",
            "description_col_name": "review_description",
            "sequential": "true",
            "queries": [
                "From the reviews from September and the US, what are the disadvantages of the ice cream machine?"],
        }

        response = self.client.post(url, files=files, data=params, timeout=Timeout(10.0, read=None))
        response.raise_for_status()  # Raise exception if the response is not 200 OK
        print(response.json())

    def get_pipelines(self) -> list[dict]:
        response = self.client.get(f"/pipelines/")
        response.raise_for_status()
        pipelines = response.json()
        return pipelines

    def get_pipeline(self, pipeline_id: str):
        response = self.client.get(f"/pipelines/{pipeline_id}")
        response.raise_for_status()
        pipeline = response.json()
        return pipeline

    def get_pipeline_execution(self, pipeline_id: str, pipeline_execution_id: str):
        response = self.client.get(f"/pipelines/{pipeline_id}/pipeline-executions/{pipeline_execution_id}")
        response.raise_for_status()
        pipeline_execution = response.json()
        return pipeline_execution

    def wait_for_pipeline_execution_to_finish(self, pipeline_id: str, pipeline_execution_id: str) -> dict:
        pipeline_execution = self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
        attempt_count = 0
        if pipeline_execution['status'] == Status.FAILED.value:
            raise WorkflowFailed()
        while not pipeline_execution['status'] == Status.COMPLETED.value and attempt_count < 1200:
            sleep(1)
            print("Processing")
            pipeline_execution = self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
            if pipeline_execution['status'] == Status.FAILED.value:
                raise WorkflowFailed()
            attempt_count += 1
        if attempt_count == 1200:
            raise WorkflowTimeout()
        return pipeline_execution


class Status(Enum):
    PENDING = 'Pending'
    INPROGRESS = 'InProgress'
    COMPLETED = 'Completed'
    FAILED = 'Failed'


class WorkflowFailed(Exception):
    def __init__(self):
        super().__init__()
class WorkflowTimeout(Exception):
    def __init__(self):
        super().__init__()