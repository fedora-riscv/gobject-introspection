%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gobject-introspection
Version:        0.6.2
Release:        1%{?dist}
Summary:        Introspection system for GObject-based libraries

Group:		Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
Source0:        http://ftp.acc.umu.se/pub/GNOME/sources/gobject-introspection/0.6/gobject-introspection-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel
BuildRequires:  python-devel >= 2.5
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk-doc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libffi-devel
BuildRequires:  chrpath
BuildRequires:  mesa-libGL-devel
BuildRequires:  cairo-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libX11-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libXft-devel
BuildRequires:  freetype-devel

# For autogen
BuildRequires:  gnome-common
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package devel
Summary: Libraries and headers for gobject-introspection
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description devel
Libraries and headers for gobject-introspection

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-{compiler,generate}
# Mistake in upstream automake
rm -f $RPM_BUILD_ROOT/%{_bindir}/barapp

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING

%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{python_sitearch}/giscanner
%{_mandir}/man1/*.gz

%changelog
* Mon Jun  1 2009 Dan Williams <dcbw@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Colin Walters <walters@verbum.org> - 0.6.1-1
- Update to 0.6.1

* Fri Oct 31 2008 Colin Walters <walters@verbum.org> - 0.6.0-1
- Create spec goo
