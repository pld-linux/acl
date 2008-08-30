Summary:	Command and library for manipulating access control lists
Summary(pl.UTF-8):	Polecenie i biblioteka do manipulacji listami kontroli dostępu (ACL)
Name:		acl
Version:	2.2.47
Release:	2
License:	LGPL v2+ (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://linux-xfs.sgi.com/projects/xfs/cmd_tars/%{name}_%{version}-1.tar.gz
# Source0-md5:	a11e4571a54a0b1ae83010d1e68a64c2
Patch0:		%{name}-miscfix.patch
Patch1:		%{name}-lt.patch
Patch2:		%{name}-LDFLAGS.patch
Patch3:		%{name}-pl.po-update.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	attr-devel >= 2.4.16-3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
Requires:	attr >= 2.4.15
Obsoletes:	libacl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_libdir		/%{_lib}
%define		_libexecdir	/usr/%{_lib}

%description
A command (chacl) and a library (libacl) to manipulate POSIX access
control lists under Linux.

%description -l pl.UTF-8
Polecenie (chacl) i biblioteka (libacl) do manipulowania zgodnymi z
POSIX listami kontroli dostępu (ACL) pod Linuksem.

%package devel
Summary:	Header files for acl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki acl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	attr-devel >= 2.4.16-3

%description devel
Header files to develop software which manipulate access control
lists.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do rozwoju oprogramowania manipulującego
listami kontroli dostępu (ACL).

%package static
Summary:	Static acl library
Summary(pl.UTF-8):	Statyczna biblioteka acl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static acl library.

%description static -l pl.UTF-8
Statyczna biblioteka acl.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -f aclocal.m4

%build
mv install-sh install-custom-sh
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
mv install-custom-sh install-sh
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags} -DENABLE_GETTEXT"

%{__make} \
	LLDFLAGS="%{rpmldflags}" \
	top_builddir="../"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/acl,%{_mandir}/man3}

export DIST_ROOT=$RPM_BUILD_ROOT
P=$(pwd)
DIST_INSTALL=$P/install.manifest
DIST_INSTALL_DEV=$P/install-dev.manifest
DIST_INSTALL_LIB=$P/install-lib.manifest

%{__make} install \
	DIST_MANIFEST=$DIST_INSTALL \
	top_builddir="../"
%{__make} install-dev \
	DIST_MANIFEST=$DIST_INSTALL_DEV \
	top_builddir="../"
%{__make} install-lib \
	DIST_MANIFEST=$DIST_INSTALL_LIB \
	top_builddir="../"

rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_copy_int,acl_set_fd,acl_set_file}.3
rm -f	$RPM_BUILD_ROOT%{_mandir}/man3/{acl_to_short_text,acl_to_text}.3
echo ".so acl_copy_ext.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_copy_int.3
echo ".so acl_get_fd.3"		> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_fd.3
echo ".so acl_get_file.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_set_file.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_short_text.3
echo ".so acl_from_text.3"	> $RPM_BUILD_ROOT%{_mandir}/man3/acl_to_text.3

#rm -f $RPM_BUILD_ROOT%{_libexecdir}/lib*.so
ln -snf %{_libdir}/$(basename $RPM_BUILD_ROOT%{_libdir}/libacl.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libexecdir}/libacl.so
%{__sed} -i "s|libdir='%{_libdir}'|libdir='%{_libexecdir}'|" \
	$RPM_BUILD_ROOT%{_libexecdir}/libacl.la

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

# already in /usr
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.{so,la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/{CHANGES,TODO}
%attr(755,root,root) %{_bindir}/chacl
%attr(755,root,root) %{_bindir}/getfacl
%attr(755,root,root) %{_bindir}/setfacl
%attr(755,root,root) %{_libdir}/libacl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libacl.so.1
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files devel
%defattr(644,root,root,755)
%doc doc/{extensions.txt,libacl.txt}
%attr(755,root,root) %{_libexecdir}/libacl.so
%{_libexecdir}/libacl.la
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_mandir}/man3/acl_*.3*

%files static
%defattr(644,root,root,755)
%{_libexecdir}/libacl.a
