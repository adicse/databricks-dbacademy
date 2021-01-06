import json
import requests


class WorkspaceClient:

    def __init__(self, token, endpoint):
        self.token = token
        self.endpoint = endpoint

    def mkdirs(self, path) -> requests.Response:
        payload = {
            "path": path
        }
        response = requests.post(
            f"{self.endpoint}/api/2.0/workspace/mkdirs",
            headers={"Authorization": "Bearer " + self.token},
            data=json.dumps(payload)
        )
        assert response.status_code in [200], f"({response.status_code}): {response.text}"
        return response

    def delete_path(self, path) -> requests.Response:
        print("-" * 80)
        print(f"Deleting {path}")
        payload = {
            "path": path,
            "recursive": True
        }
        response = requests.post(
            f"{self.endpoint}/api/2.0/workspace/delete",
            headers={"Authorization": "Bearer " + self.token},
            data=json.dumps(payload)
        )
        assert response.status_code in [200, 404], f"({response.status_code}): {response.text}"
        return response

    def import_notebook(self, language, notebook_path, content) -> requests.Response:
        import base64

        payload = {
            "content": base64.b64encode(content.encode('utf-8')).decode("utf-8"),
            "path": notebook_path,
            "language": language,
            "overwrite": True,
            "format": "SOURCE"
        }
        response = requests.post(
            f"{self.endpoint}/api/2.0/workspace/import",
            headers={"Authorization": "Bearer " + self.token},
            data=json.dumps(payload)
        )
        assert response.status_code in [200], f"({response.status_code}): {response.text}"
        return response

    def export_notebook(self, notebook_path) -> str:
        auth_header = {"Authorization": "Bearer " + self.token + ""}
        uri = f"{self.endpoint}/api/2.0/workspace/export?path={notebook_path}&direct_download=true"
        response = requests.get(
            uri,
            headers=auth_header
        )
        assert response.status_code == 200, f"({response.status_code}): {response.text}"
        return response.text
