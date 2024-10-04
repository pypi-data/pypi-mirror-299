"""
This module provides classes for working with Humatron,
including request and response handling, payload processing, and asynchronous execution.
"""
import datetime
import uuid

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

import json
import logging
import os
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from enum import StrEnum
from typing import Optional, NamedTuple, Any, Union

from locked_dict.locked_dict import LockedDict


class RequestType(StrEnum):
    """
    Represents a set of requests types for system operations.
    """

    INTERVIEW = 'interview'
    """
    This request is sent to the worker endpoint when a prospective hirer (employer or hiring manager) 
    initiates the interview on Humatron website (and auto-interview is not enabled)
    """

    REGISTER = 'register'
    """
    This register request is sent to AI worker endpoint when the new instance of this AI worker is hired. 
    The AI worker implementation is assumed to be multi-tenant, i.e. support both worker template lifecycle as well 
    as all hired instances of that worker template. 
    Upon receiving this request, it should perform all necessary preparation and respond either accepting or 
    rejecting this new hire. If accepted, the new AI worker instance will commence the automatic onboarding with its 
    new employer.
    """

    UNREGISTER = 'unregister'
    """
    This request is sent to AI worker endpoint when the worker instance is terminated. 
    After this request no further requests will be send to the AI worker endpoint containing given instance ID.
    """

    PAUSE = 'pause'
    """
    This request is sent to AI worker endpoint when the worker instance is paused. 
    In this state, the instance can only be either resumed or terminated.
    """

    RESUME = 'resume'
    """This request is sent to AI worker endpoint when the worker instance is resumed."""

    HEARTBEAT = 'heartbeat'
    """
    Apart from regular requests, Humatron sends regular heartbeat requests to each hired AI worker. 
    These requests are sent out at least several times a minute. 
    These heartbeat requests do not carry any meaningful data, their only purpose is to provide a regular ping so that 
    AI worker can react quasi-asynchronously over the synchronous HTTP protocol. 
    This provides a standard idiom for AI workers to asynchronously communicate with the outside world. 
    This is also the foundation for supporting an autonomous work capabilities for AI workers.
    """

    MESSAGE = 'message'
    """
    This request is sent to AI worker endpoint when there is one or more new messaged available for the worker instance.
    """


class Address(NamedTuple):
    """
    Represents a physical address with metadata.
    """

    street: str
    """Street address."""

    city: str
    """City name."""

    region_name: str
    """Name of the region."""

    region_abbr: Optional[str]
    """Optional abbreviation of the region."""

    postal_code: str
    """Postal or ZIP code."""

    country_name: str
    """Country name as in ISO 3166."""

    country_iso_3166: str
    """Country as ISO 3166 code."""


class ContactRecord(NamedTuple):
    """
    Represents a single contact record.
    """

    kind: str
    """Supported values: email, slack, phone, rest."""

    tstamp: str
    """Timestamp of the record creation in UTC, formatted according to ISO-8601."""

    csv_tags: Optional[str]
    """Optional list of comma separated tags."""

    properties: Any
    """Properties of the contact record. Properties content depends on the kind field."""


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
    """List of contact records. Order is not significant. Records are unique, as duplicates are removed."""


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
    """
    Indicates if the person is suspended. 
    Person can be suspended by Humatron only. Suspended person cannot sign in.
    """

    org_id: int
    """ID of the organization this person belongs to."""

    oauth_provider: Optional[str]
    """Name of the OAuth 2.0 provider from the last OAuth sing in."""

    avatar_data_uri: Optional[str]
    """
    Optional URL or data-URI for this person avatar. This avatar can only be set on Humatron website's user profile page. 
    Note that either this field, oauth_avatar_url or none can be provided for this person.
    """

    oauth_avatar_url: Optional[str]
    """User avatar URL from the last OAuth sing in."""

    primary_lang_iso_639: str
    """SO 639-2 code for the primary communication language for this person."""

    is_email_confirmed: bool
    """
    Whether or not this person email is confirmed. 
    Email must be confirmed before user can sign in at Humatron website.
    """

    phone: Optional[str]
    """Phone number of the person."""

    address: Optional[Address]
    """Address of the person."""


class File(NamedTuple):
    """
    Represents a file with associated metadata.
    """

    type: str
    """File provider type. Currently supported value are: AMAZON_S3."""

    size: int
    """File size in bytes."""

    properties: Any
    """File provider related properties."""


class Channel(NamedTuple):
    """
    Represents a communication channel with its capabilities.
    """

    type: str
    """Channel type. Supported values are: email, slack, SMS, rest."""

    descr: str
    """Channel description."""

    provider_name: str
    """Channel provider name."""

    capabilities_csv: str
    """Comma separated list of channel capabilities."""


class PricePlan(NamedTuple):
    """
    Represents a pricing plan for services.
    """

    trial_period_days: str
    """Number of days for the trial period. Can be zero."""

    trial_restrictions: Optional[str]
    """Restrictions during the trial period, if any."""

    service_level: str
    """
    	Description of the service level provided by this price plan. Could include response time, curation time, 
    	maximum number of request per hour, etc.
    """

    setup_fee_usd: float
    """Setup fee in USD, if any. Can be zero."""

    hourly_fee_usd: float
    """Hourly fee in USD. Cannot be zero."""

    monthly_fee_usd: float
    """Monthly fee in USD. Cannot be zero."""


class Role(NamedTuple):
    """
    Represents a role with associated permissions or responsibilities.
    """

    name: str
    """Name of the role."""

    descr: str
    """Description of the role."""


class Resource(NamedTuple):
    """
    Represents a resource within the system.
    """

    id: int
    """Resource ID."""

    channel_type: str
    """
    Type of the communication channel this resource belongs to. Supported values are: email, slack, SMS, rest.
    """

    csv_tags: Optional[str]
    """Optional list of comma separated tags."""

    properties: Any
    """Properties of the resource. Properties content depends on the channel_type field."""


class Organization(NamedTuple):
    """
    Represents an organization with associated metadata.
    """

    id: int
    """Unique ID of this organization."""

    avatar_url: Optional[str]
    """URL for this organization's logo. The image will be scaled down as much as 32 pixels in height."""

    show_name: bool
    """Whether or not this organization's name should be shown in the top-right corner of the header."""

    avatar_on_right: bool
    """Whether or not this organization's logo is displayed in the top-right corner of the header."""

    name: str
    """Name of this organization."""

    formal_name: Optional[str]
    """Formal or legal name of this organization."""

    industry: Optional[str]
    """Organization industry."""

    website: str
    """Website URL of this organization. It may optionally include the protocol part 'https://'."""

    is_root: bool
    """Indicates if this organization is the root organization (i.e. Humatron AI)."""

    address: Optional[Address]
    """Address of this organization."""

    country: Optional[str]
    """Country name of this organization as in ISO 3166."""

    country_iso_3166: Optional[str]
    """ISO 3166-2 code of the country for this organization."""


class Specialist(NamedTuple):
    """
    Represents a specialist with various attributes and capabilities.
    """

    id: int
    """Unique ID of this worker template."""

    planned_live_date: Optional[str]
    """
    Planned live date of the worker template. 
    String is used only for display purpose, i.e. it does not have to be in a valid string format. E.g. 'Nov 2024'.
    """

    avatar_url: str
    """
    URL for the worker template\'s avatar. This would be the avatar shown in the marketplace for this worker as well 
    as the default avatar for worker instance when hired.
    """

    status: str
    """Status of this worker template. Supported values are: init, dev, live, paused."""

    init_setup_dur_hours: int
    """Initial technical setup duration in hours. This information is public."""

    init_setup_info: Optional[str]
    """
    General information about initial technical setup to be displayed on the resumé page. This may include additional 
    information that will be gathered, technical information, technical contacts or any other information pertaining to the 
    initial setup.
    """

    support_interview_mode: bool
    """Whether or not this worker supports interview mode."""

    auto_interview: Optional[bool]
    """
    If interview mode is supported, this flag indicates whether or not Humatron should provide auto-interview for this 
    build. In auto-interview mode Humatron will use build's resumé as a LLM context to automatically provide RAG-based 
    answers to interview questions without any communications with the build's implementation. 
    Note that this implementation is technically limited by what information is provided in build settings and its 
    external links.
    """

    interview_concurrent_sessions: Optional[int]
    """
    If interview mode is supported, this is the maximum number of the concurrent interview session supported. 
    This will be automatically enforced by Humatron.
    """

    interview_reqs_per_hour: Optional[int]
    """
    If interview mode is supported, this is the maximum number of questions that can be asked per hour in a single 
    interview session. This will be automatically enforced by Humatron.
    """

    interview_sla: Optional[str]
    """
    Optional description of SLA during the non-auto interview. Should contain any restriction or limitation 
    additionally to interview_reqs_per_hour and interview_concurrent_sessions settings.
    """

    role: str
    """
    Job title or a role of the worker, e.g. ' Sr. Software Engineer' or 'Social Content Manager'. 
    When hired, this will be a default job title.
    """

    overview: str
    """
    Overview or introduction of the worker capabilities, skills and features. 
    If the auto-interview mode is enabled, this is the main part that will be used as a RAG context for LLM answering 
    questions about this build. Text or Markdown with GitHub extensions are supported. 
    NOTE: embedded HTML is not supported.
    """

    share_summary: str
    """Short summary of the build used for sharing on social media."""

    skills_csv: str
    """
    Comma-separated list of this build main code skills. 
    It is shown on resume page and used bu auto-interview function, if enabled.
    """

    deploy_descr: str
    """Public information and necessary details about technical deployment of this build."""

    ai_stack_descr: str
    """Public information and technical details of ML/AI/GenAI stack for this build."""

    country_iso_3166_csv: Optional[str]
    """
    Comma-separated list of ISO 3166 country codes for country locations supported by this build. 
    During hiring, one of these locations will be selected.
    """

    lang_iso_639_csv: Optional[str]
    """
    Comma-separated list of ISO 639 language codes for languages supported by this worker. 
    During hiring, one of the languages will be selected as a primary language.
    """

    is_human_curated: bool
    """Whether or not this build supports human-in-the-loop curation."""

    builder_submit_person: Person
    """Person who originally submitted this build."""

    builder_support_person: Person
    """Official support person for this build. It will be used internally by Humatron only."""

    builder_org: Organization
    """Organization responsible for this build."""

    builder_descr_url: Optional[str]
    """
    Optional URL for the external description or information about this build provided by the builder. 
    If provided and auto-interview is enabled, this will be used as part of the RAG LLM context when answering 
    interview questions.
    """

    support_descr: str
    """Description of the support provided for this builds hired instances. This is a public information."""

    support_email: str
    """Public email that will be used as a support email for this build's hired instances."""

    is_private: bool
    """
    Whether or not this build is private, i.e. available for hire only for the organization that built it. 
    Non-private worker are available for hire to anyone.
    """

    api_endpoint: Optional[str]
    """Worker API endpoint for this build. Until this is set, the build will remain in 'init' status."""

    price_plan: PricePlan
    """Price plan for this build."""

    channels: list[Channel]
    """Specific channels for this specialist."""


class Instance(NamedTuple):
    """
    Represents an instance of a service, tied to a specialist and an organization.
    """

    id: int
    """Unique ID of this instance."""

    specialist: Specialist
    """Worker template (i.e. resume) for this worker instance."""

    org: Organization
    """Organization this worker instance was hired by."""

    status: str
    """
    Status of this instance. Can be one of the following values: init, confirmed, preparing, live, paused, terminated.
    """

    first_names: str
    """First name or technical nickname."""

    last_name: Optional[str]
    """Optional last name."""

    avatar_urls: str
    """URL for this instance avatar."""

    gender: str
    """This instance gender. This is used to resolve language grammar only. Supported values are: male, female."""

    age: str
    """
    Assigned age group. This is used for communication style adjustment. Supported values are: 20-30, 30-40, 40-50+.
    """

    country_name: str
    """Name of the country of residence as in ISO 3166."""

    country_iso_3166: str
    """Code of the country of residence as in ISO 3166-2."""

    city: str
    """City of residence. Should align with country and working time zone."""

    tz: str
    """Working time zone. Should align with country and city of residence."""

    primary_lang: str
    """Primary communication language."""

    comm_style: str
    """Communication style of this instance. Supported values are: informal+, informal, adaptive, formal, formal+."""

    lang_mode: str
    """Language mode of this instance. Supported values are: adaptive, plain."""

    work_type: str
    """Work type assigned to this instance. Supported values are: 24/7, 9-to-5."""

    workplace_persona: str
    """Workplace persona of this instance. Supported values are: visionary, networker, builder, mentor, researcher."""

    brevity: str
    """Brevity style of this instance. Supported values are: concise, adaptive, verbose."""

    job_title: str
    """Assigned job title."""

    job_descr: Optional[str]
    """Job description."""

    team: str
    """Name of team, business unit or organization this instance is part of."""

    pay_type: str
    """Payment type. Supported values: hourly, monthly."""

    hired_by_person: Person
    """Person who hired this worker instance."""

    reporting_to_person: Person
    """Person to whom this worker instance reports."""

    contact_person: Person
    """Employer technical contact person for this worker instance"""

    hire_ts: str
    """Timestamp of the hiring application submission, formatted in ISO-8601."""

    start_date: str
    """Start date timestamp, possible in the future, formatted in ISO-8601."""

    live_ts: Optional[str]
    """Timestamp of when this instance went live for the 1st time, formatted in ISO-8601."""

    termination_ts: Optional[str]
    """Termination timestamp, formatted in ISO-8601."""

    termination_reason: Optional[str]
    """Reason for termination."""


class RequestDataInterview(NamedTuple):
    """
    Represents the data payload for initiating an interview request.
    """

    payload_id: str
    """
    Unique ID of this payload object. Note that response payload will reference this ID in its ref_payload_id field.
    """

    ses_id: str
    """Unique ID of the interview session. Every time an new interview starts, it gets assigned a new session ID"""

    person: Person
    """Person conducting the interview."""

    org: Organization
    """Organization of the person conducting the interview."""

    specialist: Specialist
    """
    Specialist being interviewed. Note that there is no worker instance yet as the interview is conducted before hiring.
    """

    ref_resp_payload_id: Optional[str]
    """
    Optional ID of the response payload ID (see payload_id field on response payload). This field is only passed in 
    if kind field is equal to 'good_response' or 'bad_response'. In both case it references ID of the response payload 
    that user marked as "good" or "bad" accordingly in the interview chat window on Humatron website.
    """

    kind: str
    """Type of the interview request: start, stop, message, good_response, bad_response"""

    text: Optional[str]
    """Text of the user request message in interview mode. Only provided if kind field is equal to 'message'."""


class ResponseDataInterview(NamedTuple):
    """
    Represents the data payload for responding to an interview request.
    """

    resp_cmd: RequestType
    """Supported value: interview."""

    ses_id: str
    """ID of the interview session as it was passed in the request payload."""

    payload_id: str
    """
    Unique ID of this payload. This ID may be referenced (see ref_resp_payload_id field on request payload) 
    by the future interview requests with kind field equal to either 'good_response' or 'bad_response'
    """

    ref_payload_id: str
    """ID of the interview request payload object this response is responding to."""

    text: Optional[str]
    """
    Interview response message. It is only required if the request's kind field is equal to 'start' or 'message'. 
    Text or Markdown with GitHub extensions are supported. NOTE: embedded HTML is not supported
    """

    @classmethod
    def make(
        cls,
        ses_id: str,
        payload_id: str,
        ref_payload_id: str,
        text: Optional[str] = None
    ) -> 'ResponseDataInterview':
        """Factory method to create a `ResponseDataInterview` object."""
        return cls(RequestType.INTERVIEW, ses_id, payload_id, ref_payload_id, text)


class RequestDataHeartbeat(NamedTuple):
    """
    Represents the data payload for a heartbeat request to keep the instance active.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class RequestDataRegister(NamedTuple):
    """
    Represents the data payload for registering an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID. """

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataRegister(NamedTuple):
    """
    Represents the data payload for the response to a registration request.
    """

    resp_cmd: RequestType
    """Supported value: register."""

    instance_id: int
    """Worker instance ID."""

    ref_payload_id: str
    """ID of the register request payload object this response is responding to."""

    result: bool
    """true if successfully registered, false if not."""

    reject_code: Optional[int]
    """Provided if result is false. Supported values are: 
     - 100 - Undefined reason.
     - 200 - Legal or contractual reason.
     - 300 - System or technical reason.
     """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

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
        return cls(RequestType.REGISTER, instance_id, ref_payload_id, result, reject_code, contacts)


class RequestDataUnregister(NamedTuple):
    """
    Represents the data payload for unregistering an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID. """

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataUnregister(NamedTuple):
    """
    Represents the data payload for the response to an unregister request.
    """

    resp_cmd: RequestType
    """Supported value: unregister."""

    instance_id: int
    """Worker Instance ID."""

    ref_payload_id: str
    """ID of the unregister request payload object this response is responding to."""

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Not unique records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataUnregister':
        """Factory method to create a `ResponseDataUnregister` object."""
        return cls(RequestType.UNREGISTER, instance_id, ref_payload_id, contacts)


class RequestDataPause(NamedTuple):
    """
    Represents the data payload for pausing an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataPause(NamedTuple):
    """
    Represents the data payload for the response to a pause request.
    """

    resp_cmd: RequestType
    """Supported value: pause."""

    instance_id: int
    """Instance ID."""

    ref_payload_id: str
    """ID of the pause request payload object."""

    result: bool
    """true if successfully paused, false if not."""

    error_code: Optional[int]
    """
    Provided if result is false. Supported values are:
    - 100 - Undefined reason.
    - 200 - Legal or contractual reason.
    - 300 - System or technical reason.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

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
        return cls(RequestType.PAUSE, instance_id, ref_payload_id, result, error_code, contacts)


class RequestDataResume(NamedTuple):
    """
    Represents the data payload for resuming an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataResume(NamedTuple):
    """
    Represents the data payload for the response to a resume request.
    """

    resp_cmd: RequestType
    """Supported value: resume."""

    instance_id: int
    """Instance ID."""

    ref_payload_id: str
    """ID of the resumé request payload object this response is responding to."""

    result: bool
    """true if successfully resumed, false if not."""

    error_code: Optional[int]
    """
    Provided if result is false. Supported values are:
    - 100 - Undefined reason.
    - 200 - Legal or contractual reason.
    - 300 - System or technical reason.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

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
        return cls(RequestType.RESUME, instance_id, ref_payload_id, result, error_code, contacts)


class RequestMessageSlack(NamedTuple):
    """
    Represents the data payload for a Slack message.
    """

    body: Any
    """
    Slack 'message' event body. See more at U{Slack Events API body<https://api.slack.com/apis/connections/events-api>}.
    """

    conversation: Any
    """
    channel property from Slack 'conversations.info' method call result. 
    See more at U{Slack Conversations Request<https://api.slack.com/methods/conversations.info>}.
    """

    conversation_users: list[Any]
    """
    Array of user property objects from Slack 'users.info' method call results. 
    See more at U{Slack Users Request<https://api.slack.com/methods/users.info>}. 
    """

    files: Optional[list[File]]
    """Files transferred with the message."""


class RequestMessageEmail(NamedTuple):
    """
    Represents the data payload for an email.
    """

    sender: str
    """Sender email address."""

    to: str
    """Comma separated list of recipient email addresses."""

    reply_to: Optional[str]
    """Comma separated list of reply-to email addresses."""

    subj: Optional[str]
    """Email subject."""

    cc: Optional[str]
    """Comma separated list of CC email addresses."""

    bcc: Optional[str]
    """Comma separated list of BCC email addresses."""

    html: Optional[str]
    """HTML email content. Has higher priority than plain text content. Either text or html field should be set."""

    text: Optional[str]
    """Plain text email content. Either text or html field should be set."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Records should be unique, duplicates will be skipped."""


class RequestMessageSms(NamedTuple):
    """
    Represents the data payload for an SMS message.
    """

    sender: str
    """Sender phone number."""

    receiver: str
    """Receiver phone number."""

    text: str
    """Plain text content of the SMS."""


class RequestMessageRest(NamedTuple):
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
    Represents the data payload for sending a message (slack, email, SMS or rest).
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""

    resource_id: int
    """ID of the resource that delivered this message."""

    message: Union[RequestMessageSlack, RequestMessageEmail, RequestMessageSms, RequestMessageRest]
    """
    Structure of this object depends on channel_type property of the resource that delivered this message. 
    ID of the resource that delivered this message is in resource_id field. 
    All resources assigned to this worker instance are available in resources field.
    """


class ResponseMessageSlack(NamedTuple):
    """
    Represents the data payload for the response to a Slack message request.
    """

    channel: str
    """Slack channel ID."""

    text: Optional[str]
    """Slack message text."""

    thread_ts: Optional[str]
    """Slack thread timestamp field. It is used for thread replies."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Not unique records will be skipped."""

    @classmethod
    def make(
        cls,
        channel: str,
        text: Optional[str] = None,
        thread_ts: Optional[str] = None,
        files: Optional[list[File]] = None
    ) -> 'ResponseMessageSlack':
        """Factory method to create a `ResponseDataSlack` object."""
        if not text and not files:
            raise ValueError('Either text or files must be provided.')
        return cls(channel, text, thread_ts, files)


class ResponseMessageEmail(NamedTuple):
    """
    Represents the data payload for the response to an email request.
    """

    sender: str
    """Sender email address. It is configured resource email."""

    to: str
    """Comma separated list of recipient email addresses."""

    reply_to: Optional[str]
    """Comma separated list of reply-to email addresses."""

    subj: Optional[str]
    """Subject of the email."""

    cc: Optional[str]
    """Comma separated list of CC email addresses."""

    bcc: Optional[str]
    """Comma separated list of BCC email addresses."""

    html: Optional[str]
    """
    HTML email content. Either text or HTML content must be provided. 
    HTML content has higher priority than plain text if both are provided.
    """

    text: Optional[str]
    """Plain text email content. Either text or HTML content must be provided."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Not unique records will be skipped."""

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
    ) -> 'ResponseMessageEmail':
        """Factory method to create a `ResponseDataEmail` object."""
        if not text and not html and not files:
            raise ValueError('Either text, html or files must be provided.')
        return cls(sender, to, reply_to, subj, cc, bcc, html, text, files)


class ResponseMessageSms(NamedTuple):
    """
    Represents the data payload for the response to an SMS request.
    """

    sender: str
    """Sender phone number."""

    receiver: str
    """Receiver phone number."""

    text: str
    """Plain text SMS content."""

    @classmethod
    def make(
        cls,
        sender: str,
        receiver: str,
        text: str
    ) -> 'ResponseMessageSms':
        """Factory method to create a `ResponseDataSms` object."""
        return cls(sender, receiver, text)


class ResponseMessageRest(NamedTuple):
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
    ) -> 'ResponseMessageRest':
        """Factory method to create a `ResponseDataRest` object."""
        return cls(sender, receiver, text)


class ResponseDataMessage(NamedTuple):
    """
    Represents the data payload for the response to a message request (slack, email, SMS or rest).
    """

    resp_cmd: RequestType
    """Supported value: message."""

    instance_id: int
    """Instance ID."""

    resource_id: int
    """ID of the resource that should be used to deliver the message in this payload."""

    message: Union[ResponseMessageSlack, ResponseMessageEmail, ResponseMessageSms, ResponseMessageRest]
    """
    Content depends on channel_type field value of the resource object specified in this payload. 
    The resource is provided by its ID in resource_id field.
    """

    ref_payload_id: Optional[str]
    """
    Optional ID of the message request payload object this response is responding to. Note that new messages from worker 
    instance may be unrelated to any previous request payloads, hence this field is optional. This is an essence 
    of autonomous work capabilities when AI worker can communicate with the outside world spontaneously "on its own".
    """

    translate_lang: Optional[str]
    """
    Optional language to translate the message to. Language should be specified as ISO 3166-2 code and 
    be one of the supported by the worker.
    """

    tone_shifting: Optional[str]
    """
    Default value is true. Message will be rewritten according on the overall social and communication preferences 
    for this worker instance. Various social and communication properties are available via instance object. 
    Note that all social and communication preferences in combination play a role in how message will be rewritten. 
    Some of them have a short-term impact, some provide an effect during a long conversation only, and some, 
    like gender, only affect the language grammar.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Not unique records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        resource_id: int,
        message: Union[ResponseMessageSlack, ResponseMessageEmail, ResponseMessageSms, ResponseMessageRest],
        ref_payload_id: Optional[str] = None,
        translate_lang: Optional[str] = None,
        tone_shifting: Optional[str] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataMessage':
        """Factory method to create a `ResponseDataMessage` object."""
        return cls(
            RequestType.MESSAGE, instance_id, resource_id, message, ref_payload_id, translate_lang, tone_shifting,
            contacts
        )


RequestPayloadPartBody = Union[
    RequestDataInterview,
    RequestDataHeartbeat,
    RequestDataRegister,
    RequestDataUnregister,
    RequestDataPause,
    RequestDataResume,
    RequestDataMessage
]
"""Request payload part body type alias."""

ResponsePayloadPartBody = Union[
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

    req_cmd: RequestType
    """The command associated with the request."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp when the request was created in ISO format."""
    payload: list[RequestPayloadPartBody]
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
        return cls(RequestType(d['req_cmd']), d['req_id'], d['req_tstamp'], d['payload'], d.get('storage'))


class Response(NamedTuple):
    """
    Represents a Humatron response with a unique ID, timestamp, optional payload, and optional storage.
    """

    resp_id: str
    """The unique identifier for the response."""
    resp_tstamp: str
    """The timestamp when the response was created in ISO format."""
    payload: Optional[list[ResponsePayloadPartBody]]
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

    req_cmd: RequestType
    """The command associated with the payload part."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp of the request."""
    body: RequestPayloadPartBody
    """An object representing a part body of the request payload."""


ResponsePayloadPart = Union[list[ResponsePayloadPartBody], ResponsePayloadPartBody, None]
"""Response payload part alias."""


class HumatronWorkerApi(ABC):
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


class HumatronAsyncWorker(HumatronWorkerApi, ABC):
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
        if req.req_cmd == RequestType.INTERVIEW:
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
