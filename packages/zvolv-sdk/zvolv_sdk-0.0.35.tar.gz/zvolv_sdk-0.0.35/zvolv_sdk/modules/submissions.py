from elasticsearch_dsl import Search as ESearch
from ..models.submission import Submission
import requests


class Submissions:
    def __init__(self, session, logger, base_url):
        self.session = session
        self.logger = logger
        self.base_url = base_url
        self.workspace_instance = None

    def get(self, id):
        """
        Get form submission details from id.

        :param id: FormSubmissionID/id of entry
        :return:
        """
        if not id:
            raise ValueError("id field is required to update the submission")

        try:
            url = f"{self.base_url}/api/v1/submissions/{id}"
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') is False:
                self.logger.info(f"Form details retrieved successfully for id {id}")
            else:
                raise ValueError(resp.get('message'))
            return Submission(**resp['data']['elements'][0])
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e

    def search(self, form_id: str, search_obj: ESearch):
        """
        Search the Analytics API to fetch data from a specific form.

        This method sends a POST request to the Analytics API, which is based on Elasticsearch.
        It searches the data associated with a specific form ID using the provided query parameters.

        :param form_id: The ID of the form to search.
        :param search_obj: The search query.
        :return:
        """

        # Accept only elasticsearch-dsl Search object as searchObj
        if not isinstance(search_obj, ESearch):
            raise ValueError("searchObj field should be an instance of elasticsearch-dsl Search object")

        if not form_id:
            raise ValueError("formId field is required to search the submissions")

        try:
            query = search_obj.to_dict()
            url = f"{self.base_url}/api/v1/analytics/search"
            response = self.session.post(url, json={'formId': form_id, 'query': query})
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') is False:
                self.logger.info(f"Successfully completed search operation for form {id}")
            else:
                raise ValueError(resp.get('message'))
            return resp['data']
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e

    def put(self, submission: Submission, skip_validation: bool = True, skip_automation: bool = True, skip_formula_validation: bool = True):
        """Update existing submission"""
        if not isinstance(submission, Submission):
            raise ValueError("submission field should be an instance of Submission model")

        if not submission.id:
            raise ValueError("id field is required to update the submission")

        if not submission.elements or submission.elements == []:
            raise ValueError("elements field with least 1 element is required to update the submission")

        try:
            url = f"{self.base_url}/api/v1/submissions/{submission.id}?skipValidation={skip_validation}&skipAutomation={skip_automation}&skipFormulaValidation={skip_formula_validation}"
            response = self.session.put(url, json=submission.model_dump(exclude_none=True, exclude_unset=True))
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') is False:
                self.logger.info(f"Successfully updated entry for id {submission.id}")
            else:
                raise ValueError(resp.get('message'))
            return resp
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e

    def post(self, submission: Submission, skip_validation: bool = True, skip_automation: bool = True, skip_formula_validation: bool = True):
        """Create a new submission"""
        if not isinstance(submission, Submission):
            raise ValueError("submission field should be an instance of Submission model")

        if not submission.formId:
            raise ValueError("formId field is required to create the submission")

        if not submission.elements:
            raise ValueError("elements field is required to create the submission")

        try:
            url = f"{self.base_url}/api/v1/submissions?skipValidation={skip_validation}&skipAutomation={skip_automation}&skipFormulaValidation={skip_formula_validation}"
            response = self.session.post(url, json=submission.model_dump(exclude_none=True, exclude_unset=True))
            response.raise_for_status()  # Raise an exception for HTTP errors

            resp = response.json()
            if resp.get('error') is False:
                self.logger.info(f"Successfully added a new entry for form {submission.formId}")
            else:
                raise ValueError(resp.get('message'))
            return resp
        except requests.exceptions.RequestException as http_err:
            error_response = response.json()
            status_code = error_response.get('statusCode', response.status_code)
            error_message = error_response.get('message', str(http_err))

            error_message = f"{status_code} Error: {error_message}"
            self.logger.error(f"An error occurred: {error_message}")
            raise requests.exceptions.HTTPError(error_message)
        except Exception as e:
            self.logger.error(e)
            raise e
