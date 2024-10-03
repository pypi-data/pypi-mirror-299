# Copyright: (c) 2023 Jordan Borean (@jborean93) <jborean93@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import annotations

import collections
import enum

from libc.stdint cimport uint64_t

from ._text cimport WideCharString, wide_char_to_str
from ._win32_types cimport *


cdef extern from "python_sspi.h":
    unsigned int _SECPKG_CRED_INBOUND "SECPKG_CRED_INBOUND"
    unsigned int _SECPKG_CRED_OUTBOUND "SECPKG_CRED_OUTBOUND"
    unsigned int _SECPKG_CRED_BOTH "SECPKG_CRED_BOTH"
    unsigned int _SECPKG_CRED_AUTOLOGON_RESTRICTED "SECPKG_CRED_AUTOLOGON_RESTRICTED"
    unsigned int _SECPKG_CRED_PROCESS_POLICY_ONLY "SECPKG_CRED_PROCESS_POLICY_ONLY"

    unsigned int _SEC_WINNT_AUTH_IDENTITY_ANSI "SEC_WINNT_AUTH_IDENTITY_ANSI"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_UNICODE "SEC_WINNT_AUTH_IDENTITY_UNICODE"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_MARSHALLED "SEC_WINNT_AUTH_IDENTITY_MARSHALLED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_ONLY "SEC_WINNT_AUTH_IDENTITY_ONLY"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_PROCESS_ENCRYPTED "SEC_WINNT_AUTH_IDENTITY_FLAGS_PROCESS_ENCRYPTED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_PROTECTED "SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_PROTECTED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_USER_PROTECTED "SEC_WINNT_AUTH_IDENTITY_FLAGS_USER_PROTECTED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_ENCRYPTED "SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_ENCRYPTED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_RESERVED "SEC_WINNT_AUTH_IDENTITY_FLAGS_RESERVED"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_USER "SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_USER"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_DOMAIN "SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_DOMAIN"
    unsigned int _SEC_WINNT_AUTH_IDENTITY_FLAGS_ID_PROVIDER "SEC_WINNT_AUTH_IDENTITY_FLAGS_ID_PROVIDER"

    unsigned int SEC_WINNT_AUTH_IDENTITY_VERSION
    unsigned int SEC_WINNT_AUTH_IDENTITY_VERSION_2

    cdef struct _SEC_WINNT_AUTH_IDENTITY_EXW:
        unsigned int Version;
        unsigned int Length;
        unsigned short *User;
        unsigned int UserLength;
        unsigned short *Domain;
        unsigned int DomainLength;
        unsigned short *Password;
        unsigned int PasswordLength;
        unsigned int Flags;
        unsigned short *PackageList;
        unsigned int PackageListLength;
    ctypedef _SEC_WINNT_AUTH_IDENTITY_EXW SEC_WINNT_AUTH_IDENTITY_EXW
    ctypedef SEC_WINNT_AUTH_IDENTITY_EXW *PSEC_WINNT_AUTH_IDENTITY_EXW

    ctypedef void (*SEC_GET_KEY_FN)(
        void *Arg,
        void *Principal,
        unsigned int KeyVer,
        void **Key,
        SECURITY_STATUS *Status,
    )

    # https://learn.microsoft.com/en-us/windows/win32/api/sspi/nf-sspi-acquirecredentialshandlew
    SECURITY_STATUS AcquireCredentialsHandleW(
        LPWSTR         pPrincipal,
        LPWSTR         pPackage,
        unsigned int  fCredentialUse,
        void           *pvLogonId,
        void           *pAuthData,
        SEC_GET_KEY_FN pGetKeyFn,
        void           *pvGetKeyArgument,
        PCredHandle    phCredential,
        PTimeStamp     ptsExpiry
    ) nogil

    # https://learn.microsoft.com/en-us/windows/win32/api/sspi/nf-sspi-freecredentialshandle
    SECURITY_STATUS FreeCredentialsHandle(
        PCredHandle phCredential
    ) nogil

class CredentialUse(enum.IntFlag):
    SECPKG_CRED_INBOUND = _SECPKG_CRED_INBOUND
    SECPKG_CRED_OUTBOUND = _SECPKG_CRED_OUTBOUND
    SECPKG_CRED_BOTH = _SECPKG_CRED_BOTH
    SECPKG_CRED_AUTOLOGON_RESTRICTED = _SECPKG_CRED_AUTOLOGON_RESTRICTED
    SECPKG_CRED_PROCESS_POLICY_ONLY = _SECPKG_CRED_PROCESS_POLICY_ONLY

class WinNTAuthFlags(enum.IntFlag):
    SEC_WINNT_AUTH_IDENTITY_ANSI = _SEC_WINNT_AUTH_IDENTITY_ANSI
    SEC_WINNT_AUTH_IDENTITY_UNICODE = _SEC_WINNT_AUTH_IDENTITY_UNICODE
    SEC_WINNT_AUTH_IDENTITY_MARSHALLED = _SEC_WINNT_AUTH_IDENTITY_MARSHALLED
    SEC_WINNT_AUTH_IDENTITY_ONLY = _SEC_WINNT_AUTH_IDENTITY_ONLY
    SEC_WINNT_AUTH_IDENTITY_FLAGS_PROCESS_ENCRYPTED = _SEC_WINNT_AUTH_IDENTITY_FLAGS_PROCESS_ENCRYPTED
    SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_PROTECTED = _SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_PROTECTED
    SEC_WINNT_AUTH_IDENTITY_FLAGS_USER_PROTECTED = _SEC_WINNT_AUTH_IDENTITY_FLAGS_USER_PROTECTED
    SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_ENCRYPTED = _SEC_WINNT_AUTH_IDENTITY_FLAGS_SYSTEM_ENCRYPTED
    SEC_WINNT_AUTH_IDENTITY_FLAGS_RESERVED = _SEC_WINNT_AUTH_IDENTITY_FLAGS_RESERVED
    SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_USER = _SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_USER
    SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_DOMAIN = _SEC_WINNT_AUTH_IDENTITY_FLAGS_NULL_DOMAIN
    SEC_WINNT_AUTH_IDENTITY_FLAGS_ID_PROVIDER = _SEC_WINNT_AUTH_IDENTITY_FLAGS_ID_PROVIDER

cdef class CredHandle:
    # cdef _CredHandle raw
    # cdef int needs_free

    def __dealloc__(CredHandle self):
        if self.needs_free:
            FreeCredentialsHandle(&self.raw)
            self.needs_free = 0

cdef class AuthIdentity:

    cdef void *__c_value__(AuthIdentity self):
        return NULL

cdef class WinNTAuthIdentity(AuthIdentity):
    cdef SEC_WINNT_AUTH_IDENTITY_EXW raw
    cdef WideCharString username_wchar
    cdef WideCharString domain_wchar
    cdef WideCharString password_wchar
    cdef WideCharString package_list_wchar

    def __cinit__(
        WinNTAuthIdentity self,
        username: str | None = None,
        domain: str | None = None,
        password: str | None = None,
        *,
        flags: WinNTAuthFlags | int = 0,
        package_list: str | None = None,
    ) -> None:
        self.raw.Version = SEC_WINNT_AUTH_IDENTITY_VERSION
        self.raw.Length = <unsigned int>sizeof(SEC_WINNT_AUTH_IDENTITY_EXW)

        self.username_wchar = WideCharString(username)
        self.raw.User = <unsigned short*>self.username_wchar.raw
        self.raw.UserLength = <unsigned int>self.username_wchar.length

        self.domain_wchar = WideCharString(domain)
        self.raw.Domain = <unsigned short*>self.domain_wchar.raw
        self.raw.DomainLength = <unsigned int>self.domain_wchar.length

        self.password_wchar = WideCharString(password)
        self.raw.Password = <unsigned short*>self.password_wchar.raw
        self.raw.PasswordLength = <unsigned int>self.password_wchar.length

        self.raw.Flags = int(flags) | _SEC_WINNT_AUTH_IDENTITY_UNICODE

        self.package_list_wchar = WideCharString(package_list)
        self.raw.PackageList = <unsigned short*>self.package_list_wchar.raw
        self.raw.PackageListLength = <unsigned int>self.package_list_wchar.length

    cdef void *__c_value__(WinNTAuthIdentity self):
        return &self.raw

    def __repr__(WinNTAuthIdentity self) -> str:
        kwargs = [f"{k}={v}" for k, v in {
            'username': repr(self.username),
            'domain': repr(self.domain),
            'password': repr(self.password),
            'flags': self.flags,
            'package_list': repr(self.package_list),
        }.items()]

        return f"WinNTAuthIdentity({', '.join(kwargs)})"

    def __str__(WinNTAuthIdentity self) -> str:
        username = self.username
        if self.domain:
            username = f"{self.domain}\\{username}"

        return username

    @property
    def username(self) -> str | None:
        return wide_char_to_str(<LPWSTR>self.raw.User, self.raw.UserLength)

    @property
    def domain(self) -> str | None:
        return wide_char_to_str(<LPWSTR>self.raw.Domain, self.raw.DomainLength)

    @property
    def password(self) -> str | None:
        return wide_char_to_str(<LPWSTR>self.raw.Password, self.raw.PasswordLength)

    @property
    def flags(self) -> WinNTAuthFlags:
        return WinNTAuthFlags(self.raw.Flags)

    @property
    def package_list(self) -> str | None:
        return wide_char_to_str(<LPWSTR>self.raw.PackageList, self.raw.PackageListLength)

AcquireCredentialsResult = collections.namedtuple(
    'AcquireCredentialsResult',
    ['credential', 'expiry'],
)

def acquire_credentials_handle(
    str principal,
    str package not None,
    unsigned int credential_use,
    *,
    AuthIdentity auth_data = None,
) -> AcquireCredentialsResult:
    cdef CredHandle cred = CredHandle()
    cdef WideCharString principal_wstr = WideCharString(principal)
    cdef WideCharString package_wstr = WideCharString(package)
    cdef void *auth_data_buffer = NULL
    cdef TimeStamp raw_expiry

    if auth_data is not None:
        auth_data_buffer = auth_data.__c_value__()

    with nogil:
        res = AcquireCredentialsHandleW(
            principal_wstr.raw,
            package_wstr.raw,
            credential_use,
            NULL,
            auth_data_buffer,
            NULL,
            NULL,
            &cred.raw,
            &raw_expiry
        )

    if res != 0:
        PyErr_SetFromWindowsErr(res)

    cred.needs_free = 1

    return AcquireCredentialsResult(
        credential=cred,
        expiry=(<uint64_t>raw_expiry.HighPart << 32) | raw_expiry.LowPart,
    )

def _replace_cred_handle(
    CredHandle src not None,
    CredHandle dst not None,
) -> None:
    # This is only used by sspilib._credential.py to store the cred state in
    # itself.
    dst.raw = src.raw
    dst.needs_free = src.needs_free
    src.needs_free = 0
