Summary:	Command and library for manipulating access control lists
Summary(pl.UTF-8):	Polecenie i biblioteka do manipulacji listami kontroli dostępu (ACL)
Name:		acl
Version:	2.2.53
Release:	1
License:	LGPL v2+ (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	http://git.savannah.gnu.org/cgit/acl.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	0c72e292be55ac60e890c00e6c561af8
Patch0:		%{name}-pl.po-update.patch
URL:		http://savannah.nongnu.org/projects/acl/
BuildRequires:	attr-devel >= 2.4.16-3
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.18.2
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.402
BuildRequires:	sed >= 4.0
Requires:	attr >= 2.4.15
Obsoletes:	libacl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

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

# prepare for gettextize
%{__sed} -i -e 's,po/Makefile\.in,,' configure.ac

%build
po/update-potfiles
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libacl.so.* $RPM_BUILD_ROOT/%{_lib}
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libacl.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libacl.so

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

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
%attr(755,root,root) /%{_lib}/libacl.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libacl.so.1
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files devel
%defattr(644,root,root,755)
%doc doc/{extensions.txt,libacl.txt}
%attr(755,root,root) %{_libdir}/libacl.so
%{_libdir}/libacl.la
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_pkgconfigdir}/libacl.pc
%{_mandir}/man3/acl_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libacl.a
