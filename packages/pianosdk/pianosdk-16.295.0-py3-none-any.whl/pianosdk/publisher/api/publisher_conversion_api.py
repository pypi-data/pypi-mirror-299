from datetime import datetime
from io import StringIO
from typing import TextIO, Dict, List, Union

from pianosdk.api_response import ApiResponse
from pianosdk.base_api import BaseApi
from pianosdk.configuration import Configuration
from pianosdk.httpwrap import HttpCallBack
from pianosdk.utils import _json_deserialize, _encode_parameter
from pianosdk.publisher.models.term_conversion import TermConversion
from pianosdk.publisher.models.term_conversion_dto import TermConversionDTO


class PublisherConversionApi(BaseApi):
    def __init__(self, config: Configuration, http_callback: HttpCallBack = None) -> None:
        super().__init__(config, http_callback)

    def count(self, aid: str, term_id: str = None) -> ApiResponse[int]:
        _url_path = '/api/v3/publisher/conversion/count'
        _query_url = self.config.get_base_url() + _url_path
        _query_parameters = {
            'aid': _encode_parameter(aid),
            'term_id': _encode_parameter(term_id)
        }

        _headers = {
            'api_token': self.config.api_token,
            'Accept': 'application/json'
        }

        _parameters = {

        }

        _body = None
        _files = None

        _request = self.config.http_client.build_request('GET',
                                                         _query_url,
                                                         headers=_headers,
                                                         query_parameters=_query_parameters,
                                                         parameters=_parameters,
                                                         json=_body,
                                                         files=_files)
        _response = self._execute_request(_request)
        _result = _json_deserialize(_response, int)
        return _result

    def get(self, aid: str, term_conversion_id: str = None, access_id: str = None, is_last_term_conversion: bool = None) -> ApiResponse[TermConversion]:
        _url_path = '/api/v3/publisher/conversion/get'
        _query_url = self.config.get_base_url() + _url_path
        _query_parameters = {
            'aid': _encode_parameter(aid),
            'term_conversion_id': _encode_parameter(term_conversion_id),
            'access_id': _encode_parameter(access_id),
            'is_last_term_conversion': _encode_parameter(is_last_term_conversion)
        }

        _headers = {
            'api_token': self.config.api_token,
            'Accept': 'application/json'
        }

        _parameters = {

        }

        _body = None
        _files = None

        _request = self.config.http_client.build_request('GET',
                                                         _query_url,
                                                         headers=_headers,
                                                         query_parameters=_query_parameters,
                                                         parameters=_parameters,
                                                         json=_body,
                                                         files=_files)
        _response = self._execute_request(_request)
        _result = _json_deserialize(_response, TermConversion)
        return _result

    def get_last(self, aid: str, rid: str = None, uid: str = None, subscription_id: str = None) -> ApiResponse[TermConversion]:
        _url_path = '/api/v3/publisher/conversion/lastAccess'
        _query_url = self.config.get_base_url() + _url_path
        _query_parameters = {
            'aid': _encode_parameter(aid),
            'rid': _encode_parameter(rid),
            'uid': _encode_parameter(uid),
            'subscription_id': _encode_parameter(subscription_id)
        }

        _headers = {
            'api_token': self.config.api_token,
            'Accept': 'application/json'
        }

        _parameters = {

        }

        _body = None
        _files = None

        _request = self.config.http_client.build_request('GET',
                                                         _query_url,
                                                         headers=_headers,
                                                         query_parameters=_query_parameters,
                                                         parameters=_parameters,
                                                         json=_body,
                                                         files=_files)
        _response = self._execute_request(_request)
        _result = _json_deserialize(_response, TermConversion)
        return _result

    def list(self, aid: str, offset: int = 0, limit: int = 100, uid: str = None, date_from: datetime = None, date_to: datetime = None) -> ApiResponse[List[TermConversionDTO]]:
        _url_path = '/api/v3/publisher/conversion/list'
        _query_url = self.config.get_base_url() + _url_path
        _query_parameters = {
            'aid': _encode_parameter(aid),
            'uid': _encode_parameter(uid),
            'date_from': _encode_parameter(date_from),
            'date_to': _encode_parameter(date_to),
            'offset': _encode_parameter(offset),
            'limit': _encode_parameter(limit)
        }

        _headers = {
            'api_token': self.config.api_token,
            'Accept': 'application/json'
        }

        _parameters = {

        }

        _body = None
        _files = None

        _request = self.config.http_client.build_request('GET',
                                                         _query_url,
                                                         headers=_headers,
                                                         query_parameters=_query_parameters,
                                                         parameters=_parameters,
                                                         json=_body,
                                                         files=_files)
        _response = self._execute_request(_request)
        _result = _json_deserialize(_response, TermConversionDTO)
        return _result

    def log_conversion(self, tracking_id: str, term_id: str, term_name: str, step_number: int = None, conversion_category: str = None, amount: float = None, currency: str = None, custom_params: str = None, browser_id: str = None, page_title: str = None, url: str = None, referer: str = None, content_author: str = None, content_created: str = None, content_section: str = None, content_type: str = None, tags: List[str] = None, previous_user_segments: str = None, user_state: str = None, cookie_consents: str = None) -> ApiResponse[Dict]:
        _url_path = '/api/v3/publisher/conversion/log'
        _query_url = self.config.get_base_url() + _url_path
        _query_parameters = {

        }

        _headers = {
            'api_token': self.config.api_token,
            'Accept': 'application/json'
        }

        _parameters = {
            'tracking_id': _encode_parameter(tracking_id),
            'term_id': _encode_parameter(term_id),
            'term_name': _encode_parameter(term_name),
            'step_number': _encode_parameter(step_number),
            'conversion_category': _encode_parameter(conversion_category),
            'amount': _encode_parameter(amount),
            'currency': _encode_parameter(currency),
            'custom_params': _encode_parameter(custom_params),
            'browser_id': _encode_parameter(browser_id),
            'page_title': _encode_parameter(page_title),
            'url': _encode_parameter(url),
            'referer': _encode_parameter(referer),
            'content_author': _encode_parameter(content_author),
            'content_created': _encode_parameter(content_created),
            'content_section': _encode_parameter(content_section),
            'content_type': _encode_parameter(content_type),
            'tags': _encode_parameter(tags),
            'previous_user_segments': _encode_parameter(previous_user_segments),
            'user_state': _encode_parameter(user_state),
            'cookie_consents': _encode_parameter(cookie_consents)
        }

        _body = None
        _files = None

        _request = self.config.http_client.build_request('POST',
                                                         _query_url,
                                                         headers=_headers,
                                                         query_parameters=_query_parameters,
                                                         parameters=_parameters,
                                                         json=_body,
                                                         files=_files)
        _response = self._execute_request(_request)
        _result = _json_deserialize(_response)
        return _result

