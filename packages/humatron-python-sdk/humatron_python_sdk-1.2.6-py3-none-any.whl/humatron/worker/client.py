"""
This module provides classes and utility functions for working with Humatron,
including request and response handling, payload processing, and asynchronous execution.
"""
from enum import StrEnum

"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

import datetime
import json
import os
import threading
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, NamedTuple, Any, Union
import logging

from locked_dict.locked_dict import LockedDict


class CommandType(StrEnum):
    """
    Represents a set of command types for system operations.
    """

    INTERVIEW = 'interview'
    """Command to initiate or manage an interview."""

    REGISTER = 'register'
    """Command to register an instance or user."""

    UNREGISTER = 'unregister'
    """Command to unregister an instance or user."""

    PAUSE = 'pause'
    """Command to pause an instance or service."""

    RESUME = 'resume'
    """Command to resume an instance or service."""

    HEARTBEAT = 'heartbeat'
    """Command to send a heartbeat signal for system health checks."""

    MESSAGE = 'message'
    """Command to send or process a message."""


class Address(NamedTuple):
    """
    Represents a physical address with metadata.
    """

    street: str
    """Street name and number."""

    city: str
    """City name."""

    region_name: str
    """Full name of the region (e.g., state, province)."""

    region_abbr: Optional[str]
    """Abbreviated name of the region."""

    postal_code: str
    """Postal or ZIP code."""

    country_name: str
    """Full name of the country."""

    country_iso_3166: str
    """ISO 3166 code for the country."""


class ContactRecord(NamedTuple):
    """
    Represents a single contact record.
    """

    kind: str
    """Type of contact (e.g., phone, email)."""

    tstamp: str
    """Timestamp of the contact event."""

    csv_tags: Optional[str]
    """Comma-separated tags for categorization."""

    properties: Any
    """Additional metadata or properties."""


class Contact(NamedTuple):
    """
    Represents a contact with multiple records.
    """

    first_name: Optional[str]
    """First name of the contact."""

    last_name: Optional[str]
    """Last name of the contact."""

    full_name: str
    """Full name of the contact."""

    records: list[ContactRecord]
    """List of contact records associated with the contact."""


class Person(NamedTuple):
    """
    Represents an individual or user within the system.
    """

    first_name: str
    """First name of the person."""

    last_name: Optional[str]
    """Last name of the person."""

    email: str
    """Email address of the person."""

    suspended: bool
    """Indicates if the person is suspended from the system."""

    org_id: int
    """Organization ID the person is associated with."""

    oauth_provider: Optional[str]
    """OAuth provider used for authentication, if any."""

    avatar_data_uri: Optional[str]
    """Data URI for the person's avatar."""

    oauth_avatar_url: Optional[str]
    """URL to the person's avatar from an OAuth provider."""

    primary_lang_iso_639: str
    """Primary language code (ISO 639) of the person."""

    is_email_confirmed: bool
    """Indicates whether the person's email is confirmed."""

    phone: Optional[str]
    """Phone number of the person."""

    address: Optional[Address]
    """Address information of the person."""


class File(NamedTuple):
    """
    Represents a file with associated metadata.
    """

    type: str
    """Type or format of the file (e.g., PDF, image)."""

    size: int
    """Size of the file in bytes."""

    properties: Any
    """Additional metadata or properties of the file."""


class Channel(NamedTuple):
    """
    Represents a communication channel with its capabilities.
    """

    type: str
    """Type of the channel (e.g., Slack, Email)."""

    descr: str
    """Description of the channel."""

    provider_name: str
    """Name of the service provider for the channel."""

    capabilities_csv: str
    """Comma-separated string of the channel's capabilities."""


class PricePlan(NamedTuple):
    """
    Represents a pricing plan for services.
    """

    trial_period_days: str
    """Number of trial period days for the service."""

    trial_restrictions: Optional[str]
    """Restrictions applied during the trial period."""

    service_level: str
    """Service level description."""

    setup_fee_usd: float
    """Setup fee in USD."""

    hourly_fee_usd: float
    """Hourly fee in USD."""

    monthly_fee_usd: float
    """Monthly fee in USD."""


class Role(NamedTuple):
    """
    Represents a role with associated permissions or responsibilities.
    """

    name: str
    """Name of the role."""

    descr: str
    """Description of the role's purpose."""


class Resource(NamedTuple):
    """
    Represents a resource within the system.
    """

    id: int
    """Unique identifier for the resource."""

    channel_type: str
    """Type of the communication channel associated with the resource."""

    csv_tags: Optional[str]
    """Comma-separated tags for resource categorization."""

    properties: Any
    """Additional metadata or properties of the resource."""


class Organization(NamedTuple):
    """
    Represents an organization with associated metadata.
    """

    id: int
    """Unique identifier for the organization."""

    avatar_url: Optional[str]
    """URL to the organization's avatar."""

    show_name: bool
    """Indicates whether the organization's name should be displayed."""

    avatar_on_right: bool
    """Indicates whether the avatar is displayed on the right side."""

    name: str
    """Display name of the organization."""

    formal_name: Optional[str]
    """Formal name of the organization."""

    industry: Optional[str]
    """Industry the organization operates in."""

    website: str
    """Website URL of the organization."""

    is_root: bool
    """Indicates whether the organization is the root entity."""

    address: Optional[Address]
    """Address information of the organization."""

    country: Optional[str]
    """Country name of the organization."""

    country_iso_3166: Optional[str]
    """ISO 3166 code for the organization's country."""


class Specialist(NamedTuple):
    """
    Represents a specialist with various attributes and capabilities.
    """

    id: int
    """Unique identifier for the specialist."""

    planned_live_date: Optional[str]
    """The planned live date for the specialist, if applicable."""

    avatar_url: str
    """URL to the specialist's avatar."""

    status: str
    """Current status of the specialist (e.g., active, inactive)."""

    init_setup_dur_hours: int
    """Initial setup duration in hours."""

    init_setup_info: Optional[str]
    """Additional information about the initial setup."""

    support_interview_mode: bool
    """Indicates whether the specialist supports interview mode."""

    auto_interview: Optional[bool]
    """Indicates if interviews are automatically handled."""

    interview_concurrent_sessions: Optional[int]
    """Number of concurrent interview sessions allowed."""

    interview_reqs_per_hour: Optional[int]
    """Number of interview requests allowed per hour."""

    interview_sla: Optional[str]
    """Service Level Agreement for interview response times."""

    role: str
    """The role or job title of the specialist."""

    overview: str
    """Brief overview of the specialist's expertise."""

    share_summary: str
    """Summary information to be shared externally."""

    skills_csv: str
    """Comma-separated list of the specialist's skills."""

    deploy_descr: str
    """Description of the deployment responsibilities."""

    ai_stack_descr: str
    """Description of the AI stack or technologies used."""

    country_iso_3166_csv: Optional[str]
    """Comma-separated list of ISO 3166 country codes for supported regions."""

    lang_iso_639_csv: Optional[str]
    """Comma-separated list of ISO 639 language codes the specialist speaks."""

    is_human_curated: bool
    """Indicates if the specialist's profile is human-curated."""

    builder_submit_person: Person
    """Person responsible for submitting the specialist."""

    builder_support_person: Person
    """Person responsible for supporting the specialist's integration."""

    builder_org: Organization
    """Organization responsible for building the specialist."""

    builder_descr_url: Optional[str]
    """URL for additional description about the builder."""

    support_descr: str
    """Description of the specialist's support capabilities."""

    support_email: str
    """Support email for contacting the specialist."""

    is_private: bool
    """Indicates whether the specialist's profile is private."""

    api_endpoint: Optional[str]
    """API endpoint for interacting with the specialist."""

    price_plan: PricePlan
    """Pricing plan associated with the specialist."""

    channels: list[Channel]
    """List of communication channels associated with the specialist."""


class Instance(NamedTuple):
    """
    Represents an instance of a service, tied to a specialist and an organization.
    """

    id: int
    """Unique identifier for the instance."""

    specialist: Specialist
    """The specialist associated with the instance."""

    org: Organization
    """The organization the instance is part of."""

    status: str
    """Current status of the instance (e.g., active, paused)."""

    first_names: str
    """First names of the person tied to the instance."""

    last_name: Optional[str]
    """Last name of the person tied to the instance."""

    avatar_urls: str
    """URLs of the avatars associated with the instance."""

    gender: str
    """Gender of the person tied to the instance."""

    age: str
    """Age of the person tied to the instance."""

    country_iso_3166: str
    """ISO 3166 country code for the instance."""

    country_name: str
    """Country name of the instance."""

    city: str
    """City of the instance."""

    tz: str
    """Time zone of the instance."""

    primary_lang_iso_639: str
    """Primary language code (ISO 639) of the instance."""

    comm_style: str
    """Communication style used by the instance."""

    lang_mode: str
    """Language mode or setting of the instance."""

    work_type: str
    """Type of work being handled by the instance."""

    workplace_persona: str
    """Persona associated with the instance in the workplace."""

    brevity: str
    """Level of brevity in communication for the instance."""

    job_title: str
    """Job title of the person tied to the instance."""

    job_descr: Optional[str]
    """Job description for the instance."""

    team: str
    """Team name or role associated with the instance."""

    pay_type: str
    """Payment type or method for the instance."""

    hired_by_person: Person
    """Person who hired the individual for the instance."""

    reporting_to_person: Person
    """Person the instance reports to."""

    contact_person: Person
    """Contact person for the instance."""

    hire_ts: str
    """Timestamp of when the instance was hired."""

    start_date: str
    """Start date of the instance's work."""

    live_ts: Optional[str]
    """Timestamp of when the instance went live."""

    termination_ts: Optional[str]
    """Timestamp of the instance's termination, if applicable."""

    termination_reason: Optional[str]
    """Reason for the instance's termination."""


class RequestDataInterview(NamedTuple):
    """
    Represents the data payload for initiating an interview request.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    ses_id: str
    """Session ID for tracking the interview."""

    person: Person
    """The person involved in the interview."""

    org: Organization
    """The organization involved in the interview."""

    specialist: Specialist
    """The specialist handling the interview."""

    ref_resp_payload_id: Optional[str]
    """Reference ID to the response payload, if applicable."""

    kind: str
    """Type or kind of interview."""

    text: Optional[str]
    """Text content or message associated with the interview."""


class ResponseDataInterview(NamedTuple):
    """
    Represents the data payload for responding to an interview request.
    """

    resp_cmd: CommandType
    """Response command for the interview (e.g., accept, reject)."""

    ses_id: str
    """Session ID for tracking the interview response."""

    payload_id: str
    """Unique identifier for the response payload."""

    ref_payload_id: str
    """Reference to the original request payload."""

    text: Optional[str]
    """Text content or message in the response."""

    @classmethod
    def make(
        cls,
        ses_id: str,
        payload_id: str,
        ref_payload_id: str,
        text: Optional[str] = None
    ) -> 'ResponseDataInterview':
        """Factory method to create a `ResponseDataInterview` object."""
        return cls(CommandType.INTERVIEW, ses_id, payload_id, ref_payload_id, text)


class RequestDataHeartbeat(NamedTuple):
    """
    Represents the data payload for a heartbeat request to keep the instance active.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance for which the heartbeat is being sent."""

    contacts: list[Contact]
    """List of contacts related to the request."""

    resources: list[Resource]
    """List of resources involved in the request."""


class RequestDataRegister(NamedTuple):
    """
    Represents the data payload for registering an instance.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance to be registered."""

    contacts: list[Contact]
    """List of contacts related to the registration."""

    resources: list[Resource]
    """List of resources involved in the registration."""


class ResponseDataRegister(NamedTuple):
    """
    Represents the data payload for the response to a registration request.
    """

    resp_cmd: CommandType
    """Command type for the response."""

    instance_id: int
    """Unique identifier for the instance."""

    ref_payload_id: str
    """Reference to the original request payload."""

    result: bool
    """Result of the registration process (True if successful)."""

    reject_code: Optional[int]
    """Optional rejection code if the registration fails."""

    contacts: Optional[list[Contact]]
    """Optional list of updated contacts after registration."""

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        reject_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataRegister':
        """Factory method to create a `ResponseDataRegister` object."""
        return cls(CommandType.REGISTER, instance_id, ref_payload_id, result, reject_code, contacts)


class RequestDataUnregister(NamedTuple):
    """
    Represents the data payload for unregistering an instance.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance to be unregistered."""

    contacts: list[Contact]
    """List of contacts related to the unregistration."""

    resources: list[Resource]
    """List of resources involved in the unregistration."""


class ResponseDataUnregister(NamedTuple):
    """
    Represents the data payload for the response to an unregistration request.
    """

    resp_cmd: CommandType
    """Command type for the response."""

    instance_id: int
    """Unique identifier for the instance."""

    ref_payload_id: str
    """Reference to the original request payload."""

    contacts: Optional[list[Contact]]
    """Optional list of updated contacts after unregistration."""

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataUnregister':
        """Factory method to create a `ResponseDataUnregister` object."""
        return cls(CommandType.UNREGISTER, instance_id, ref_payload_id, contacts)


class RequestDataPause(NamedTuple):
    """
    Represents the data payload for pausing an instance.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance to be paused."""

    contacts: list[Contact]
    """List of contacts related to the pause request."""

    resources: list[Resource]
    """List of resources involved in the pause request."""


class ResponseDataPause(NamedTuple):
    """
    Represents the data payload for the response to a pause request.
    """

    resp_cmd: CommandType
    """Command type for the response."""

    instance_id: int
    """Unique identifier for the instance."""

    ref_payload_id: str
    """Reference to the original request payload."""

    result: bool
    """Result of the pause process (True if successful)."""

    error_code: Optional[int]
    """Optional error code if the pause process fails."""

    contacts: list[Contact]
    """List of contacts involved in the pause process."""

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        error_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataPause':
        """Factory method to create a `ResponseDataPause` object."""
        return cls(CommandType.PAUSE, instance_id, ref_payload_id, result, error_code, contacts)


class RequestDataResume(NamedTuple):
    """
    Represents the data payload for resuming an instance.
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance to be resumed."""

    contacts: list[Contact]
    """List of contacts related to the resume request."""

    resources: list[Resource]
    """List of resources involved in the resume request."""


class ResponseDataResume(NamedTuple):
    """
    Represents the data payload for the response to a resume request.
    """

    resp_cmd: CommandType
    """Command type for the response."""

    instance_id: int
    """Unique identifier for the instance."""

    ref_payload_id: str
    """Reference to the original request payload."""

    result: bool
    """Result of the resume process (True if successful)."""

    error_code: Optional[int]
    """Optional error code if the resume process fails."""

    contacts: list[Contact]
    """List of contacts involved in the resume process."""

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        error_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataResume':
        """Factory method to create a `ResponseDataResume` object."""
        return cls(CommandType.RESUME, instance_id, ref_payload_id, result, error_code, contacts)


class RequestDataSlack(NamedTuple):
    """
    Represents the data payload for a Slack message.
    """

    body: Any
    """The body of the Slack message."""

    conversation: Any
    """Conversation details associated with the Slack message."""

    conversation_users: list[Any]
    """List of users involved in the conversation."""

    files: Optional[list[File]]
    """Optional list of files attached to the Slack message."""


class RequestDataEmail(NamedTuple):
    """
    Represents the data payload for an email.
    """

    sender: str
    """The sender of the email."""

    to: str
    """Recipient of the email."""

    reply_to: Optional[str]
    """Optional reply-to email address."""

    subj: Optional[str]
    """Optional subject of the email."""

    cc: Optional[str]
    """Optional list of CC'd recipients."""

    bcc: Optional[str]
    """Optional list of BCC'd recipients."""

    html: Optional[str]
    """Optional HTML content of the email."""

    text: Optional[str]
    """Optional plain text content of the email."""

    files: Optional[list[File]]
    """Optional list of files attached to the email."""


class RequestDataSms(NamedTuple):
    """
    Represents the data payload for an SMS message.
    """

    sender: str
    """The sender of the SMS."""

    receiver: str
    """The receiver of the SMS."""

    text: str
    """The text content of the SMS."""


class RequestDataRest(NamedTuple):
    """
    Represents the data payload for an REST channel message.
    """

    sender: str
    """The sender of the REST channel message."""

    receiver: str
    """The receiver of the REST channel message."""

    text: str
    """The text content of the REST channel message."""


class RequestDataMessage(NamedTuple):
    """
    Represents the data payload for sending a message (Slack, Email, or SMS).
    """

    payload_id: str
    """Unique identifier for the request payload."""

    instance: Instance
    """The instance for which the message is being sent."""

    contacts: list[Contact]
    """List of contacts involved in the message request."""

    resources: list[Resource]
    """List of resources involved in the message request."""

    resource_id: int
    """Identifier for the resource being used in the message."""

    message: Union[RequestDataSlack, RequestDataEmail, RequestDataSms, RequestDataRest]
    """The message payload (Slack, Email, SMS or REST)."""


class ResponseDataSlack(NamedTuple):
    """
    Represents the data payload for the response to a Slack message request.
    """

    channel: str
    """Slack channel where the message was posted."""

    text: Optional[str]
    """Optional text content of the message."""

    thread_ts: Optional[str]
    """Optional thread timestamp for the message."""

    files: Optional[list[File]]
    """Optional list of files attached to the message."""

    @classmethod
    def make(
        cls,
        channel: str,
        text: Optional[str] = None,
        thread_ts: Optional[str] = None,
        files: Optional[list[File]] = None
    ) -> 'ResponseDataSlack':
        """Factory method to create a `ResponseDataSlack` object."""
        if not text and not files:
            raise ValueError('Either text or files must be provided.')
        return cls(channel, text, thread_ts, files)


class ResponseDataEmail(NamedTuple):
    """
    Represents the data payload for the response to an email request.
    """

    sender: str
    """The sender of the email."""

    to: str
    """Recipient of the email."""

    reply_to: Optional[str]
    """Optional reply-to email address."""

    subj: Optional[str]
    """Optional subject of the email."""

    cc: Optional[str]
    """Optional list of CC'd recipients."""

    bcc: Optional[str]
    """Optional list of BCC'd recipients."""

    html: Optional[str]
    """Optional HTML content of the email."""

    text: Optional[str]
    """Optional plain text content of the email."""

    files: Optional[list[File]]
    """Optional list of files attached to the email."""

    @classmethod
    def make(
        cls,
        sender: str,
        to: str,
        reply_to: Optional[str] = None,
        subj: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: Optional[str] = None,
        text: Optional[str] = None,
        files: Optional[list[File]] = None
    ) -> 'ResponseDataEmail':
        """Factory method to create a `ResponseDataEmail` object."""
        if not text and not html and not files:
            raise ValueError('Either text, html or files must be provided.')
        return cls(sender, to, reply_to, subj, cc, bcc, html, text, files)


class ResponseDataSms(NamedTuple):
    """
    Represents the data payload for the response to an SMS request.
    """

    sender: str
    """The sender of the SMS."""

    receiver: str
    """The receiver of the SMS."""

    text: str
    """The text content of the SMS."""

    @classmethod
    def make(
        cls,
        sender: str,
        receiver: str,
        text: str
    ) -> 'ResponseDataSms':
        """Factory method to create a `ResponseDataSms` object."""
        return cls(sender, receiver, text)


class ResponseDataRest(NamedTuple):
    """
    Represents the data payload for the response to a REST channel request.
    """

    sender: str
    """The sender of the REST channel message."""

    receiver: str
    """The receiver of the REST channel message."""

    text: str
    """The text content of the REST channel message."""

    @classmethod
    def make(
        cls,
        sender: str,
        receiver: str,
        text: str
    ) -> 'ResponseDataRest':
        """Factory method to create a `ResponseDataRest` object."""
        return cls(sender, receiver, text)


class ResponseDataMessage(NamedTuple):
    """
    Represents the data payload for the response to a message request (Slack, Email, or SMS).
    """

    resp_cmd: CommandType
    """Command type for the response."""

    instance_id: int
    """Unique identifier for the instance."""

    resource_id: int
    """Identifier for the resource being used in the message."""

    message: Union[ResponseDataSlack, ResponseDataEmail, ResponseDataSms, ResponseDataRest]
    """The response message payload (Slack, Email, SMS or REST)."""

    ref_payload_id: Optional[str]
    """Reference to the original request payload."""

    translate_lang: Optional[str]
    """Optional language to translate the message to."""

    tone_shifting: Optional[str]
    """Optional tone shifting for the message."""

    contacts: Optional[list[Contact]]
    """Optional list of contacts involved in the message."""

    @classmethod
    def make(
        cls,
        instance_id: int,
        resource_id: int,
        message: Union[ResponseDataSlack, ResponseDataEmail, ResponseDataSms, ResponseDataRest],
        ref_payload_id: Optional[str] = None,
        translate_lang: Optional[str] = None,
        tone_shifting: Optional[str] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataMessage':
        """Factory method to create a `ResponseDataMessage` object."""
        return cls(
            CommandType.MESSAGE, instance_id, resource_id, message, ref_payload_id, translate_lang, tone_shifting,
            contacts
        )


RequestPayloadPartData = Union[
    RequestDataInterview,
    RequestDataHeartbeat,
    RequestDataRegister,
    RequestDataUnregister,
    RequestDataPause,
    RequestDataResume,
    RequestDataMessage
]
"""Request payload part data type alias."""

ResponsePayloadPartData = Union[
    ResponseDataInterview,
    ResponseDataRegister,
    ResponseDataUnregister,
    ResponseDataPause,
    ResponseDataResume,
    ResponseDataMessage
]
"""Request payload part data type alias."""

Storage = dict[Any, Any]
"""Storage type alias."""


class Request(NamedTuple):
    """
    Represents a Humatron request with a command, unique ID, timestamp, payload, and optional storage.
    """

    req_cmd: CommandType
    """ The command associated with the request."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp when the request was created in ISO format."""
    payload: list[RequestPayloadPartData]
    """A list of payload parts containing the data for the request."""
    storage: Optional[Storage]
    """Optional storage for maintaining state during request processing."""

    @classmethod
    def from_json(cls, js: str) -> 'Request':
        """
        Creates a Request instance from a JSON string.

        @param js :
            The JSON string representing the request.

        @return:
            A new Request instance.
        """
        return cls.from_dict(json.loads(js))

    @classmethod
    def from_dict(cls, d: dict[Any, Any]) -> 'Request':
        """
        Creates a Request instance from a dictionary.

        @param d :
            A dictionary containing the request data.

        @return:
            A new Request instance.
        """
        return cls(CommandType(d['req_cmd']), d['req_id'], d['req_tstamp'], d['payload'], d.get('storage'))


class Response(NamedTuple):
    """
    Represents a Humatron response with a unique ID, timestamp, optional payload, and optional storage.
    """

    resp_id: str
    """The unique identifier for the response."""
    resp_tstamp: str
    """The timestamp when the response was created in ISO format."""
    payload: Optional[list[ResponsePayloadPartData]]
    """An optional list of payload parts containing the response data."""
    storage: Optional[Storage]
    """Optional storage for maintaining state during response processing."""

    def to_json(self) -> str:
        """
        Converts the Response instance to a JSON string.

        @return:
            A JSON string representing the Response instance.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Response instance to a dictionary.

        @return:
            A dictionary representing the Response instance.
        """
        return {
            'resp_id': self.resp_id,
            'resp_tstamp': self.resp_tstamp,
            'payload': self.payload,
            'storage': self.storage
        }


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
_logger = logging.getLogger('humatron.worker.sdk')


class RequestPayloadPart(NamedTuple):
    """
    Represents a part of the request payload with command, ID, timestamp, and payload part.
    """

    req_cmd: CommandType
    """The command associated with the payload part."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp of the request."""
    data: RequestPayloadPartData
    """A dictionary representing a part of the request payload."""


ResponsePayloadPart = Union[list[ResponsePayloadPartData], ResponsePayloadPartData, None]
"""Response payload part alias."""


class HumatronWorker(ABC):
    """
    Abstract base class for Humatron workers responsible for handling asynchronous requests.

    This class defines the contract for processing requests, where each concrete implementation
    of this class should provide its own logic for handling a request and returning an appropriate
    response.
    """

    @abstractmethod
    def process_request(self, req: Request) -> Optional[Response]:
        """
        Posts a request asynchronously, processing its payload parts and returning a response.

        @param req :
            The request to be processed asynchronously.

        @return:
            The response after processing the request, or None if no response is available.
        """

        pass


class HumatronAsyncWorker(HumatronWorker, ABC):
    """
    Asynchronous adapter for Humatron worker using a thread pool executor.

    This class extends the HumatronWorker to provide asynchronous request processing
    using a thread pool for concurrency.
    """

    def __init__(self, pool_size: Optional[int] = None):
        """
        Initializes the async adapter with a thread pool.

        @param pool_size :
            The maximum number of threads in the pool. Defaults to the number of CPUs.
        """

        if pool_size is not None and pool_size <= 0:
            raise ValueError('Pool size must be greater than 0.')

        self._pool = ThreadPoolExecutor(max_workers=pool_size or os.cpu_count())
        self._resp_payloads_parts_data: list[ResponsePayloadPart] = []
        self._lock = threading.Lock()
        self._storage: Optional[LockedDict] = None

    def close(self) -> None:
        """
        Shuts down the thread pool, ensuring all tasks are completed.
        """
        self._pool.shutdown()

    def process_request(self, req: Request) -> Optional[Response]:
        if req.req_cmd == CommandType.INTERVIEW:
            if req.storage:
                raise ValueError('Storage cannot be provided for `interview` requests.')
            elif not req.payload or len(req.payload) != 1:
                raise ValueError('Invalid payload for `interview` request.')

            pp = self.process_payload_part(
                RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, req.payload[0]), None
            )

            match pp:
                case dict():
                    return Response(_make_id(), _utc_now_iso_format(), [pp], None)
                case _:
                    raise ValueError(f'Unexpected response payload for `interview` request [payload={pp}]')

        if self._storage is None:
            self._storage = LockedDict()
            self._storage.update(req.storage)

        def fn() -> None:
            try:
                res: list[ResponsePayloadPart] = []
                if req.payload:
                    for parts_data in req.payload:
                        rpp = RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, parts_data)
                        parts_data = self.process_payload_part(rpp, self._storage)

                        if parts_data is not None:
                            if not isinstance(parts_data, list):
                                parts_data = [parts_data]

                            parts_data = list(filter(lambda el: el, parts_data)) if parts_data else None

                            if parts_data:
                                res.extend(parts_data)
                    with self._lock:
                        if res:
                            self._resp_payloads_parts_data.extend(res)
            except Exception as e:
                _logger.error(f'Error during processing [error={e}]', exc_info=True)

        self._pool.submit(fn)

        with self._lock:
            if not self._resp_payloads_parts_data and not self._storage:
                return None

            payloads = self._resp_payloads_parts_data[:]
            self._resp_payloads_parts_data.clear()

        return Response(_make_id(), _utc_now_iso_format(), (payloads if payloads else None), self._storage.copy())

    @abstractmethod
    def process_payload_part(
        self, req_payload_part: RequestPayloadPart, storage: Optional[Storage]
    ) -> ResponsePayloadPart:
        """
        Abstract method to process a request payload part.

        @param req_payload_part :
            The request payload part to be executed.
        @param storage :
            Optional storage used for processing. It is always None for `interview` requests.

        @return:
            The result of the execution, which could be a list of payload parts, a single payload part, or None.
        """
        pass


# Utility functions

def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format, truncated to milliseconds.

    @return:
        The current UTC time in ISO format, truncated to milliseconds.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def _make_id() -> str:
    """
    Generates a unique ID.

    @return:
        A unique identifier string.
    """
    return str(uuid.uuid4().hex)


def make_default_response_payload(
    req_cmd: CommandType, req_payload_part: RequestPayloadPartData
) -> Optional[ResponsePayloadPartData]:
    """
    Generates a default response payload based on the request command.

    @param req_cmd :
        The command associated with the request.
        Supported: CommandType.REGISTER, CommandType.PAUSE, CommandType.RESUME, CommandType.UNREGISTER, CommandType.HEARTBEAT

    @param req_payload_part :
        The request payload part for which to generate a response.

    @return:
        The generated response payload, or None if the request command is not supported.
    """
    match req_cmd:
        case CommandType.REGISTER:
            return ResponseDataRegister.make(
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                reject_code=None,
                contacts=req_payload_part.contacts
            )
        case CommandType.PAUSE:
            return ResponseDataPause.make(
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                error_code=None,
                contacts=req_payload_part.contacts
            )
        case 'resume':
            return ResponseDataResume(
                resp_cmd=req_cmd,
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                error_code=None,
                contacts=req_payload_part.contacts
            )
        case 'unregister':
            return ResponseDataUnregister(
                resp_cmd=req_cmd,
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                contacts=req_payload_part.contacts
            )
        case 'heartbeat':
            return None
        case _:
            raise ValueError(f'Unsupported request type: {req_cmd}')
