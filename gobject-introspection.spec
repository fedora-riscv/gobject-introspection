%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define         alphatag    20100115git

Name:           gobject-introspection
Version:        0.6.7.%{alphatag}
Release:        1%{?dist}
Summary:        Introspection system for GObject-based libraries

Group:		Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
#Source0:        ftp://ftp.gnome.org/pub/gnome/sources/%{name}/0.6/%{name}-%{version}.tar.bz2
# git clone git://git.gnome.org/gobject-introspection
# rm -fr gobject-introspection/.git
# tar -cvzf gobject-introspection.tar.gz gobject-introspection/
Source0:        %{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


# git snapshot requires some other fun stuff
BuildRequires:  autoconf >= 2.53
BuildRequires:  automake >= 1.10
BuildRequires:  gnome-common >= 2.2.0
BuildRequires:  libtool >= 1.4.3

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
#%setup -q

# git snapshot has a different directory name:
%setup -q -n %{name}
# needed to build the git tree
/bin/sh autogen.sh

%build
%configure
make V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-{compiler,generate}
# Mistake in upstream automake
rm -f $RPM_BUILD_ROOT/%{_bindir}/barapp

# Move the python modules to the correct location
mkdir -p $RPM_BUILD_ROOT/%{python_sitearch}
mv $RPM_BUILD_ROOT/%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT/%{python_sitearch}/

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
%{_datadir}/gobject-introspection-1.0
%{_datadir}/aclocal/introspection.m4
%{python_sitearch}/giscanner
%{_mandir}/man1/*.gz

%changelog
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
