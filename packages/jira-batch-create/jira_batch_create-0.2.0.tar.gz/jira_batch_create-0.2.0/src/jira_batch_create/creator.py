import csv
import logging
import requests


class JiraIssueCreator:
    def __init__(self, csv_file_path):
        self.logger = logging.getLogger(__name__)
        self.field_mapping = {}
        self._load_field_mapping(csv_file_path)

    def _load_field_mapping(self, csv_file_path):
        """
        Load Jira field mapping from the CSV file into a dictionary.
        """
        self.logger.debug(f"Loading field mapping from {csv_file_path}")
        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user_field_name = row['Name']
                    backend_field_name = row['id']
                    self.field_mapping[user_field_name] = backend_field_name
            self.logger.info(f"Field mapping loaded successfully from {csv_file_path}")
        except Exception as e:
            self.logger.error(f"Error loading field mapping from {csv_file_path}: {e}")
            raise

    def translate_fields(self, issue_data):
        """
        Translate user-facing Jira field names to backend names based on the mapping.
        """
        self.logger.debug(f"Translating fields for issue: {issue_data}")
        translated_data = {}
        for user_field, value in issue_data.items():
            backend_field = self.field_mapping.get(user_field, user_field)
            translated_data[backend_field] = value
        self.logger.debug(f"Translated issue: {translated_data}")
        return translated_data

    def batch_create_payload(self, issues_data):
        """
        Batch create Jira issues by translating field names and sending REST requests.
        """
        # self.logger.debug(f"Preparing to create issues in Jira: {jira_url}")
        translated_issues = []
        for issue in issues_data:
            translated_issue = {
                "fields": self.translate_fields(issue)
            }
            translated_issues.append(translated_issue)
        self.payload = {
            "issueUpdates": translated_issues
        }

    def post_batch_create_request(self, jira_url, auth):
        """
        Send request for payload prepared in self.payload
        """
        url = f"{jira_url}/rest/api/3/issue/bulk"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            self.logger.info("Sending batch issue creation request to Jira")
            response = requests.post(url, auth=auth, headers=headers, json=self.payload)
            response.raise_for_status()
            self.logger.info("Issues created successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error creating issues in Jira: {e}")
            raise
