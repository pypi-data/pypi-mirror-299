# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import protocol_create_params
from .matches import (
    MatchesResource,
    AsyncMatchesResource,
    MatchesResourceWithRawResponse,
    AsyncMatchesResourceWithRawResponse,
    MatchesResourceWithStreamingResponse,
    AsyncMatchesResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .criteria import (
    CriteriaResource,
    AsyncCriteriaResource,
    CriteriaResourceWithRawResponse,
    AsyncCriteriaResourceWithRawResponse,
    CriteriaResourceWithStreamingResponse,
    AsyncCriteriaResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .criteria_instances import (
    CriteriaInstancesResource,
    AsyncCriteriaInstancesResource,
    CriteriaInstancesResourceWithRawResponse,
    AsyncCriteriaInstancesResourceWithRawResponse,
    CriteriaInstancesResourceWithStreamingResponse,
    AsyncCriteriaInstancesResourceWithStreamingResponse,
)
from ...types.protocol_read import ProtocolRead
from ...types.protocol_list_response import ProtocolListResponse

__all__ = ["ProtocolsResource", "AsyncProtocolsResource"]


class ProtocolsResource(SyncAPIResource):
    @cached_property
    def matches(self) -> MatchesResource:
        return MatchesResource(self._client)

    @cached_property
    def criteria(self) -> CriteriaResource:
        return CriteriaResource(self._client)

    @cached_property
    def criteria_instances(self) -> CriteriaInstancesResource:
        return CriteriaInstancesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProtocolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return ProtocolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProtocolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return ProtocolsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        external_protocol_id: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolRead:
        """
        Create Protocol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/protocols",
            body=maybe_transform(
                {
                    "external_protocol_id": external_protocol_id,
                    "title": title,
                },
                protocol_create_params.ProtocolCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolRead,
        )

    def retrieve(
        self,
        protocol_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolRead:
        """
        Get Protocol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/protocols/{protocol_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolRead,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolListResponse:
        """Get All Protocols"""
        return self._get(
            "/protocols",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolListResponse,
        )


class AsyncProtocolsResource(AsyncAPIResource):
    @cached_property
    def matches(self) -> AsyncMatchesResource:
        return AsyncMatchesResource(self._client)

    @cached_property
    def criteria(self) -> AsyncCriteriaResource:
        return AsyncCriteriaResource(self._client)

    @cached_property
    def criteria_instances(self) -> AsyncCriteriaInstancesResource:
        return AsyncCriteriaInstancesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProtocolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncProtocolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProtocolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncProtocolsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        external_protocol_id: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolRead:
        """
        Create Protocol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/protocols",
            body=await async_maybe_transform(
                {
                    "external_protocol_id": external_protocol_id,
                    "title": title,
                },
                protocol_create_params.ProtocolCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolRead,
        )

    async def retrieve(
        self,
        protocol_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolRead:
        """
        Get Protocol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/protocols/{protocol_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolRead,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolListResponse:
        """Get All Protocols"""
        return await self._get(
            "/protocols",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProtocolListResponse,
        )


class ProtocolsResourceWithRawResponse:
    def __init__(self, protocols: ProtocolsResource) -> None:
        self._protocols = protocols

        self.create = to_raw_response_wrapper(
            protocols.create,
        )
        self.retrieve = to_raw_response_wrapper(
            protocols.retrieve,
        )
        self.list = to_raw_response_wrapper(
            protocols.list,
        )

    @cached_property
    def matches(self) -> MatchesResourceWithRawResponse:
        return MatchesResourceWithRawResponse(self._protocols.matches)

    @cached_property
    def criteria(self) -> CriteriaResourceWithRawResponse:
        return CriteriaResourceWithRawResponse(self._protocols.criteria)

    @cached_property
    def criteria_instances(self) -> CriteriaInstancesResourceWithRawResponse:
        return CriteriaInstancesResourceWithRawResponse(self._protocols.criteria_instances)


class AsyncProtocolsResourceWithRawResponse:
    def __init__(self, protocols: AsyncProtocolsResource) -> None:
        self._protocols = protocols

        self.create = async_to_raw_response_wrapper(
            protocols.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            protocols.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            protocols.list,
        )

    @cached_property
    def matches(self) -> AsyncMatchesResourceWithRawResponse:
        return AsyncMatchesResourceWithRawResponse(self._protocols.matches)

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithRawResponse:
        return AsyncCriteriaResourceWithRawResponse(self._protocols.criteria)

    @cached_property
    def criteria_instances(self) -> AsyncCriteriaInstancesResourceWithRawResponse:
        return AsyncCriteriaInstancesResourceWithRawResponse(self._protocols.criteria_instances)


class ProtocolsResourceWithStreamingResponse:
    def __init__(self, protocols: ProtocolsResource) -> None:
        self._protocols = protocols

        self.create = to_streamed_response_wrapper(
            protocols.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            protocols.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            protocols.list,
        )

    @cached_property
    def matches(self) -> MatchesResourceWithStreamingResponse:
        return MatchesResourceWithStreamingResponse(self._protocols.matches)

    @cached_property
    def criteria(self) -> CriteriaResourceWithStreamingResponse:
        return CriteriaResourceWithStreamingResponse(self._protocols.criteria)

    @cached_property
    def criteria_instances(self) -> CriteriaInstancesResourceWithStreamingResponse:
        return CriteriaInstancesResourceWithStreamingResponse(self._protocols.criteria_instances)


class AsyncProtocolsResourceWithStreamingResponse:
    def __init__(self, protocols: AsyncProtocolsResource) -> None:
        self._protocols = protocols

        self.create = async_to_streamed_response_wrapper(
            protocols.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            protocols.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            protocols.list,
        )

    @cached_property
    def matches(self) -> AsyncMatchesResourceWithStreamingResponse:
        return AsyncMatchesResourceWithStreamingResponse(self._protocols.matches)

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithStreamingResponse:
        return AsyncCriteriaResourceWithStreamingResponse(self._protocols.criteria)

    @cached_property
    def criteria_instances(self) -> AsyncCriteriaInstancesResourceWithStreamingResponse:
        return AsyncCriteriaInstancesResourceWithStreamingResponse(self._protocols.criteria_instances)
