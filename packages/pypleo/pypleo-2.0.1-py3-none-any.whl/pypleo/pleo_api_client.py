# WWT Pixel Pleo API Client Module
# Title: pleo-api-client
# Author: Scott Murray (scott.murray@wwt.com)
# Version: 1.0
# Changelog:
# 2023-09-08: Initial Draft.

# IMPORT REQUIRED MODULES:
import requests
from time import sleep

# API ENDPOINTS:
expenses_endpoint = 'https://openapi.pleo.io/v1/expenses/'
tag_group_endpoint = 'https://openapi.pleo.io/v1/tag-groups/'
tags_endpoint = 'https://openapi.pleo.io/v1/tag-groups/tagGroupId/tags/'
receipt_endpoint = 'https://openapi.pleo.io/v1/expenses/expenseId/receipts/'
employee_endpoint = 'https://openapi.pleo.io/v1/employees/'
account_endpoint = 'https://openapi.pleo.io/v1/accounts/'

# API RETRY STRATEGY:
MAX_RETRIES = 3

# DISABLE URLLIB3 WARNING:
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PleoAPIClient:
    ####################################################################################################################
    # INITIALIZER
    def __init__(self, api_key):
        """
        Wrapper for the Pleo REST API.
        """
        self.access_token = api_key

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"}

    ####################################################################################################################
    # METHODS
    ####################################################################################################################
    def __get_request(self, url):
        """
        Send the API GET Request. Internal Method
        """
        for _ in range(MAX_RETRIES):
            response = requests.request('GET', url=url, headers=self.headers)
            if response.ok:
                return response.json()
            print(response.content)
            sleep(0.1)

    ####################################################################################################################
    def __post_request(self, url, payload):
        """
        Send the API POST Request. Internal Method
        """
        for _ in range(MAX_RETRIES):
            response = requests.request('POST', url=url, json=payload, headers=self.headers)
            if response.ok:
                return response.json()
            print(response.content)
            sleep(0.1)

    ####################################################################################################################
    def __delete_request(self, url):
        """
        Send the API DELETE Request. Internal Method
        """
        for _ in range(MAX_RETRIES):
            response = requests.request('DELETE', url=url, headers=self.headers)
            if response.ok:
                return response.text
            print(response.content)
            sleep(0.1)

    ####################################################################################################################
    def __put_request(self, url, payload):
        """
        Send the API PUT Request. Internal Method
        """
        for _ in range(MAX_RETRIES):
            response = requests.request('PUT', url=url, json=payload, headers=self.headers)
            if response.ok:
                return response.json()
            print(response.content)
            sleep(0.1)

    ####################################################################################################################
    def get_all_expenses(self):
        """
        Get all expense reports.
        :return: Dictionary. Return None on API call failure.
        """
        url = f"{expenses_endpoint}?pageSize=100000"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_expenses_between(self, date_from, date_to):
        """
        Get all expense reports between 2 dates. Format must be YYYY-MM-DD
        :return: Dictionary. Return None on API call failure.
        """
        url = f"{expenses_endpoint}?dateFrom={date_from}&dateTo={date_to}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_expense(self, expense_id):
        """
        Get a specific expense using the expense ID
        :param expense_id: UUID of the expense
        :return: Dictionary. Return None on API call failure.
        """
        url = f"{expenses_endpoint}{expense_id}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_all_employees(self):
        """
        Get all employees in the company
        :return: Dictionary. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/employees/"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_employee(self, employee_id):
        """
        Get employee data from their ID
        :param employee_id: Unique UUID of the employee
        :return: Dictionary. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/employees/{employee_id}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def create_employee(self, email_address, first_name, last_name, job_title, phone):
        """
        Add a new employee
        :param email_address: Email Address of the Employee
        :param first_name: First name of employee
        :param last_name: Last name of employee
        :param job_title: Job title of employee
        :param phone: Phone number of employee
        :return: Dictionary containing the UUID of the new employee. Return None on API call failure.
        """
        new_user_url = f"https://openapi.pleo.io/v1/employees/"
        post_payload = {"email": email_address}
        new_user_id = self.__post_request(new_user_url, post_payload)['id']

        update_user_url = f"https://openapi.pleo.io/v1/employees/{new_user_id}"
        new_user_payload = {"firstName": first_name,
                            "lastName": last_name,
                            "jobTitle": job_title,
                            "phone": phone}
        updated_employee = self.__put_request(update_user_url, new_user_payload)
        return updated_employee

    ####################################################################################################################
    def delete_employee(self, employee_id):
        """
        Delete an employee
        :param employee_id: UUID of the employee
        :return: 200 success HTTP Response
        """
        url = f"https://openapi.pleo.io/v1/employees/{employee_id}"
        response = self.__delete_request(url)
        return response

    ####################################################################################################################
    def get_all_tag_groups(self):
        """
        Get all the tag groups.
        :return: Dictionary. Return None on API call failure.
        """
        url = "https://openapi.pleo.io/v1/tag-groups"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_all_tags_in_group(self, tag_group):
        """
        Get all the tags for a specific tag group.
        :return: Dictionary. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/tag-groups/{tag_group}/tags"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_a_tag(self, tag_group, tag_id):
        """
        Get a specific tag from a tag group
        :return: Dictionary. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/tag-groups/{tag_group}/tags/{tag_id}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def create_a_tag(self, tag_group, attribute_id, tag_name):
        """
        Create a new tag within a specific tag group.
        :param: tag_group: The UUID of the Tag Group
        :param: attribute_id: This is the internal pleo identifier of the created tag group attribute.
        :param: tag_name: The name of the new tag.
        :return: Dictionary. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/tag-groups/{tag_group}/tags"
        payload = {"attributeValues": [{"attributeId": f"{attribute_id}", "value": f"{tag_name}"}]}
        response = self.__post_request(url, payload)
        return response

    ####################################################################################################################
    def delete_a_tag(self, tag_group, tag_id):
        """
        Delete a new tag within a specific tag group.
        :param: tag_group: The UUID of the Tag Group.
        :param: tag_id: UUID of the tag to be deleted.
        :return: 200 Success HTTP Response
        """
        url = f"https://openapi.pleo.io/v1/tag-groups/{tag_group}/tags/{tag_id}"
        response = self.__delete_request(url)
        return response

    ####################################################################################################################
    def get_all_receipts(self, expense_id):
        """
        Get all receipts associated with an expense
        :param: expense_id: UUID of the expense.
        :return: Dictionary containing receipt download URLs. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/expenses/{expense_id}/receipts"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_a_receipt(self, expense_id, receipt_id):
        """
        Get all receipts associated with an expense
        :param: expense_id: UUID of the expense.
        :return: Dictionary containing receipt download URLs. Return None on API call failure.
        """
        url = f"https://openapi.pleo.io/v1/expenses/{expense_id}/receipts/{receipt_id}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_company_balance(self):
        """
        Get company balance
        :return: Dictionary. Return None on API call failure.
        """
        url = "https://openapi.pleo.io/v1/companies/balance"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_all_accounts(self):
        """
        Get all accounts within the company.
        :return: Dictionary. Return None on API call failure
        """
        url = account_endpoint
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    def get_account(self, account_id):
        """
        Get the details of a specific account
        :param account_id: UUID of the account
        :return: Dictionary. Return None on API call failure
        """
        url = f"{account_endpoint}{account_id}"
        response = self.__get_request(url)
        return response

    ####################################################################################################################
    # END
    ####################################################################################################################
