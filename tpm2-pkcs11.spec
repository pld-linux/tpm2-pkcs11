#
# Conditional build:
%bcond_without	python		# CPython 3.x module and tpm2_ptool
%bcond_with	tests		# unit/integration tests

Summary:	OSS implementation of the TCG TPM2 Software Stack (TSS2)
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja TCG TPM2 Software Stack (TSS2)
Name:		tpm2-pkcs11
Version:	1.8.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/tpm2-software/tpm2-pkcs11/releases
Source0:	https://github.com/tpm2-software/tpm2-pkcs11/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b5551af45f3941153c8327164e2746b2
Patch0:		%{name}-ac.patch
URL:		https://github.com/tpm2-software/tpm2-pkcs11
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	p11-kit-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tpm2-tss-devel >= 3.2
BuildRequires:	yaml-devel
%if %{with python}
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-setuptools
%endif
%if %{with tests}
BuildRequires:	expect
# p11tool
BuildRequires:	gnutls
# ss
BuildRequires:	iproute2
BuildRequires:	jdk
# certutil, modutil
BuildRequires:	nss-tools
# pkcs11-tool
BuildRequires:	opensc
BuildRequires:	sqlite3
# or ibmswtpm2
BuildRequires:	swtpm
BuildRequires:	tpm2-tools
BuildRequires:	tpm2-abrmd
# tpm2tss-genkey, tss2_provision
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS).

%description -l pl.UTF-8
Implementacja specyfikacji TPM2 Software Stack (TSS), stworzonej przez
Trusted Computing Group (TCG).

%package devel
Summary:	Header files for tpm2-pkcs11
Summary(pl.UTF-8):	Pliki nagłówkowe do tpm2-pkcs11
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Requires:	tpm2-tss-devel

%description devel
Header files for implementation of the Trusted Computing Group's (TCG)
TPM2 Software Stack (TSS).

%description devel -l pl.UTF-8
Pliki nagłówkowe implementacji Trusted Computing Group (TCG) TPM2
Software Stack (TSS).

%package -n python3-tpm2-pkcs11
Summary:	Command line tools for the TPM2.0 PKCS11 module
Summary(pl.UTF-8):	Narzędzia linii poleceń do modułu PKCS11 TPM2.0
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-tpm2-pkcs11
This tool is used to configure and manipulate stores for the
tpm2-pkcs11 cryptographic library.

%description -n python3-tpm2-pkcs11 -l pl.UTF-8
To narzędzie służy do konfiguracji i operowania na danych
przechowywanych przez bibliotekę kryptograficzną tpm2-pkcs11.

%prep
%setup -q
%patch0 -p1

# set VERSION properly when there is no .git directory
%{__sed} -i -e 's/m4_esyscmd_s(\[git describe --tags --always --dirty\])/%{version}/' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_tests:--enable-integration} \
	--disable-ptool-checks \
	--disable-silent-rules
	%{?with_tests:--enable-unit}

%{__make}

%if %{with tests}
%{__make} check
%endif

%if %{with python}
cd tools
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pkcs11/libtpm2_pkcs11.la

%if %{with python}
cd tools
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE docs/{ARCHITECTURE,DB_UPGRADE,EAP-TLS,FAPI,INITIALIZING,INTEROPERABILITY,OPENSSL,OPENVPN,P11,PKCS11_TOOL,README,SSH,SSH_HOSTKEYS,tpm2-pkcs11_object_auth_model}.md
%attr(755,root,root) %{_libdir}/pkcs11/libtpm2_pkcs11.so.*
%{_datadir}/p11-kit/modules/tpm2_pkcs11.module

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pkcs11/libtpm2_pkcs11.so
%{_pkgconfigdir}/tpm2-pkcs11.pc

%files -n python3-tpm2-pkcs11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tpm2_ptool
%{py3_sitescriptdir}/tpm2_pkcs11
%{py3_sitescriptdir}/tpm2_pkcs11_tools-1.33.7-py*.egg-info
