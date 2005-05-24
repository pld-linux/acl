Summary:	Command and library for manipulating access control lists
Summary(pl):	Polecenie i biblioteka do manipulacji listami kontroli dostêpu (ACL)
Name:		acl
Version:	2.2.28
Release:	1
License:	LGPL v2+ (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
# Source0-md5:	69ba4f7e2bb87d20aedd15249f8747eb
Patch0:		%{name}-miscfix.patch
Patch1:		%{name}-lt.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	attr-devel >= 2.4.16-3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	sed >= 4.0
Requires:	attr >= 2.4.15
Obsoletes:	libacl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_libdir		/%{_lib}
%define		_libexecdir	/usr/%{_lib}

%description
A command (chacl) and a library (libacl) to manipulate POSIX access
control lists under Linux.

%description -l pl
Polecenie (chacl) i biblioteka (libacl) do manipulowania zgodnymi z
POSIX listami kontroli dostêpu (ACL) pod Linuksem.

%package devel
Summary:	Header files for acl library
Summary(pl):	Pliki nag³ówkowe biblioteki acl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	attr-devel >= 2.4.16-3

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
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static acl library.

%description static -l pl
Statyczna biblioteka acl.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f aclocal.m4
%{__aclocal} -I m4
%{__autoconf}
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags} -DENABLE_GETTEXT"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/acl,%{_mandir}/man3}

DIST_ROOT=$RPM_BUILD_ROOT
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB

%{__make} install \
	DIST_MANIFEST=$DIST_INSTALL
%{__make} install-dev \
	DIST_MANIFEST=$DIST_INSTALL_DEV
%{__make} install-lib \
	DIST_MANIFEST=$DIST_INSTALL_LIB

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_copy_int,acl_set_fd,acl_set_file}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_to_short_text,acl_to_text}.3
echo ".so acl_copy_ext.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_copy_int.3
echo ".so acl_get_fd.3"		> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_fd.3
echo ".so acl_get_file.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_file.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_short_text.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_text.3

rm -f $RPM_BUILD_ROOT%{_libexecdir}/lib*.so
ln -sf %{_libdir}/$(cd $RPM_BUILD_ROOT%{_libdir} ; echo libacl.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libexecdir}/libacl.so
%{__sed} -i "s|libdir='%{_libdir}'|libdir='%{_libexecdir}'|" \
	$RPM_BUILD_ROOT%{_libexecdir}/libacl.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/{CHANGES,TODO}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man[15]/*

%files devel
%defattr(644,root,root,755)
%doc doc/{extensions.txt,libacl.txt}
%attr(755,root,root) %{_libexecdir}/lib*.so
%{_libexecdir}/lib*.la
%{_includedir}/acl
%{_includedir}/sys/*
%{_mandir}/man[23]/*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/lib*.a
