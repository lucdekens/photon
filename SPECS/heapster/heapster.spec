Summary:	Heapster enables Container Cluster Monitoring and Performance Analysis.
Name:		heapster
Version:    1.5.4
Release:    2%{?dist}
License:	Apache 2.0
URL:		https://github.com/wavefrontHQ/cadvisor
Source0:	https://github.com/kubernetes/heapster/archive/%{name}-%{version}.tar.gz
%define sha1 heapster=102b8f21ecebc695987701b1d97f87dda1ea5645
Patch0:         go-27704.patch
Patch1:         go-27842.patch
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  go
BuildRequires:  unzip

%description
Heapster collects and interprets various signals like compute resource usage, lifecycle events, etc, and exports cluster metrics via REST endpoints.

%prep
%setup -q

pushd vendor/golang.org/x/net
%patch0 -p1
%patch1 -p1
popd

%build
mkdir -p $GOPATH/src/k8s.io/heapster
cp -r . $GOPATH/src/k8s.io/heapster
cd $GOPATH/src/k8s.io/heapster
make build

%install
cd $GOPATH/src/k8s.io/heapster
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 heapster %{buildroot}%{_bindir}
install -p -m 0755 eventer %{buildroot}%{_bindir}

%check
cd $GOPATH/src/k8s.io/heapster
make test-unit

%files
%defattr(-,root,root)
%{_bindir}/heapster
%{_bindir}/eventer

%changelog
*   Mon Jan 28 2019 Bo Gan <ganb@vmware.com> 1.5.4-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.5.4-1
-   Update to version 1.5.4
*   Thu Aug 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.2-1
-   Initial heapster package
