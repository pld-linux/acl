Summary:	Command for manipulating access control lists
Summary(pl):	Komenda do manipulacji listami kontroli dostêpu (ACL)
Name:		acl
Version:	1.0.1
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_bindir	/bin

%description
A command (chacl) to manipulate POSIX access control lists under
Linux.

%description -l pl
Komenda (chacl) do manipulowania zgodnymi z POSIX listami kontroli
dostêpu (ACL) pod Linuxem.

%package devel
Summary:	Header files and libraries to manipulate acls
Summary(pl):	Pliki nag³ówkowe i biblioteki do manipulacji ACLami
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki

%description devel
Header files and libraries to develop software which manipulate access
control lists.

%description -l pl devel
Pliki nag³ówkowe i biblioteki potrzebne do rozwoju oprogramowania
manipuluj±cego listami kontroli dostêpu (ACL).

%prep
%setup  -q
%patch0 -p1

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
autoconf
%configure 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV 
%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_copy_int,acl_set_fd,acl_set_file}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_to_short_text,acl_to_text}.3
echo ".so man3/acl_copy_ext.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_copy_int.3
echo ".so man3/acl_get_fd.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_fd.3
echo ".so man3/acl_get_file.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_file.3
echo ".so man3/acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_short_text.3
echo ".so man3/acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_text.3

gzip -9nf doc/CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_includedir}/acl
%{_mandir}/man[235]/*
