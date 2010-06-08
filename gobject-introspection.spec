%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gobject-introspection
Version:        0.6.14
Release:        1%{?dist}
Summary:        Introspection system for GObject-based libraries

Group:      Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
Source0:        ftp://ftp.gnome.org/pub/gnome/sources/%{name}/0.6/%{name}-%{version}.tar.bz2

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
make V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-{compiler,generate}

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
%dir %{_libdir}/gobject-introspection
%{_libdir}/gobject-introspection/*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%dir %{_datadir}/gobject-introspection-1.0
%{_datadir}/gobject-introspection-1.0/*
%{_datadir}/aclocal/introspection.m4
%{_mandir}/man1/*.gz

%changelog
* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.14-1
- Update to 0.6.14

* Wed May 24 2010 Colin Walters <walters@verbum.org> - 0.6.12-1
- Update to latest upstream release 0.6.12

* Thu Mar 25 2010 Colin Walters <walters@verbum.org> - 0.6.9-3
- Move python library back into /usr/lib/gobject-introspection.  I put
  it there upstream for a reason, namely that apps need to avoid
  polluting the global Python site-packages with bits of their internals.
  It's not a public API.
  
  Possibly resolves bug #569885

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.9-2
- Added newly owned files (gobject-introspection-1.0 directory)

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.9-1
- Update to latest upstream release 0.6.9

* Thu Mar 11 2010 Colin Walters <walters@verbum.org> - 0.6.8-0.3.20100311git2cc97351
- rebuilt

* Thu Mar 11 2010 Colin Walters <walters@verbum.org>
- New upstream snapshot
- rm unneeded rm

* Thu Jan 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.8-0.1.20100128git
- Update to new git snapshot
- Fix Version tag to comply with correct naming use with alphatag

* Thu Jan 15 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.6.7.20100115git-1
- Update to git snapshot for rawhide 

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Fri Sep 11 2009 Colin Walters <walters@verbum.org> - 0.6.5-1
- New upstream
- Drop libtool dep 

* Fri Aug 28 2009 Colin Walters <walters@verbum.org> - 0.6.4-2
- Add dep on libtool temporarily

* Mon Aug 26 2009 Colin Walters <walters@verbum.org> - 0.6.4-1
- New upstream 0.6.4
- Drop upstreamed build fix patch 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-4
- Add upstream patch to fix a build crash

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-3
- Add -ggdb temporarily so it compiles on ppc64

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-2
- Add the new source file

* Thu Jul  2 2009 Peter Robinson <pbrobinson@gmail.com> - 0.6.3-1
- Update to 0.6.3

* Mon Jun  1 2009 Dan Williams <dcbw@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Colin Walters <walters@verbum.org> - 0.6.1-1
- Update to 0.6.1

* Fri Oct 31 2008 Colin Walters <walters@verbum.org> - 0.6.0-1
- Create spec goo
