Summary:	Command for manipulating access control lists
Summary(pl):	Komenda do manipulacji listami kontroli dostêpu (ACL)
Name:		acl
Version:	2.1.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-miscfix.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	autoconf
BuildRequires:	attr-devel >= 2.0.0
Requires:	attr
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_libdir		/lib
%define		_libexecdir	/usr/lib

%description
A command (chacl) to manipulate POSIX access control lists under
Linux.

%description -l pl
Komenda (chacl) do manipulowania zgodnymi z POSIX listami kontroli
dostêpu (ACL) pod Linuksem.

%package devel
Summary:	Header files for acl library
Summary(pl):	Pliki nag³ówkowe biblioteki acl
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files to develop software which manipulate access control
lists.

%description devel -l pl
Pliki nag³ówkowe potrzebne do rozwoju oprogramowania manipuluj±cego
listami kontroli dostêpu (ACL).

%package static
Summary:	Static acl library
Summary(pl):	Statyczna biblioteka acl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static acl library.

%description static -l pl
Statyczna biblioteka acl.

%prep
%setup  -q
%patch0 -p1

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/acl

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
%{__make} install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_copy_int,acl_set_fd,acl_set_file}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_to_short_text,acl_to_text}.3
echo ".so acl_copy_ext.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_copy_int.3
echo ".so acl_get_fd.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_fd.3
echo ".so acl_get_file.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_file.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_short_text.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_text.3

rm -f $RPM_BUILD_ROOT%{_libexecdir}/lib*.so
ln -sf %{_libdir}/libacl.so.1.0.2 $RPM_BUILD_ROOT%{_libexecdir}/libacl.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/CHANGES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_libexecdir}/lib*.la
%attr(755,root,root) %{_libexecdir}/lib*.so
%{_includedir}/acl
%{_includedir}/sys/*
%{_mandir}/man[235]/*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/lib*.a
