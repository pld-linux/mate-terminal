#
# Conditional build:
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x
#
Summary:	MATE Terminal Emulator
Summary(pl.UTF-8):	Emulator terminala dla środowiska MATE
Name:		mate-terminal
Version:	1.6.2
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	30d12c11897e630ba3af07282adffd4d
Patch0:		wordseps.patch
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.30
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	sed >= 4.0
%{!?with_gtk3:BuildRequires:	vte0-devel >= 0.25.91}
%{?with_gtk3:BuildRequires:	vte-devel >= 0.25.91}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
Requires:	dconf >= 0.13.4
Requires:	glib2 >= 1:2.30
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	mate-desktop
%{!?with_gtk3:Requires:	vte0 >= 0.25.91}
%{?with_gtk3:Requires:	vte >= 0.25.91}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Terminal Emulator.

%description -l pl.UTF-8
Emulator terminala dla środowiska MATE.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' mate-terminal.wrapper

%build
mate-doc-common --copy
mate-doc-prepare --copy --force
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	%{?with_gtk3:--with-gtk=3.0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%find_lang %{name} --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-terminal
%attr(755,root,root) %{_bindir}/mate-terminal.wrapper
%{_mandir}/man1/mate-terminal.1*
%{_desktopdir}/mate-terminal.desktop
%{_datadir}/glib-2.0/schemas/org.mate.terminal.gschema.xml
%{_datadir}/mate-terminal
