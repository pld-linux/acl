Summary:	Advanced Color Logs
Summary(pl):	Advanced Color Logs - program koloruj±cy logi
Name:		acl
Version:	0.6.0
Release:	1
Group:		Utilities/Console
Group(pl):	Narzêdzia/Konsola
Copyright:	GPL
Source:		http://spyjurenet.com/linuxrc.org/projects/acl/%{name}-%{version}.tar.gz
Patch:		acl-config.patch
URL:		http://spyjurenet.com/linuxrc.org/projects/acl/
Requires:	perl
BuildArch:	noarch
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
acl is a perl script that colorizes system logs. Inspired by ColorLogs, 
acl (Advanced Color Logs) has advanced parsing capabilities.

%description -l pl
acl to skrypt napisany w perlu, koloruj±cy logi systemowe. Zainspirowany
programem ColorLogs, acl (Advanced Color Logs) posiada bardziej rozbudowane
mo¿liwo¶ci parsowania.

%prep
%setup -q
%patch -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc}

install acl.pl   $RPM_BUILD_ROOT%{_bindir}/acl
install acl.conf $RPM_BUILD_ROOT/etc

gzip -9nf README NEWS TODO 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,TODO}.gz
%attr(755,root,root) %{_bindir}/acl
%config(noreplace) %verify(not size mtime md5) /etc/acl.conf
