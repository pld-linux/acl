Summary:	Advanced Color Logs
Summary(pl):	Advanced Color Logs - program kolorujący logi
Name:		acl
Version:	0.7.0
Release:	1
License:	GPL
Group:		Utilities/Console
Group(pl):	Narzędzia/Konsola
Source0:	http://spyjurenet.com/linuxrc.org/projects/acl/%{name}-%{version}.tar.gz
Patch0:		acl-config.patch
URL:		http://spyjurenet.com/linuxrc.org/projects/acl/
Requires:	perl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acl is a perl script that colorizes system logs. Inspired by
ColorLogs, acl (Advanced Color Logs) has advanced parsing
capabilities.

%description -l pl
acl to skrypt napisany w perlu, kolorujący logi systemowe.
Zainspirowany programem ColorLogs, acl (Advanced Color Logs) posiada
bardziej rozbudowane możliwości parsowania.

%prep
%setup -q
%patch -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}}

install acl.pl   $RPM_BUILD_ROOT%{_bindir}/acl
install acl.conf $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf README NEWS TODO 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,TODO}.gz
%attr(755,root,root) %{_bindir}/acl
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/acl.conf
